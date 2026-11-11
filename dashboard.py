
import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import date
from storage import load_expenses, save_expenses
from reports import get_total_expenses, get_top_category, get_average_expense

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide"
)

st.title("💸 Expense Tracker")
st.caption("Personal Finance Dashboard")

# Load expenses
expenses = load_expenses()

# Sidebar
st.sidebar.header("➕ Add Expense")

with st.sidebar.form("expense_form"):
    amount = st.number_input("Amount (₹)", min_value=0.0)
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills",
         "Entertainment", "Health", "Other"]
    )
    custom_category = st.text_input("Custom Category (optional)")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    if amount <= 0:
        st.sidebar.error("Enter a valid amount.")
    else:
        expenses.append({
            "amount": float(amount),
            "category": custom_category.strip() or category,
            "date": date.today().isoformat()
        })

        save_expenses(expenses)
        st.sidebar.success("Expense added!")
        st.rerun()

# DataFrame
df = pd.DataFrame(expenses)

if df.empty:
    st.info("No expenses yet. Add your first expense!")
    st.stop()

df["amount"] = pd.to_numeric(df["amount"])
df["date"] = pd.to_datetime(df["date"])

# Filters
st.sidebar.header("🔎 Filters")

categories = ["All"] + sorted(df["category"].unique().tolist())

selected_category = st.sidebar.selectbox(
    "Filter Category", categories
)

if selected_category != "All":
    df = df[df["category"] == selected_category]

# Dashboard metrics
total = df["amount"].sum()
transactions = len(df)
average = total / transactions
top_category = (
    df.groupby("category")["amount"].sum().idxmax()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Spending", f"₹{total:,.2f}")
c2.metric("🧾 Transactions", transactions)
c3.metric("📊 Average Expense", f"₹{average:,.2f}")
c4.metric("🏆 Top Category", top_category)

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("🥧 Category Breakdown")

    category_data = df.groupby("category")["amount"].sum().reset_index()

    fig_pie = px.pie(
        category_data,
        values="amount",
        names="category",
        hole=0.45
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with right:
    st.subheader("📅 Monthly Spending")

    df["month"] = df["date"].dt.strftime("%b %Y")

    monthly_data = df.groupby("month")["amount"].sum().reset_index()

    monthly_data["sort"] = pd.to_datetime(
        monthly_data["month"], format="%b %Y"
    )

    monthly_data = monthly_data.sort_values("sort")

    fig_bar = px.bar(
        monthly_data,
        x="month",
        y="amount",
        text_auto=True
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# Line chart
st.subheader("📈 Daily Spending Trend")

daily_data = df.groupby(
    df["date"].dt.date
)["amount"].sum().reset_index()

daily_data.columns = ["Date", "Amount"]

fig_line = px.line(
    daily_data,
    x="Date",
    y="Amount",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

# Expense history
st.subheader("🧾 Expense History")

history = df.sort_values("date", ascending=False)

st.dataframe(
    history[["date", "category", "amount"]],
    use_container_width=True,
    hide_index=True
)
