# Automated Personal Finance Tracker

## About This Project

I built this project to automate and simplify personal finance tracking. The app lets users upload their bank statements, automatically categorizes transactions, and provides clear visualizations of spending and income trends. My goal was to create a practical, portfolio-ready tool that demonstrates my skills in data engineering, Python, and interactive dashboard development.

## Key Features
- Upload CSV bank statements for instant analysis
- Rule-based categorization of expenses and income
- Manual category and keyword management
- Summary dashboard: total income, expenses, net income, top categories, and recent transactions
- Interactive charts and tables for deep financial insights
- Persistent category memory (JSON)

## Tech Stack
- **Python**: Core language for all logic and data processing
- **Streamlit**: For building the interactive dashboard UI
- **pandas**: For data cleaning, transformation, and analysis
- **Plotly**: For modern, interactive data visualizations
- **JSON/CSV**: For persistent storage and data input

## How This Helps Users
- Instantly see where your money goes each month
- Spot trends in spending and income
- Customize categories and keywords to fit your lifestyle
- Edit and correct transaction categories with ease
- All data stays local—no cloud or third-party storage

## How to Run the App
1. **Clone the repository**
   ```bash
   git clone https://github.com/noshikchowdary/Automated-Finance-tracker-.git
   cd Automated-Finance-tracker-
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the dashboard**
   ```bash
   streamlit run main.py
   ```
4. **Upload your bank statement**
   - Use the dashboard to upload a CSV file with columns: `Date`, `Details`, `Amount`, `Debit/Credit`.
   - Explore, categorize, and visualize your transactions interactively.

## Example CSV Format
| Date        | Details           | Amount   | Debit/Credit |
|-------------|-------------------|----------|--------------|
| 01 Jan 2024 | AMAZON AE         | 120.00   | Debit        |
| 02 Jan 2024 | NETFLIX.COM       | 50.00    | Debit        |
| 03 Jan 2024 | SALARY            | 5000.00  | Credit       |

## Why I Built This
This project was a hands-on way for me to deepen my skills in data engineering, ETL, and dashboard development. It's a practical demonstration of my ability to design, implement, and document a complete data-driven application from scratch.

---

*Feel free to reach out if you have questions or want to collaborate!*


