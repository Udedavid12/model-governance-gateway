import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    client_id = Column(String, index=True)
    model_name = Column(String, index=True)
    model_version = Column(String)
    
    input_features = Column(JSON)
    prediction_output = Column(Float)
    
    passed_validation = Column(Boolean, default=True)
    
    # NEW: Fairness tracking
    flagged_for_fairness = Column(Boolean, default=False) 
    requires_human_review = Column(Boolean, default=False)
    
    timestamp = Column(DateTime, default=datetime.utcnow)