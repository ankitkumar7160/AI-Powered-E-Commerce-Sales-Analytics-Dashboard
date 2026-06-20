import pandas as pd


def revenue_growth(df):

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    monthly = (
        df.groupby(df["Order_Date"].dt.to_period("M"))
        .agg({
            "Revenue": "sum",
            "Profit": "sum",
            "Order_ID": "count"
        })
        .reset_index()
    )

    monthly["Order_Date"] = monthly["Order_Date"].astype(str)

    if len(monthly) < 2:
        return 0, 0, 0

    current = monthly.iloc[-1]
    previous = monthly.iloc[-2]

    revenue_growth = (
        (current["Revenue"] - previous["Revenue"])
        / previous["Revenue"]
    ) * 100

    profit_growth = (
        (current["Profit"] - previous["Profit"])
        / previous["Profit"]
    ) * 100

    order_growth = (
        (current["Order_ID"] - previous["Order_ID"])
        / previous["Order_ID"]
    ) * 100

    return (
        round(revenue_growth, 2),
        round(profit_growth, 2),
        round(order_growth, 2)
    )