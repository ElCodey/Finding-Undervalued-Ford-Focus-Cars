from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

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
   