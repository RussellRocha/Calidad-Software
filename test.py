import joblib
scaler = joblib.load("models/scaler.save")
print(len(scaler.feature_names_in_))
print(scaler.feature_names_in_)