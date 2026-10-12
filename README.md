# Smart Clothing BI: Sales Analytics & Demand Forecasting Dashboard

A business intelligence dashboard for a clothing retailer. It turns raw sales records into live KPIs, category insights, 14-day demand forecasts and restock recommendations, so that inventory decisions are based on data rather than guesswork.

Built as my final-year project for a BSc in Data Science (KCA University).

## The problem

Retail teams often track sales in spreadsheets and decide what to restock by gut feeling. This leads to stock-outs on popular items and overstock on slow ones. This project brings sales data into one database and shows the key numbers and recommended actions in a single dashboard.

## Features

- **Executive dashboard:** total revenue, units sold and unique SKUs at a glance.
- **Category performance:** a bar chart of units sold per product category, plus a live feed of the latest sales records.
- **Demand forecasting:** a 14-day forecast of units sold for each category (T-Shirts, Pants, Outerwear), based on historical sales trends.
- **Action plan:** automatic RESTOCK and other suggestions per SKU, based on the sales data.
- **Data management:** upload sales data as a CSV file, preview it, then load it into the database.
- **System status:** a live health check that shows whether the backend is online.
- **Flexible database:** SQLite for local use, PostgreSQL when deployed to the cloud.

## Tech stack

| Layer | Tools |
|-------|-------|
| Language | Python |
| Dashboard / front end | Streamlit |
| Data handling | Pandas |
| Backend | REST API (`main.py`) |
| Database | SQLite (local), PostgreSQL (cloud) |
| Deployment | Render |

## Project structure

```
├── dashboard.py        # Streamlit dashboard (the user interface)
├── main.py             # Backend API serving sales data, forecasts and recommendations
├── database.py         # Database connection and setup
├── generate_data.py    # Generates sample sales data for testing
└── requirements.txt    # Python dependencies
```

## Getting started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Griffincjs/grfnsss.git
   cd grfnsss
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend API** (runs on `http://127.0.0.1:8000` by default)
   ```bash
   uvicorn main:app --reload
   ```

4. **Generate sample data** (optional)
   ```bash
   python generate_data.py
   ```

5. **Launch the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

### Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `API_URL` | Address of the backend API used by the dashboard | `http://127.0.0.1:8000` |
| `DATABASE_URL` | PostgreSQL connection string. If not set, SQLite is used. | not set |

## Uploading your own data

On the **Data Management** page, upload a CSV file with these columns:

`date`, `sku`, `category`, `quantity_sold`, `price`

The dashboard shows a preview of the first rows before you confirm the upload to the database.

## What I learned

- Designing a full data pipeline: ingestion, storage, analysis and visualization.
- Cleaning and validating data before it reaches the database.
- Using time-series trends to forecast demand.
- Building a clean, usable dashboard for non-technical decision makers.
- Deploying an app with a cloud database (Render, PostgreSQL).

## Possible improvements

- Add screenshots and a live demo link.
- Add automated tests for the data upload and forecasting logic.
- Add user login and role-based access.

## Author

**Olome Griffins Lugongo**: Data Science student, KCA University
griffinolome@gmail.com
