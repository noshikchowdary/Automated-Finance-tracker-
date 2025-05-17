Personal Finance Dashboard

A simple and interactive web application built with Streamlit to help you analyze and categorize your personal finance transactions from your bank statements.

Features

Upload bank statement CSV files easily.
Automatically categorize transactions based on user-defined keywords.
Create, edit, and manage custom expense categories.
Visualize expenses by category with interactive pie charts.
View detailed expenses and income transactions.
Save category keywords persistently in a JSON file.
User-friendly interface with editable transaction tables.
How It Works

Upload CSV: Upload your bank statement in CSV format with columns like Date, Details, Amount, and Debit/Credit.
Auto-categorization: Transactions are auto-categorized by matching keywords in the transaction details.
Edit Categories: Add new categories or update existing ones directly from the app.
Expense Management: View and edit categorized expense transactions.
Summary & Visualization: See total expenses grouped by category and visualize them with a pie chart.
Income Tab: View total income and detailed income transactions.
Getting Started

Prerequisites
Python 3.8+
Install required libraries:
pip install streamlit pandas plotly
Running the App
Clone the repository:
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Run the Streamlit app:
streamlit run app.py
Open the link provided in the terminal (usually http://localhost:8501) in your web browser.
File Structure

app.py — Main Streamlit app file.
categories.json — Stores user-defined categories and keywords persistently.
README.md — Project overview and instructions.
CSV Format Requirements

Your CSV file should contain the following columns (case-insensitive):

Date — Transaction date, formatted like 01 Jan 2023.
Details — Description of the transaction.
Amount — Amount of money involved (can include commas).
Debit/Credit — Specify if the transaction is a debit or credit.
Customization

Modify or add categories in the app interface.
Keywords for auto-categorization can be edited and saved dynamically.
Supports unlimited categories and keywords.
Future Improvements

Support for multiple file formats (Excel, OFX).
Enhanced visualization (time series, monthly trends).
Export categorized transactions.
User authentication for personalized experiences.
