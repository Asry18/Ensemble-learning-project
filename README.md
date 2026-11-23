# Sri Lankan Used Vehicle Price Prediction – Ensemble Learning Project

Compares Random Forest, XGBoost, an ANN and a hybrid RF + ANN model on Sri Lankan used-vehicle listings (Kaggle), with a Streamlit dashboard.
Prices are in units of LKR 100,000 (lakhs). Models are trained on log(1+price); metrics are reported in original units.

## Structure
```
dataset/car_prices.csv        raw Kaggle data  (dataset/processed/ = cleaned data + train/val/test splits)
notebooks/                    run in order 01 -> 04  (common.py = shared paths, feature lists, metric function)
  01_data_exploration         cleaning, EDA, 70/15/15 split, shared preprocessing pipeline
  02_random_forest            baseline + random search (3-fold CV) + test evaluation
  03_xgboost                  same protocol and search budget as 02
  04_model_comparison         ANN, hybrid RF+ANN, final metrics, bootstrap test RF vs XGBoost
models/                       random_forest.pkl, xgboost.json, ann.keras, preprocessor.pkl
results/                      metrics.json, predictions.csv, feature_importance.csv, ...
dashboard/app.py              Streamlit dashboard (reads models/ and results/); dashboard/styles.py = design tokens, CSS, chart style
.streamlit/config.toml        Streamlit theme (light, indigo accent)
```

## Run
```
pip install -r requirements.txt
cd notebooks          # run 01, 02, 03, 04 in order (Jupyter), regenerates models/ and results/
cd .. && streamlit run dashboard/app.py   # run from the project root so .streamlit/config.toml is picked up
```

## Fair comparison design
Same cleaned data, same fixed split, same preprocessing (fitted on train only), same CV folds and same search budget for RF and XGBoost; the test set is used once for final evaluation. The hybrid weight is chosen on the validation set only.

## Limitations
Mileage is almost perfectly determined by year of manufacture in this dataset; prices are advertised asking prices; errors are larger for expensive vehicles.
