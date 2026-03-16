# Guardar señal en archivo
signal_data = {
    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    "signal": signal_map[predicted_class],
    "short_prob": float(prediction[0]),
    "hold_prob": float(prediction[1]),
    "long_prob": float(prediction[2])
}

with open("models/live_signal.json", "w") as f:
    json.dump(signal_data, f, indent=4)

print("Señal guardada en models/live_signal.json")