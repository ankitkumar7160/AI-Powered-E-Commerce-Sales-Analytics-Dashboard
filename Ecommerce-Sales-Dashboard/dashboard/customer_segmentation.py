import pandas as pd
from sklearn.cluster import KMeans


def segment_customers(df):

    customer_data = (
        df.groupby("Customer_ID")
        .agg({
            "Revenue": "sum",
            "Order_ID": "count"
        })
        .reset_index()
    )

    customer_data.rename(
        columns={
            "Revenue": "Total_Spending",
            "Order_ID": "Total_Orders"
        },
        inplace=True
    )

    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    customer_data["Cluster"] = kmeans.fit_predict(
        customer_data[
            ["Total_Spending", "Total_Orders"]
        ]
    )

    return customer_data