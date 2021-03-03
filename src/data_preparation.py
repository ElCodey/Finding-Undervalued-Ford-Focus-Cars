import pandas as pd 
from sklearn.model_selection import train_test_split

def split_years_df():
    df_focus = pd.read_csv("focus.csv")
    df_focus = pd.get_dummies(df_focus)
    df_focus.drop(columns="model_ Focus", inplace=True)
    focus_2017 = df_focus[(df_focus["year"]==2017)]
    focus_2018 = df_focus[(df_focus["year"]==2018)]
    focus_2019 = df_focus[(df_focus["year"]==2019)]
    
    return focus_2017, focus_2018, focus_2019

def split_train(df, X):
    x = df[X]
    y = df["price"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    return x_train, x_test, y_train, y_test

