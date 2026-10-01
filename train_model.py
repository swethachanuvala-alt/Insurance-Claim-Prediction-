"""Run `python train_model.py` to re-create models/xg_boost_model.pkl and models/scaler.pkl."""
from utils.training import train_and_save, MODEL_PATH, SCALER_PATH

train_and_save()
print("Done ->", MODEL_PATH, "|", SCALER_PATH)
