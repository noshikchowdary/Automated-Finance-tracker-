import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Streamlit page configuration
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="📈",
    layout="wide"
)

# Constants
CATEGORY_FILE = "categories.json"

# Initialize default categories
if "categories" not in st.session_state:
    st.session_state.categories = {"Uncategorized": []}

# Load existing categories from file (if available)
if os.path.exists(CATEGORY_FILE):
    with open(CATEGORY_FILE, "r") as file:
        st.session_state.categories = json.load(file)

# Save categories to local JSON file
def save_categories():
    with open(CATEGORY_FILE, "w") as file:
        json.dump(st.session_state.categories, file, indent=4)

# Automatically assign categories based on defined keywords
def categorize_transactions(df):
    df["Category"] = "Uncategorized"
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue
        for idx, row in df.iterrows():
            if any(keyword.lower() in row["Details"].lower() for keyword in keywords):
                df.at[idx, "Category"] = category
    return df

# Load and clean uploaded CSV file
def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
        return categorize_transactions(df)
    except Exception as e:
        st.error(f"⚠️ Failed to load file: {e}")
        return None

# Add new keyword to a category
def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories.get(category, []):
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False

# Main app logic
def main():
    st.title("📊 Personal Finance Dashboard")
    st.markdown("Easily track your income and expenses by uploading your bank statement CSV.")

    uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type=["csv"])

    if uploaded_file:
        df = load_transactions(uploaded_file)

        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab1, tab2 = st.tabs(["💸 Expenses", "💰 Income"])

            # --- Expenses Tab ---
            with tab1:
                st.subheader("Manage Categories")
                new_category = st.text_input("Create New Category")
                if st.button("Add Category") and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.success(f"✅ Category '{new_category}' added!")
                        st.rerun()

                st.subheader("Edit and Categorize Expenses")

                edited_df = st.data_editor(
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="expense_editor"
                )

                if st.button("💾 Save Changes"):
                    for idx, row in edited_df.iterrows():
                        new_cat = row["Category"]
                        if new_cat != st.session_state.debits_df.at[idx, "Category"]:
                            detail = row["Details"]
                            st.session_state.debits_df.at[idx, "Category"] = new_cat
                            add_keyword_to_category(new_cat, detail)
                    st.success("✅ Changes saved!")
                    st.rerun()

                st.subheader("Expense Summary")
                summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
                summary = summary.sort_values(by="Amount", ascending=False)
                st.dataframe(summary, use_container_width=True)

                fig = px.pie(
                    summary,
                    names="Category",
                    values="Amount",
                    title="Expenses by Category",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)

            # --- Income Tab ---
            with tab2:
                st.subheader("Income Overview")
                total_income = credits_df["Amount"].sum()
                st.metric("Total Income", f"${total_income:,.2f}")
                st.dataframe(credits_df, use_container_width=True)

# Run Streamlit app
if __name__ == "__main__":
    main()
