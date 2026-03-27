from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Smart Clothing Business Intelligence and Trend Forecasting System",
    description="Backend for inventory, sales tracking, and ML forecasting.",
    version="1.0.0"
)

# 2. Define Data Models (Pydantic)
# This ensures that any data coming into or leaving our API is strictly validated.
class Recommendation(BaseModel):
    type: str              # e.g., "RESTOCK", "DISCOUNT", "TRENDING"
    sku: str               # e.g., "JEANS-BLU-32"
    message: str           # e.g., "Stock depleting in 4 days."
    actionable_value: float

class SalesRecord(BaseModel):
    date: datetime.date
    sku: str
    category: str
    quantity_sold: int
    price: float

# 3. Create API Endpoints
@app.get("/", tags=["Health"])
def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "online", "system": "Smart Clothing BI"}

@app.get("/ml/recommendations", response_model=List[Recommendation], tags=["Machine Learning"])
def get_recommendations(limit: int = 5):
    """
    Returns a list of actionable insights for the seller.
    (Currently returning mock data until we build the ML pipeline).
    """
    # In the future, this will call our Pandas/Scikit-learn logic.
    mock_data = [
        Recommendation(
            type="RESTOCK",
            sku="JEANS-BLU-32",
            message="Current stock (12) will deplete in 4 days based on forecasted demand.",
            actionable_value=25.0
        ),
        Recommendation(
            type="DISCOUNT",
            sku="WINTER-COAT-L",
            message="High inventory with low sales velocity. Suggest 20% markdown.",
            actionable_value=0.8
        )
    ]
    return mock_data[:limit]

@app.post("/data/upload", tags=["Data Ingestion"])
def upload_sales_data(records: List[SalesRecord]):
    """
    Accepts a list of sales records.
    FastAPI automatically checks if the incoming data matches the SalesRecord model.
    """
    # Later, we will write this to our PostgreSQL database
    return {
        "status": "success", 
        "message": f"Successfully received {len(records)} records for processing."
    }