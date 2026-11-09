import pandas as pd
from src.config import olist_clean_csv_path

raw = pd.read_csv(olist_clean_csv_path,parse_dates=['order_date','order_purchase_timestamp'])
# df=pd.read_csv(olist_clean_csv_path)
# print(df.head())
# print(df.info())
def data_merger(raw):

    df=raw.copy()

    
    df_time_series = df.groupby(['order_date', 'product_category_name_english']).agg(
        daily_volume=('quantity', 'sum'),       # SUM the volume, do not count the rows
        median_price=('price', 'median'),       # MEDIAN to ignore $2,000 outliers
        median_freight=('freight_value', 'median')
    ).reset_index()
    
    df_time_series = df_time_series.set_index('order_date')
    df_time_series = df_time_series[df_time_series.index >= '2017-01-01']
    
    df_daily = df_time_series.groupby('product_category_name_english')[['daily_volume', 'median_price', 'median_freight']].resample('D').asfreq().reset_index()
    
    df_daily['daily_volume'] = df_daily['daily_volume'].fillna(0)
    df_daily['median_price'] = df_daily.groupby('product_category_name_english')['median_price'].ffill()
    df_daily['median_freight'] = df_daily.groupby('product_category_name_english')['median_freight'].ffill()
    print(df_daily.head(2))
    
    df_daily = df_daily.sort_values(by=['product_category_name_english', 'order_date'])
    print(df_daily.isna().sum())
    
    return df_daily


processed_csv=data_merger(raw)

processed_csv.to_csv("data/processed/olist_daily_grouped.csv", index=False)
   




    # E:\Projects\inventory-intelligence-suite\src\pipeline\data_merger.py
    
'''
 0   order_id                       98795 non-null  str    
 1   customer_id                    98795 non-null  str    
 2   order_purchase_timestamp       98795 non-null  str    
 3   product_id                     98795 non-null  str    
 4   price                          98795 non-null  float64
 5   freight_value                  98795 non-null  float64
 6   product_category_name_english  98795 non-null  str    
 7   quantity                       98795 non-null  int64  
 8   order_date                     98795 non-null  str  
'''

