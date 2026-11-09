from fastapi import FastAPI , HTTPException
from src.api.schemas import ForecastRequest, ForecastResponse
import joblib
from src.config import inference_load_csv_path, day1_path, day7_path, day15_path, day30_path
from src.pipeline.rfm_engineer import rfm_engineer
import math
app=FastAPI(title="Sales Forecasting API", version="1.0")

models={
    1:joblib.load(day1_path),
    7:joblib.load(day7_path),
    15:joblib.load(day15_path),
    30:joblib.load(day30_path)
}

@app.post("/predict", response_model=ForecastResponse)
def predict_sales(request: ForecastRequest):
    try:
      
        model = models[request.forecast_window]
        
      
        features = rfm_engineer(
            target_date=request.target_date,
            requested_category=request.category,
            day_name=request.forecast_window
        )
        
       
        raw_prediction = float(model.predict(features)[0])
        prediction = math.ceil(raw_prediction)
        
    
        return ForecastResponse(
            target_date=request.target_date,
            category=request.category,
            forecast_window=request.forecast_window,
            predicted_sales=prediction
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))