from pydantic import BaseModel, model_validator
from typing import Literal
from datetime import datetime, timedelta

class ForecastRequest(BaseModel):
    target_date: str 
    category: str
    forecast_window: Literal[1, 7, 15, 30]

    @model_validator(mode='after')
    def validate_date_boundaries(self):
       
        try:
            target_dt = datetime.strptime(self.target_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be exactly in YYYY-MM-DD format.")

        absolute_start = datetime(2017, 2, 23)
        absolute_end = datetime(2018, 8, 29)

        if target_dt < absolute_start:
            raise ValueError(f"Target date cannot be before {absolute_start.date()} due to lag calculation requirements.")
            
        if target_dt > absolute_end:
            raise ValueError(f"Target date cannot exceed the dataset limit of {absolute_end.date()}.")

        return self

class ForecastResponse(BaseModel):
    target_date: str
    category: str
    forecast_window: int
    predicted_sales: int