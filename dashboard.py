
import streamlit as st
import pandas as pd
import plotly.express as px

from storage import load_expenses, save_expenses
from reports import (
    get_total_expenses,
    get_top_category,
    get_average_expense
)

# Page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide"
)

st.title("💸 Expense Tracker")
st.caption("Personal Finance Dashboard")

# Load expenses
expenses = load_expenses()
df = pd.DataFrame(expenses)

# Handle empty data
if df.empty:
    df = pd.DataFrame(columns=["amount", "category", "date"])

# Convert amount and date safely
if not df.empty:
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"]).dt.date

# Sidebar - Add Expense
st.sidebar.header("➕ Add Expense")

amount = st.sidebar.number_input(
    "Amount (₹)", min_value=0.0, step=100.0
)

category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Fuel", "Grocery", "Movie", "Shopping", "Other"]
)

custom_category = st.sidebar.text_input("Custom Category (optional)")

if st.sidebar.button("Add Expense"):
    if amount > 0:
        expense = {
            "amount": amount,
            "category": custom_category.strip().lower()
                if custom_category.strip() else category.lower(),
            "date": pd.Timestamp.today().strftime("%Y-%m-%d")
        }

        expenses.append(expense)
        save_expenses(expenses)

        st.sidebar.success("Expense added!")
        st.rerun()
    else:
        st.sidebar.error("Enter a valid amount!")

# Reload data after adding expense
expenses = load_expenses()
df = pd.DataFrame(expenses)

if df.empty:
    df = pd.DataFrame(columns=["amount", "category", "date"])

if not df.empty:
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"]).dt.date

# Sidebar - Filter
st.sidebar.header("🔎 Filters")

categories = ["All"] + sorted(df["category"].unique().tolist()) if not df.empty else ["All"]

selected_category = st.sidebar.selectbox(
    "Filter Category", categories
)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

# KPI Metrics
total = get_total_expenses(filtered_df.to_dict("records"))
top = get_top_category(filtered_df.to_dict("records"))
average = get_average_expense(filtered_df.to_dict("records"))

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Spending", f"₹{total:,.2f}")
col2.metric("🧾 Transactions", len(filtered_df))
col3.metric("📊 Average Expense", f"₹{average:,.2f}")
col4.metric("🏆 Top Category", top)

st.divider()

# Charts
if not filtered_df.empty:

    col1, col2 = st.columns(2)

    # Category Pie Chart
    with col1:
        st.subheader("🍲 Category Breakdown")

        category_totals = (
            filtered_df.groupby("category")["amount"]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            category_totals,
            names="category",
            values="amount",
            hole=0.4
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # Monthly Spending
    with col2:
        st.subheader("📅 Monthly Spending")

        monthly = filtered_df.copy()
        monthly["month"] = pd.to_datetime(monthly["date"]).dt.strftime("%b %Y")

        monthly_totals = (
            monthly.groupby("month")["amount"]
            .sum()
            .reset_index()
        )

        fig_bar = px.bar(
            monthly_totals,
            x="month",
            y="amount",
            text_auto=".2s"
        )

        fig_bar.update_yaxes(title="Amount (₹)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Daily Spending Trend
    st.subheader("📈 Daily Spending Trend")

    daily = (
        filtered_df.groupby("date")["amount"]
        .sum()
        .reset_index()
    )

    daily["date"] = pd.to_datetime(daily["date"])

    fig_line = px.line(
        daily,
        x="date",
        y="amount",
        markers=True
    )

    fig_line.update_xaxes(
        tickformat="%d %b",
        dtick="D1",
        title="Date"
    )

    fig_line.update_yaxes(title="Amount (₹)")

    st.plotly_chart(fig_line, use_container_width=True)

    # Expense History
    st.subheader("🧾 Expense History")

    history = filtered_df.copy()
    history["date"] = pd.to_datetime(history["date"]).dt.strftime("%d %b %Y")

    history = history.sort_values("date", ascending=False)

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No expenses available. Add your first expense!")
