import streamlit as st
import pandas as pd

st.title('Personal Finance Dashboard')
st.write('Upload your bank statement as a CSV file.')

uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.write('Preview of uploaded data:')
        st.dataframe(df.head())
    except Exception as e:
        st.error(f'Error reading CSV: {e}')
