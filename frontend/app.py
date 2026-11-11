import streamlit as st
import requests
from datetime import datetime, date


st.set_page_config(page_title="Olist Demand Forecaster", layout="wide")
st.title("📦 Olist Strategic Intelligence Suite")
st.markdown("### Multi-Horizon Sales Forecasting Engine")


col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Forecast Parameters")
    
    
    MIN_DATE = date(2017, 2, 23)
    MAX_DATE = date(2018, 8, 29)

    # 2. Lock the Streamlit calendar
    target_date = st.date_input(
        "Target Date", 
        min_value=MIN_DATE, 
        max_value=MAX_DATE, 
        value=date(2018, 5, 1)  
    )
    
    category = st.selectbox(
        "Product Category", 
       ['agro_industry_and_commerce', 'air_conditioning', 'art', 'arts_and_craftmanship', 'audio', 'auto', 'baby', 'bed_bath_table', 'books_general_interest', 'books_imported', 'books_technical', 'cds_dvds_musicals', 'christmas_supplies', 'cine_photo', 'computers', 'computers_accessories', 'consoles_games', 'construction_tools_construction', 'construction_tools_lights', 'construction_tools_safety', 'cool_stuff', 'costruction_tools_garden', 'costruction_tools_tools', 'diapers_and_hygiene', 'drinks', 'dvds_blu_ray', 'electronics', 'fashio_female_clothing', 'fashion_bags_accessories', 'fashion_childrens_clothes', 'fashion_male_clothing', 'fashion_shoes', 'fashion_sport', 'fashion_underwear_beach', 'fixed_telephony', 'flowers', 'food', 'food_drink', 'furniture_bedroom', 'furniture_decor', 'furniture_living_room', 'furniture_mattress_and_upholstery', 'garden_tools', 'health_beauty', 'home_appliances', 'home_appliances_2', 'home_comfort_2', 'home_confort', 'home_construction', 'housewares', 'industry_commerce_and_business', 'kitchen_and_food_preparation_portables', 'kitchen_dining_laundry_garden_furniture', 'la_cuisine', 'luggage_accessories', 'market_place', 'music', 'musical_instruments', 'office_furniture', 'party_supplies', 'pc_gamer', 'perfumery', 'pet_shop', 'security_and_services', 'signaling_and_security', 'small_appliances', 'small_appliances_home_oven_and_coffee', 'sports_leisure', 'stationery', 'tablets_printing_image', 'telephony', 'toys', 'watches_gifts']
    )
    
    forecast_window = st.radio(
        "Forecast Horizon (Days)", 
        options=[1, 7, 15, 30],
        horizontal=True
    )
    
    analyze_btn = st.button("Run Demand Forecast", type="primary", use_container_width=True)

with col2:
    st.subheader("Engine Output")
    
    if analyze_btn:
       
        payload = {
            "target_date": str(target_date), 
            "category": category,
            "forecast_window": forecast_window
        }
        
        API_URL = "http://127.0.0.1:8000/predict"
        
        try:
            with st.spinner(f"Computing RFM features and running {forecast_window}-day model..."):
                response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
          
                st.success("API Connection & Feature Engineering Successful")
                
               
                st.metric(
                    label=f"Predicted Sales ({forecast_window}-Day Horizon)", 
                    value=f"{result['predicted_sales']} Units"
                )
                
                
                with st.expander("View Raw API Response"):
                    st.json(result)
                    
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Connection Failed. Ensure your FastAPI Uvicorn server is running on port 8000.")