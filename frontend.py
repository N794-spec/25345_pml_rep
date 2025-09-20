# frontend_fin.py
import streamlit as st
import pandas as pd
from datetime import datetime
# Import all necessary functions from the backend
import backend_fin as be

st.set_page_config(page_title="Financial Transaction Manager", layout="wide")

# Initialize the database on first run
be.init_db()

# --- App Title ---
st.title("💰 Financial Transaction Manager")
st.markdown("An expert-level application for tracking income and expenses.")

# --- Input Form ---
st.header("Add a New Transaction")
categories = ['Salary', 'Groceries', 'Rent', 'Utilities', 'Entertainment', 'Investment', 'Other']
with st.form("transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.now())
        category = st.selectbox("Category", categories)
        transaction_type = st.radio("Type", ('Income', 'Expense'))
    with col2:
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")

    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if not description:
            st.error("Description cannot be empty.")
        else:
            be.add_transaction(date, description, category, amount, transaction_type)
            st.success("Transaction added successfully! 🎉")

st.markdown("---")

# --- Business Insights Section ---
st.header("📊 Business Insights")
insights = be.get_business_insights()

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{insights['total_income']:.2f}", delta_color="normal")
col2.metric("Total Expense", f"₹{insights['total_expense']:.2f}", delta_color="inverse")
col3.metric("Net Savings", f"₹{insights['net_savings']:.2f}", f"₹{insights['net_savings'] - insights['total_income']:.2f}")

with st.expander("View Detailed Analytics"):
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Transactions", insights['total_transactions'])
    m2.metric("Average Transaction", f"₹{insights.get('average_transaction_amount', 0):.2f}")
    m3.metric("Highest Transaction", f"₹{insights.get('max_transaction_amount', 0):.2f}")
    m4.metric("Lowest Transaction", f"₹{insights.get('min_transaction_amount', 0):.2f}")

st.markdown("---")

# --- Data Display and Deletion Section ---
st.header("📋 All Transactions")
all_transactions = be.get_all_transactions()

if not all_transactions.empty:
    # Add a 'delete' column with buttons
    all_transactions['delete'] = [st.button(f"Delete", key=f"del_{i}") for i in all_transactions['id']]
    
    st.dataframe(all_transactions.drop(columns=['delete']), use_container_width=True)

    # Check if any delete button was pressed
    for index, row in all_transactions.iterrows():
        if row['delete']:
            be.delete_transaction(row['id'])
            st.toast(f"Deleted transaction ID: {row['id']}")
            st.rerun() # Rerun the app to refresh the data
else:
    st.info("No transactions found. Add one using the form above.")