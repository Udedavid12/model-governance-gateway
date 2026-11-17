# Model Governance Gateway

An API gateway designed for the banking industry to ensure Machine Learning models are safe, explainable, and compliant with regulations before making customer-facing decisions. 

## The Problem
Banks want to use AI for loan approvals and credit scoring, but they face massive regulatory risks. If an AI model denies a loan, the bank must prove *why* it did so, and they must prove it did not discriminate based on protected classes (like zip code or age).

## The Solution
This gateway sits between the frontend application and the Machine Learning model. It intercepts every request, validates the inputs, enforces fairness rules, and logs a complete audit trail.

## Features
*   **Explainability:** Returns the feature importances (why the model made its decision) alongside the prediction.
*   **Audit Logging:** Stores the inputs, outputs, model version, and flags in PostgreSQL for compliance reviews.
*   **Fairness Validation:** Automatically flags applications from protected zip codes for mandatory human review, even if the model approves them.
*   **Human-in-the-Loop:** Routes low-confidence predictions to human underwriters.

## Tech Stack
*   **Python & FastAPI** (API Gateway)
*   **Scikit-Learn** (Mock Credit Risk Model)
*   **PostgreSQL** (Audit Log Storage)
*   **SQLAlchemy** (ORM)
*   **Docker Compose** (Database)

## How to Run
1. Clone the repo and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt