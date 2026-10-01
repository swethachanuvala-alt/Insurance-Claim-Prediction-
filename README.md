# ClaimSense - Insurance Claim Prediction 

Multipage Streamlit app for the XGBoost insurance-claim model.

## Run locally (VS Code terminal / cmd)
```
python -m venv venv
venv\Scripts\activate          # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

## Use your own trained model (recommended)
Copy `xg_boost_model.pkl` and `scaler.pkl` (created by your notebook) into the `models/` folder.
If they are missing or incompatible, the app retrains them from `data/Insurance.csv` automatically
(or run `python train_model.py`).

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repo (see commands below).
2. Go to share.streamlit.io -> New app -> pick the repo, branch `main`, main file `app.py` -> Deploy.

```
git init
git add .
git commit -m "Insurance claim app"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```
