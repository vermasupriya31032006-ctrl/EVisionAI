import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def train_range_model():

    data = pd.read_csv(
        "ev_battery_dataset.csv"
    )

    features = [
        "Battery_Capacity_kWh",
        "Battery_Health_%",
        "Charge_Cycles",
        "Energy_Consumption_kWh_per_100km",
        "Temperature_C"
    ]

    X = data[features]

    y = data["Range_km"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    return model
    
