import pandas as pd


def segment_customer(score):

    score = int(score)

    if score >= 444:
        return "🏆 Champion"

    elif score >= 344:
        return "💎 Loyal"

    elif score >= 244:
        return "👍 Potential Loyalist"

    elif score >= 144:
        return "⚠️ At Risk"

    else:
        return "❌ Lost"


def calculate_rfm(df):

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    latest_date = df["Order_Date"].max()

    rfm = df.groupby("Customer_ID").agg({
        "Order_Date": lambda x: (latest_date - x.max()).days,
        "Order_ID": "count",
        "Revenue": "sum"
    })

    rfm.columns = [
        "Recency",
        "Frequency",
        "Monetary"
    ]

    rfm = rfm.reset_index()

    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        4,
        labels=[4, 3, 2, 1]
    )

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    )

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"],
        4,
        labels=[1, 2, 3, 4]
    )

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    rfm["Customer_Type"] = (
        rfm["RFM_Score"]
        .apply(segment_customer)
    )

    return rfm