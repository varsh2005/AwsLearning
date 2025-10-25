# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import joblib

# toy dataset generator
def make_data(n=2000):
    np.random.seed(42)
    base_price = np.random.uniform(10, 100, n)
    demand = np.random.poisson(5, n) + np.random.rand(n)
    competition_price = base_price + np.random.normal(0, 5, n)
    time_of_day = np.random.randint(0, 24, n)
    day_of_week = np.random.randint(0, 7, n)
    # target: price should grow with demand and competition, with noise
    price = base_price * (1 + 0.05 * (demand - 3)) + 0.2 * (competition_price - base_price) + 2*np.sin(time_of_day/24*2*np.pi)
    price += np.random.normal(0, 3, n)
    df = pd.DataFrame({
        'base_price': base_price,
        'demand': demand,
        'competition_price': competition_price,
        'time_of_day': time_of_day,
        'day_of_week': day_of_week,
        'price': price
    })
    return df

def train_and_save():
    df = make_data()
    X = df[['base_price','demand','competition_price','time_of_day','day_of_week']]
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    model = XGBRegressor(n_estimators=100, max_depth=4, random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    joblib.dump(model, 'model.pkl')
    print("Saved model.pkl")

if __name__ == "__main__":
    train_and_save()
