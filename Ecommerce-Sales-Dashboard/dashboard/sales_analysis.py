import pandas as pd


def get_sales_metrics(df):
    """
    Main Sales KPIs
    """

    total_revenue = df["Revenue"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order_ID"].nunique()

    average_order_value = (
        round(total_revenue / total_orders, 2)
        if total_orders > 0 else 0
    )

    profit_margin = (
        round((total_profit / total_revenue) * 100, 2)
        if total_revenue > 0 else 0
    )

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "profit_margin": profit_margin
    }


def monthly_sales_trend(df):
    """
    Monthly Revenue Trend
    """

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    monthly_sales = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order_Date"] = (
        monthly_sales["Order_Date"].astype(str)
    )

    return monthly_sales


def daily_sales_trend(df):
    """
    Daily Revenue Trend
    """

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    daily_sales = (
        df.groupby(df["Order_Date"].dt.date)["Revenue"]
        .sum()
        .reset_index()
    )

    return daily_sales


def category_sales(df):
    """
    Category-wise Revenue
    """

    category_df = (
        df.groupby("Category")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    return category_df


def payment_method_sales(df):
    """
    Revenue by Payment Method
    """

    payment_df = (
        df.groupby("Payment_Method")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    return payment_df


def state_wise_sales(df):
    """
    State-wise Revenue
    """

    state_df = (
        df.groupby("State")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    return state_df


def city_wise_sales(df):
    """
    City-wise Revenue
    """

    city_df = (
        df.groupby("City")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    return city_df


def monthly_profit_trend(df):
    """
    Monthly Profit Trend
    """

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    profit_df = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Profit"]
        .sum()
        .reset_index()
    )

    profit_df["Order_Date"] = (
        profit_df["Order_Date"].astype(str)
    )

    return profit_df