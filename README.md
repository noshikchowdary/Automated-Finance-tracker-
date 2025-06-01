# 📊 Personal Finance Dashboard

A simple and powerful Streamlit app that lets users visualize, categorize, and analyze their personal financial transactions using uploaded bank statements.

---

## 🚀 Features

- ✅ Upload CSV bank statements for quick parsing
- 🏷️ Auto-categorize expenses based on keywords
- ✍️ Manually edit and save transaction categories
- 📊 Pie charts and tables for spending insights
- 💾 Category memory stored locally (JSON)
- 📁 Built using Streamlit, pandas, and Plotly

---


## 🧠 How It Works

1. Upload a `.csv` bank statement.
2. The app automatically separates **Debits** and **Credits**.
3. Expenses are auto-tagged into categories based on keyword matching.
4. Users can:
   - Add custom categories
   - Assign transactions to categories manually
   - Visualize spending in a pie chart

---

## 💼 Why This Project?

This dashboard mimics how real-world finance tools work — automating ETL-like parsing, categorization logic, and data visualization.

It showcases:
- Practical **data cleaning & transformation**
- Custom **rule-based classification logic**
- **Interactive UI** design with Streamlit
- Modern data visualization using Plotly

---

## 🛠️ Tech stack.

- `Streamlit` – for web UI
- `Pandas` – for data transformation
- `Plotly` – for rich charts
- `JSON` – for persistent category memory
- `CSV` – input data format

---

## 📁 File Structure
```bash
📦finance-dashboard
┣ 📜 app.py
┣ 📜 categories.json
┣ 📜 sample_data.csv
┗ 📜 README.md
```



---

## 📊 Sample Data Format

Make sure your CSV file includes the following columns:


- `Date`: Transaction date (e.g., `01 Jan 2024`)
- `Details`: Merchant or description
- `Amount`: Amount spent or received
- `Debit/Credit`: Type of transaction

---

## ⚙️ Run Locally

```bash
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard
pip install -r requirements.txt
streamlit run app.py


