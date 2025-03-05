import streamlit as st
import pandas as pd

st.title('Personal Finance Dashboard')
st.write('Upload your bank statement as a CSV file.')

CATEGORY_KEYWORDS = {
    'Shopping': ['amazon', 'store', 'retail'],
    'Transportation': ['uber', 'taxi', 'fuel', 'gas'],
    'Food & Dining': ['grocery', 'restaurant', 'cafe'],
    'Entertainment': ['netflix', 'movie', 'concert'],
    'Utilities': ['electric', 'water', 'internet', 'phone'],
    'Uncategorized': []
}

def categorize(details):
    details = str(details).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in details for keyword in keywords):
            return category
    return 'Uncategorized'

uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        required_cols = ['Date', 'Details', 'Amount', 'Debit/Credit']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
        else:
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date', 'Amount'])
            df['Category'] = df['Details'].apply(categorize)

            # Summary metrics
            total_income = df[df['Debit/Credit'] == 'Credit']['Amount'].sum()
            total_expenses = df[df['Debit/Credit'] == 'Debit']['Amount'].sum()
            net_income = total_income - total_expenses
            col1, col2, col3 = st.columns(3)
            col1.metric('Total Income', f"${total_income:,.2f}")
            col2.metric('Total Expenses', f"${total_expenses:,.2f}")
            col3.metric('Net Income', f"${net_income:,.2f}")

            st.write('Categorized data:')
            st.dataframe(df.head())
    except Exception as e:
        st.error(f'Error reading or cleaning CSV: {e}')
