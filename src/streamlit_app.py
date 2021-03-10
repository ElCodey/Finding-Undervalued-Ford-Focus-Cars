import streamlit as st
import pandas as pd
import numpy as np
from models import xgb_r, custom_input_for_model, live_predictor
from data_preparation import split_years_df, split_train
from aa_web_scraper import main
import xgboost as xg 


def train_model():
    df_17 , df_18 , df_19 ,df_all = split_years_df()
    fitted_model = xgb_r(df_all)
    return fitted_model


def load_data():
    df = pd.read_csv("scrape_car_df.csv")
    df = df.dropna()
    indexNames = df[ df['engineSize'] == 0.0 ].index
    df.drop(indexNames , inplace=True)
    df = df.drop_duplicates(subset=["car_name", "mileage"])
    df_17_new = df[df["year"] == 2017]
    df_18_new = df[df["year"] == 2018]
    df_19_new = df[df["year"] == 2019]
    return df_17_new, df_18_new, df_19_new

def predict(df):
    fitted_model = train_model() 
    x = df[["year", "mileage", "engineSize"]]
    y = df["price"]
    y_predict = fitted_model.predict(np.array(x))
    predicted = pd.DataFrame(y_predict, columns=["predicted"])
    df["predicted"] = (predicted.values).round(2)
    df["potential_profit"] = (df["predicted"] - df["price"]).round()
    return df


def model_and_results():
    df_17_new, df_18_new, df_19_new = load_data()

    df_predictions_17 = predict(df_17_new)
    df_predictions_18 = predict(df_18_new)
    df_predictions_19 = predict(df_19_new)

    return df_predictions_17, df_predictions_18, df_predictions_19

st.header("Ford Focus Car Predictors From AA")
df_predictions_17, df_predictions_18, df_predictions_19 = model_and_results()
add_select = st.sidebar.selectbox("Model Year", ("2017", "2018", "2019"))

if add_select == "2017":
    st.write(df_predictions_17.sort_values(by=["potential_profit"], ascending=False))
elif add_select == "2018":
    st.write(df_predictions_18.sort_values(by=["potential_profit"], ascending=False))
elif add_select == "2019":
    st.write(df_predictions_19.sort_values(by=["potential_profit"], ascending=False))



