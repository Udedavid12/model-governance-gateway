import numpy as np
from sklearn.tree import DecisionTreeClassifier

class CreditRiskModel:
    def __init__(self):
        self.version = "v1.2.0"
        X = np.array([[50000, 700], [30000, 500], [100000, 800], [20000, 400], [60000, 650]])
        y = np.array([1, 0, 1, 0, 1])
        self.model = DecisionTreeClassifier(max_depth=3)
        self.model.fit(X, y)
        
        # The model tracks how important each feature is
        # [Income Importance, Credit Score Importance]
        self.feature_importances = self.model.feature_importances_

    def predict(self, income: float, credit_score: int):
        features = np.array([[income, credit_score]])
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = max(probabilities)
        
        # Create a simple explanation dictionary
        # In a real bank, this would use SHAP or LIME
        explanation = {
            "income_impact": float(self.feature_importances[0]),
            "credit_score_impact": float(self.feature_importances[1])
        }
        
        return int(prediction), float(confidence), explanation

model = CreditRiskModel()