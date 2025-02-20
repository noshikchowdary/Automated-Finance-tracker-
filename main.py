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
            st.write('Categorized data:')
            st.dataframe(df.head())
    except Exception as e:
        st.error(f'Error reading or cleaning CSV: {e}')
