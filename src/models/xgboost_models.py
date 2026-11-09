import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
import joblib

def train_and_evaluate(model_name, file_path):
    print(f"--- Training {model_name} ---")
    df = pd.read_csv(file_path)
    df = df.sort_values('order_date')
    
    X = df.drop(columns=['daily_volume', 'order_date'])
    y = df['daily_volume']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    categorical_features = ['product_category_name_english']

    categorical_transformer = OneHotEncoder(handle_unknown='ignore') 

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough' 
    )
    

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', XGBRegressor(random_state=42))
    ])
    
    param_grid = {
    'model__n_estimators': [50, 100, 200],
    'model__max_depth': [3, 5, 7],
    'model__learning_rate': [0.01, 0.1, 0.2]
    }
    
    tscv = TimeSeriesSplit(n_splits=3)
    grid_search = GridSearchCV(pipeline, param_grid, cv=tscv, scoring='neg_mean_absolute_error', n_jobs=-1)

    
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    
   
    predictions = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"{model_name} MAE: {mae}")
    
    
    joblib.dump(best_model, f'../artifacts/model_{model_name}.joblib')
    print(f"Saved {model_name} artifact.\n")


day_model = [
    ('day1', 'E:/Projects/inventory-intelligence-suite/data/processed/olist_train_day1.csv'),
    ('day7', 'E:/Projects/inventory-intelligence-suite/data/processed/olist_train_day7.csv'),
    ('day15', 'E:/Projects/inventory-intelligence-suite/data/processed/olist_train_day15.csv'),
    ('day30', 'E:/Projects/inventory-intelligence-suite/data/processed/olist_train_day30.csv')
]

for name, path in day_model:
    train_and_evaluate(name, path)
    
'''
--- Training day1 ---
day1 MAE: 1.5528196739782496
Saved day1 artifact.

--- Training day7 ---
day7 MAE: 1.5846381922820576
Saved day7 artifact.

--- Training day15 ---
day15 MAE: 1.7398494965026214
Saved day15 artifact.

--- Training day30 ---
day30 MAE: 1.7713530150993053
Saved day30 artifact.

'''
