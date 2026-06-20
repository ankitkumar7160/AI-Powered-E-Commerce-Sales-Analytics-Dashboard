import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def forecast_sales(df):

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    monthly_sales = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order_Date"] = monthly_sales["Order_Date"].astype(str)

    monthly_sales["Month_Number"] = range(1, len(monthly_sales) + 1)

    X = monthly_sales[["Month_Number"]]
    y = monthly_sales["Revenue"]

    model = LinearRegression()
    model.fit(X, y)

    next_month = [[len(monthly_sales) + 1]]

    predicted_sales = model.predict(next_month)[0]

    return monthly_sales, predicted_sales