from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, engine, Base
from models import AuditLog
from ml_model import model

# Drop and recreate to apply the new schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Model Governance Gateway")

class LoanApplication(BaseModel):
    client_id: str
    income: float
    credit_score: int
    zip_code: str # NEW: We need to monitor this

@app.post("/api/v1/predict/loan")
def predict_loan(application: LoanApplication, db: Session = Depends(get_db)):
    if application.income < 0 or application.credit_score < 300 or application.credit_score > 850:
        raise HTTPException(status_code=400, detail="Invalid input data.")

    prediction, confidence, explanation = model.predict(application.income, application.credit_score)
    
    # --- FAIRNESS RULE ---
    # Mock rule: Zip codes starting with "902" are protected zones.
    # The model's prediction is overridden and sent to a human.
    flagged_for_fairness = application.zip_code.startswith("902")
    
    # Human review is triggered if confidence is low OR if flagged for fairness
    requires_human_review = bool(confidence < 0.70) or flagged_for_fairness
    
    log = AuditLog(
        client_id=application.client_id,
        model_name="CreditRiskModel",
        model_version=model.version,
        input_features=application.model_dump(),
        prediction_output=float(prediction),
        passed_validation=True,
        flagged_for_fairness=flagged_for_fairness,
        requires_human_review=requires_human_review
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "application_id": log.id,
        "prediction": "Approved" if prediction == 1 else "Rejected",
        "confidence": confidence,
        "explanation": explanation,
        "flagged_for_fairness": flagged_for_fairness,
        "requires_human_review": requires_human_review
    }