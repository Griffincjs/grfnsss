from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import datetime
from datetime import date, timedelta
from database import SessionLocal, init_db, Sale as SaleModel
import pandas as pd
from prophet import Prophet
import io

# Initialize the database tables
init_db()

app = FastAPI(title="Smart Clothing BI API")

# --- DATA MODELS ---
class Recommendation(BaseModel):
    type: str
    sku: str
    message: str
    actionable_value: float

class SalesRecord(BaseModel):
    date: date
    sku: str
    category: str
    quantity_sold: int
    price: float

# --- ENDPOINTS ---
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "online", "system": "Smart Clothing BI"}

@app.get("/ml/recommendations", response_model=List[Recommendation], tags=["Machine Learning"])
def get_recommendations():
    db = SessionLocal()
    try:
        sales = db.query(SaleModel).all()
        if not sales:
            return []

        df = pd.DataFrame([s.__dict__ for s in sales])
        sku_stats = df.groupby("sku")["quantity"].sum().sort_values(ascending=False)

        top_sku = sku_stats.index[0]
        top_qty = int(sku_stats.iloc[0])
        bottom_sku = sku_stats.index[-1]
        bottom_qty = int(sku_stats.iloc[-1])

        return [
            Recommendation(
                type="RESTOCK",
                sku=top_sku,
                message=f"High Demand! You've sold {top_qty} units. Restock soon to avoid losing momentum.",
                actionable_value=float(top_qty)
            ),
            Recommendation(
                type="DISCOUNT",
                sku=bottom_sku,
                message=f"Slow Mover. Only {bottom_qty} units sold. Suggest a 15% discount to clear space.",
                actionable_value=0.85
            )
        ]
    except Exception as e:
        print(f"Error calculating recommendations: {e}")
        return []
    finally:
        db.close()

@app.post("/data/upload", tags=["Data Ingestion"])
def upload_sales_data(records: List[SalesRecord]):
    """Upload sales records as a JSON list (used by generate_data.py)."""
    db = SessionLocal()
    try:
        for rec in records:
            new_sale = SaleModel(
                date=rec.date,
                sku=rec.sku,
                category=rec.category,
                quantity=rec.quantity_sold,
                price=rec.price
            )
            db.add(new_sale)
        db.commit()
        return {"status": "success", "message": f"Saved {len(records)} items to the database!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/data/upload/csv", tags=["Data Ingestion"])
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file. Required columns: date, sku, category, quantity_sold, price."""
    db = SessionLocal()
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Validate that the CSV has the right columns
        required_cols = {"date", "sku", "category", "quantity_sold", "price"}
        missing = required_cols - set(df.columns)
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"CSV is missing required columns: {missing}. Required: {required_cols}"
            )

        count = 0
        for _, row in df.iterrows():
            new_sale = SaleModel(
                date=pd.to_datetime(row["date"]).date(),
                sku=str(row["sku"]),
                category=str(row["category"]),
                quantity=int(row["quantity_sold"]),
                price=float(row["price"])
            )
            db.add(new_sale)
            count += 1

        db.commit()
        return {"status": "success", "message": f"Saved {count} records from CSV to the database!"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/data/sales", tags=["Data Retrieval"])
def get_all_sales():
    db = SessionLocal()
    try:
        sales = db.query(SaleModel).all()
        return sales
    finally:
        db.close()

@app.get("/analytics/trends", tags=["Machine Learning"])
def get_trends():
    db = SessionLocal()
    try:
        sales = db.query(SaleModel).all()
        if not sales:
            return []
        df = pd.DataFrame([s.__dict__ for s in sales])
        df["date"] = pd.to_datetime(df["date"])

        today = datetime.datetime.now()
        last_7_days = today - timedelta(days=7)
        previous_7_days = today - timedelta(days=14)

        curr_stats = df[df["date"] >= last_7_days].groupby("category")["quantity"].sum()
        past_stats = df[(df["date"] >= previous_7_days) & (df["date"] < last_7_days)].groupby("category")["quantity"].sum()

        trends = []
        for category in curr_stats.index:
            current_val = curr_stats[category]
            past_val = past_stats.get(category, 1)
            growth = ((current_val - past_val) / past_val) * 100
            trends.append({
                "category": category,
                "growth_pct": round(growth, 2),
                "status": "🔥 Trending UP" if growth > 10 else "🧊 Stable"
            })
        return sorted(trends, key=lambda x: x["growth_pct"], reverse=True)
    finally:
        db.close()

@app.get("/ml/forecast/{category}", tags=["Machine Learning"])
def get_category_forecast(category: str):
    db = SessionLocal()
    try:
        sales = db.query(SaleModel).filter(SaleModel.category == category).all()
        if len(sales) < 5:
            return {"error": "Need more data"}
        df = pd.DataFrame([{"ds": s.date, "y": s.quantity} for s in sales]).groupby("ds").sum().reset_index()
        model = Prophet(yearly_seasonality=False, daily_seasonality=False).fit(df)
        future = model.make_future_dataframe(periods=14)
        forecast = model.predict(future)
        return forecast[["ds", "yhat"]].tail(14).to_dict("records")
    finally:
        db.close()
