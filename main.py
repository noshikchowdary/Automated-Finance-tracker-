import streamlit as st
import pandas as pd

st.title('Personal Finance Dashboard')
st.write('Upload your bank statement as a CSV file.')

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
            st.write('Cleaned and validated data:')
            st.dataframe(df.head())
    except Exception as e:
        st.error(f'Error reading or cleaning CSV: {e}')
