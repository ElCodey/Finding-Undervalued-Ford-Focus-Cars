from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import xgboost as xg 

def linear_model(x_train, x_test, y_train, y_test):
    model = LinearRegression()
    model_fit = model.fit(x_train, y_train)
    y_predict = model_fit.predict(x_test)
    r2 = r2_score(y_test, y_predict)
    return model_fit, r2

def custom_input_for_model(model_fit, x, y_price):
    # x data for model_all has to be a list in this order:
    #'year', "mileage", "engineSize(Float)", 
    y_predict = model_fit.predict(np.array(x).reshape(1,-1))
    y_predict = round(float(y_predict))
    print(y_predict)
    actual_price = round(float(y_price))
    potential_profit = y_predict - actual_price   
    print("Potential Profit: £{}".format(potential_profit)) 
   
def xgb_r(df):
    xgb_r = xg.XGBRegressor(objective = "reg:squarederror", n_estimators = 10)
    xgb_r_fit = xgb_r.fit(np.array(df[["year", "mileage", "engineSize"]]), np.array(df["price"]))
    return xgb_r_fit

def live_predictor(model_fit, df):
    x = df[["year", "mileage", "engineSize"]]
    y = df["price"]
    y_predict = model_fit.predict(np.array(x).reshape(1,-1))
    r2 = r2_score(y, y_predict)
    return r2
