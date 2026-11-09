import pandas as pd 
from src.config import inference_load_csv_path


raw = pd.read_csv(inference_load_csv_path, parse_dates=['order_date'])

def rfm_engineer(target_date: str, requested_category: str, day_name: int):
    
    df_daily = raw.copy()
    
    target_dt = pd.to_datetime(target_date)
  
    df_daily = df_daily[df_daily['order_date'] <= target_dt]
    

    df_daily = df_daily[df_daily['product_category_name_english'] == requested_category]

  
    if day_name == 1:
        
        df_daily['lag_1'] = df_daily['daily_volume'].shift(1)
        df_daily['lag_7'] = df_daily['daily_volume'].shift(7)
        df_daily['lag_15'] = df_daily['daily_volume'].shift(15)
        df_daily['lag_30'] = df_daily['daily_volume'].shift(30)
        df_daily['rolling_7_avg'] = df_daily['lag_1'].rolling(window=7).mean()
        
        df_daily['rolling_30_avg'] = df_daily['lag_1'].rolling(window=30).mean()
        
    elif day_name == 7:
        
        df_daily['lag_1'] = df_daily['daily_volume'].shift(1)
        df_daily['lag_7'] = df_daily['daily_volume'].shift(7)
        df_daily['lag_15'] = df_daily['daily_volume'].shift(15)
        df_daily['lag_30'] = df_daily['daily_volume'].shift(30)
        df_daily['rolling_7_avg'] = df_daily['lag_1'].rolling(window=7).mean()
        df_daily['rolling_30_avg'] = df_daily['lag_1'].rolling(window=30).mean()
        
        df_daily = df_daily.drop(columns=['lag_1'])
        
    elif day_name == 15:
        df_daily['lag_1'] = df_daily['daily_volume'].shift(1)
        df_daily['lag_15'] = df_daily['daily_volume'].shift(15)
        df_daily['lag_30'] = df_daily['daily_volume'].shift(30)
        df_daily['rolling_30_avg'] = df_daily['lag_1'].rolling(window=30).mean()
        
        df_daily = df_daily.drop(columns=['lag_1'])

    elif day_name == 30:
        
        df_daily['lag_1'] = df_daily['daily_volume'].shift(1)
        df_daily['lag_30'] = df_daily['daily_volume'].shift(30)
        df_daily['rolling_30_avg'] = df_daily['lag_1'].rolling(window=30).mean()
        
        df_daily = df_daily.drop(columns=['lag_1'])
    
    df_daily['month'] = df_daily['order_date'].dt.month
    df_daily['day_of_week'] = df_daily['order_date'].dt.dayofweek
  
   
    columns_to_drop = ['order_date', 'daily_volume'] 
    df_daily = df_daily.drop(columns=columns_to_drop)
    
    final_feature_row = df_daily.iloc[[-1]]
    
    return final_feature_row



if __name__ == "__main__":
    
    test_row = rfm_engineer("2018-05-01", "health_beauty", 15)
    print("Columns:", test_row.columns.tolist())
    print(test_row)
    
