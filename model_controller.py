from pipeline import model_training, trainingSet, featureExtraction
from datetime import date, timedelta
import joblib


startDate = "04/27/2025"

today = date.today()
yesterday = today - timedelta(days=1)

endDate = yesterday.strftime("%m/%d/%Y")

full_df = trainingSet.gather_data(startDate, endDate)

feature_df = featureExtraction.extract_features(full_df)

log_reg, xgb, rf, ensemble = model_training.train_models(feature_df)

# Save individual models
joblib.dump(log_reg, 'models/logistic_regression.pkl')
joblib.dump(xgb, 'models/xgboost_model.pkl')
joblib.dump(rf, 'models/random_forest_model.pkl')

# Save the ensemble model
joblib.dump(ensemble, 'models/ensemble_model.pkl')