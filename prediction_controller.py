from pipeline import trainingSet, featureExtraction
from datetime import date
import joblib

today = date.today()
today_string = today.strftime("%m/%d/%Y")

full_df = trainingSet.gather_data(today_string, today_string)

feature_df, meta_data_df = featureExtraction.extract_features(full_df)

# Load models
log_reg = joblib.load('models/logistic_regression.pkl')
xgb = joblib.load('models/xgboost_model.pkl')
rf = joblib.load('models/random_forest_model.pkl')
ensemble = joblib.load('models/ensemble_model.pkl')

# Make Predictions
log_reg_preds = log_reg.predict_proba(feature_df)[:,1]
xgb_preds = xgb.predict_proba(feature_df)[:,1]
rf_preds = rf.predict_proba(feature_df)[:,1]
ensemble_preds = ensemble.predict_proba(feature_df)[:,1]

#Add predictions to data
output_df = meta_data_df.copy()
output_df["Log_Reg_Preds"] = log_reg_preds
output_df["XGB_Preds"] = xgb_preds
output_df["RF_Preds"] = rf_preds
output_df["Ensemble_Preds"] = ensemble_preds