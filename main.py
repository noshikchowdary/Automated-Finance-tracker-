import streamlit as st
import pandas as pd
import plotly.express as px

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
        if hasattr(uploaded_file, 'getbuffer') and uploaded_file.getbuffer().nbytes == 0:
            st.error('Uploaded file is empty. Please upload a valid CSV file.')
        else:
            try:
                df = pd.read_csv(uploaded_file)
            except pd.errors.EmptyDataError:
                st.error('The uploaded CSV file is empty. Please select a file with data.')
                df = None
            except UnicodeDecodeError:
                st.error('File encoding error: Please upload a UTF-8 encoded CSV file.')
                df = None
            except pd.errors.ParserError:
                st.error('Parsing error: The CSV file appears to be malformed or corrupted.')
                df = None
            except Exception as e:
                st.error(f'Unexpected error loading file: {e}')
                df = None
            if df is not None:
                df.columns = df.columns.str.strip()
                required_cols = ['Date', 'Details', 'Amount', 'Debit/Credit']
                missing_cols = [col for col in required_cols if col not in df.columns]
                if missing_cols:
                    st.error(f"Missing required columns: {', '.join(missing_cols)}")
                else:
                    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    invalid_rows = df[df['Amount'].isna() | df['Date'].isna()]
                    if not invalid_rows.empty:
                        st.warning(f"{len(invalid_rows)} rows were removed due to invalid date or amount.")
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

                    # Category distribution visualizations
                    expense_df = df[df['Debit/Credit'] == 'Debit']
                    if not expense_df.empty:
                        cat_summary = expense_df.groupby('Category')['Amount'].sum().reset_index()
                        st.subheader('Spending by Category')
                        col4, col5 = st.columns(2)
                        with col4:
                            pie_fig = px.pie(cat_summary, values='Amount', names='Category', title='Expense Distribution')
                            st.plotly_chart(pie_fig, use_container_width=True)
                        with col5:
                            bar_fig = px.bar(cat_summary, x='Category', y='Amount', title='Expenses by Category')
                            st.plotly_chart(bar_fig, use_container_width=True)

                        # Time series visualization for monthly spend
                        expense_df['Month'] = expense_df['Date'].dt.to_period('M').astype(str)
                        monthly_summary = expense_df.groupby('Month')['Amount'].sum().reset_index()
                        st.subheader('Monthly Spend Trend')
                        line_fig = px.line(monthly_summary, x='Month', y='Amount', title='Monthly Expenses Over Time')
                        st.plotly_chart(line_fig, use_container_width=True)
    except Exception as e:
        st.error(f'Error reading or cleaning CSV: {e}')
