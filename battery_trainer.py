import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def load_dataset():

    data = pd.read_csv(
        "datahub/ev_battery_dataset.csv"
    )

    return data


def train_health_model():

    data = load_dataset()

    features = [
        "Battery_Capacity_kWh",
        "Range_km",
        "Charge_Cycles",
        "Energy_Consumption_kWh_per_100km",
        "Mileage_km",
        "Avg_Speed_kmh",
        "Temperature_C"
    ]

    X = data[features]

    y = data["Battery_Health_%"]

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

    model.fit(X_train, y_train)
    
    return model
    