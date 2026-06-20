def generate_insights(df):

    top_category = (
        df.groupby("Category")["Revenue"]
        .sum()
        .idxmax()
    )

    top_product = (
        df.groupby("Product")["Revenue"]
        .sum()
        .idxmax()
    )

    top_state = (
        df.groupby("State")["Revenue"]
        .sum()
        .idxmax()
    )

    top_payment = (
        df["Payment_Method"]
        .value_counts()
        .idxmax()
    )

    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()

    insights = [
        f"📌 Top Revenue Category: {top_category}",
        f"📌 Best Selling Product: {top_product}",
        f"📌 Highest Sales State: {top_state}",
        f"📌 Most Used Payment Method: {top_payment}",
        f"📌 Total Revenue: ₹{total_revenue:,.0f}",
        f"📌 Total Profit: ₹{total_profit:,.0f}",
    ]

    return insights