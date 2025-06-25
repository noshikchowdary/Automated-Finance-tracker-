import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration
class Config:
    PAGE_TITLE = "Personal Finance Dashboard"
    PAGE_ICON = "📈"
    # Allow override of category file via environment variable
    CATEGORY_FILE = Path(os.environ.get("CATEGORY_FILE", "categories.json"))
    DEFAULT_CATEGORIES = {
        "Food & Dining": ["restaurant", "grocery", "food", "cafe", "pizza"],
        "Transportation": ["uber", "taxi", "gas", "fuel", "parking"],
        "Shopping": ["amazon", "store", "retail", "clothing"],
        "Utilities": ["electric", "water", "internet", "phone"],
        "Entertainment": ["netflix", "spotify", "movie", "concert"],
        "Healthcare": ["pharmacy", "doctor", "hospital", "medical"],
        "Uncategorized": [],
    }


class CategoryManager:
    """Handles category management and transaction categorization"""

    def __init__(self):
        self.categories = self._load_categories()

    def _load_categories(self) -> Dict[str, List[str]]:
        """Load categories from file or use defaults"""
        try:
            if Config.CATEGORY_FILE.exists():
                with open(Config.CATEGORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.warning(f"Could not load categories: {e}")

        return Config.DEFAULT_CATEGORIES.copy()

    def save_categories(self) -> bool:
        """Save categories to file"""
        try:
            with open(Config.CATEGORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.categories, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save categories: {e}")
            return False

    def add_category(self, category_name: str) -> bool:
        """Add a new category with improved error feedback"""
        category_name = category_name.strip()
        if not category_name:
            st.warning("Category name cannot be empty.")
            return False
        if category_name in self.categories:
            st.warning(f"Category '{category_name}' already exists.")
            return False
        self.categories[category_name] = []
        logger.info(f"Category added: {category_name}")
        return self.save_categories()

    def add_keyword(self, category: str, keyword: str) -> bool:
        """Add keyword to category with improved error feedback"""
        keyword = keyword.strip().lower()
        if not keyword:
            st.warning("Keyword cannot be empty.")
            return False
        if category not in self.categories:
            st.warning(f"Category '{category}' does not exist.")
            return False
        if keyword in self.categories[category]:
            st.warning(f"Keyword '{keyword}' already exists in '{category}'.")
            return False
        self.categories[category].append(keyword)
        logger.info(f"Keyword '{keyword}' added to category '{category}'")
        return self.save_categories()

    def categorize_transaction(self, description: str) -> str:
        """Categorize a single transaction based on description"""
        description_lower = description.lower()

        for category, keywords in self.categories.items():
            if category == "Uncategorized":
                continue

            if any(keyword in description_lower for keyword in keywords):
                return category

        return "Uncategorized"


class DataProcessor:
    """Handles data loading and processing"""

    @staticmethod
    def load_csv(file) -> Optional[pd.DataFrame]:
        """Load and validate CSV file with robust error handling"""
        # Check for empty file
        if hasattr(file, "getbuffer") and file.getbuffer().nbytes == 0:
            st.error("Uploaded file is empty. Please upload a valid CSV file.")
            return None
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            logger.info(
                f"File uploaded and parsed successfully: {getattr(file, 'name', str(file))}"
            )
        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file is empty. Please select a file with data.")
            return None
        except UnicodeDecodeError:
            st.error("File encoding error: Please upload a UTF-8 encoded CSV file.")
            return None
        except pd.errors.ParserError:
            st.error(
                "Parsing error: The CSV file appears to be malformed or corrupted."
            )
            return None
        except Exception as e:
            st.error(f"Unexpected error loading file: {str(e)}")
            return None

        # Validate required columns
        required_cols = ["Date", "Details", "Amount", "Debit/Credit"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            return None

        # Clean and convert data
        try:
            df["Amount"] = pd.to_numeric(
                df["Amount"].astype(str).str.replace(",", ""), errors="coerce"
            )
            df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors="coerce")
        except Exception as e:
            st.error(f"Data conversion error: {str(e)}")
            return None

        # Remove rows with invalid data
        invalid_rows = df[df["Amount"].isna() | df["Date"].isna()]
        if not invalid_rows.empty:
            st.warning(
                f"{len(invalid_rows)} rows were removed due to invalid date or amount."
            )
        df = df.dropna(subset=["Date", "Amount"])

        return df

    @staticmethod
    def apply_categorization(
        df: pd.DataFrame, category_manager: CategoryManager
    ) -> pd.DataFrame:
        """Apply categorization to dataframe"""
        df = df.copy()
        df["Category"] = df["Details"].apply(category_manager.categorize_transaction)
        return df


class FinanceDashboard:
    """Main dashboard class"""

    def __init__(self):
        self.category_manager = CategoryManager()
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize Streamlit session state"""
        if "categories" not in st.session_state:
            st.session_state.categories = self.category_manager.categories
        else:
            self.category_manager.categories = st.session_state.categories

    def render_header(self):
        """Render dashboard header"""
        st.title("📊 Personal Finance Dashboard")
        st.markdown(
            """
        **Upload your bank statement CSV to analyze your spending patterns and manage categories.**
        
        *Expected CSV format: Date, Details, Amount, Debit/Credit*
        """
        )

    def render_file_upload(self) -> Optional[pd.DataFrame]:
        """Render file upload section"""
        uploaded_file = st.file_uploader(
            "Upload Bank Statement (CSV)",
            type=["csv"],
            help="Upload a CSV file with columns: Date, Details, Amount, Debit/Credit",
        )

        if uploaded_file:
            with st.spinner("Loading transactions..."):
                df = DataProcessor.load_csv(uploaded_file)
                if df is not None:
                    df = DataProcessor.apply_categorization(df, self.category_manager)
                    return df

        return None

    def render_category_management(self):
        """Render category management section"""
        with st.expander("🏷️ Manage Categories", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                new_category = st.text_input(
                    "New Category Name", placeholder="e.g., Subscriptions"
                )

            with col2:
                if st.button("Add Category", type="primary"):
                    if new_category and self.category_manager.add_category(
                        new_category
                    ):
                        st.session_state.categories = self.category_manager.categories
                        st.success(f"✅ Added '{new_category}'")
                        st.rerun()
                    elif new_category:
                        st.warning("Category already exists or invalid name")

            # Display current categories
            if st.checkbox("Show Current Categories"):
                for cat, keywords in self.category_manager.categories.items():
                    if keywords:
                        st.write(f"**{cat}:** {', '.join(keywords)}")

    def render_expense_analysis(self, expenses_df: pd.DataFrame):
        """Render expense analysis section"""
        st.subheader("💸 Expense Analysis")

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Expenses", f"${expenses_df['Amount'].sum():,.2f}")
        with col2:
            st.metric("Transactions", len(expenses_df))
        with col3:
            avg_expense = expenses_df["Amount"].mean()
            st.metric("Average Transaction", f"${avg_expense:.2f}")

        # Interactive data editor
        st.subheader("📝 Edit Categories")

        edited_df = st.data_editor(
            expenses_df[["Date", "Details", "Amount", "Category"]].copy(),
            column_config={
                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "Category": st.column_config.SelectboxColumn(
                    "Category",
                    options=list(self.category_manager.categories.keys()),
                    required=True,
                ),
            },
            hide_index=True,
            use_container_width=True,
            key="expense_editor",
        )

        # Save changes
        if st.button("💾 Save Changes", type="primary"):
            self._save_categorization_changes(expenses_df, edited_df)

        # Charts
        self._render_expense_charts(expenses_df)

    def _save_categorization_changes(
        self, original_df: pd.DataFrame, edited_df: pd.DataFrame
    ):
        """Save categorization changes and learn from them"""
        changes_made = 0

        for idx, row in edited_df.iterrows():
            if idx < len(original_df):
                new_category = row["Category"]
                old_category = original_df.iloc[idx]["Category"]

                if new_category != old_category:
                    # Update the category
                    original_df.iloc[idx, original_df.columns.get_loc("Category")] = (
                        new_category
                    )

                    # Learn from the change by adding the description as a keyword
                    detail = row["Details"]
                    self.category_manager.add_keyword(new_category, detail)
                    changes_made += 1

        if changes_made > 0:
            st.session_state.categories = self.category_manager.categories
            st.success(f"✅ Saved {changes_made} changes and learned new patterns!")
            st.rerun()
        else:
            st.info("No changes detected.")

    def _render_expense_charts(self, expenses_df: pd.DataFrame):
        """Render expense visualization charts"""
        if expenses_df.empty:
            st.warning("No expense data to display")
            return

        # Category summary
        category_summary = (
            expenses_df.groupby("Category")["Amount"]
            .agg(["sum", "count"])
            .reset_index()
            .sort_values("sum", ascending=False)
        )
        category_summary.columns = ["Category", "Total Amount", "Transaction Count"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Spending by Category")
            st.dataframe(
                category_summary.style.format({"Total Amount": "${:,.2f}"}),
                use_container_width=True,
            )

        with col2:
            # Pie chart
            fig_pie = px.pie(
                category_summary,
                values="Total Amount",
                names="Category",
                title="Expense Distribution",
                hole=0.4,
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)

        # Time series analysis
        if len(expenses_df) > 1:
            st.subheader("📈 Spending Over Time")

            daily_expenses = (
                expenses_df.groupby([expenses_df["Date"].dt.date, "Category"])["Amount"]
                .sum()
                .reset_index()
            )

            fig_time = px.line(
                daily_expenses,
                x="Date",
                y="Amount",
                color="Category",
                title="Daily Spending by Category",
            )
            st.plotly_chart(fig_time, use_container_width=True)

    def render_income_analysis(self, income_df: pd.DataFrame):
        """Render income analysis section"""
        st.subheader("💰 Income Analysis")

        if income_df.empty:
            st.info("No income transactions found.")
            return

        # Key metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Income", f"${income_df['Amount'].sum():,.2f}")
        with col2:
            st.metric("Income Sources", len(income_df))

        # Income details
        st.dataframe(
            income_df[["Date", "Details", "Amount"]].sort_values(
                "Date", ascending=False
            ),
            use_container_width=True,
        )

    def render_summary(self, expenses_df: pd.DataFrame, income_df: pd.DataFrame):
        """Render high-level financial summary"""
        st.subheader("📈 Financial Summary")
        total_income = income_df["Amount"].sum() if not income_df.empty else 0
        total_expenses = expenses_df["Amount"].sum() if not expenses_df.empty else 0
        net_income = total_income - total_expenses

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")
        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")
        with col3:
            delta_color = "normal" if net_income >= 0 else "inverse"
            st.metric(
                "Net Income",
                f"${net_income:,.2f}",
                delta=f"${net_income:,.2f}",
                delta_color=delta_color,
            )

        # Top 3 categories by spend
        st.markdown("**Top 3 Expense Categories**")
        if not expenses_df.empty:
            top_cats = (
                expenses_df.groupby("Category")["Amount"]
                .sum()
                .sort_values(ascending=False)
                .head(3)
                .reset_index()
            )
            st.table(top_cats.rename(columns={"Amount": "Total Spent"}))
        else:
            st.info("No expense data available.")

        # 5 most recent transactions
        st.markdown("**5 Most Recent Transactions**")
        if not expenses_df.empty or not income_df.empty:
            all_tx = pd.concat([expenses_df, income_df]).sort_values(
                "Date", ascending=False
            )
            st.dataframe(
                all_tx[["Date", "Details", "Amount", "Debit/Credit", "Category"]].head(
                    5
                ),
                use_container_width=True,
            )
        else:
            st.info("No transactions available.")

    def run(self):
        """Main application entry point"""
        st.set_page_config(
            page_title=Config.PAGE_TITLE,
            page_icon=Config.PAGE_ICON,
            layout="wide",
            initial_sidebar_state="collapsed",
        )

        self.render_header()
        self.render_category_management()

        # Load data
        df = self.render_file_upload()

        if df is not None and not df.empty:
            # Split data
            expenses_df = df[df["Debit/Credit"] == "Debit"].copy()
            income_df = df[df["Debit/Credit"] == "Credit"].copy()

            # Create tabs (Summary, Expenses, Income, Overview)
            tab_summary, tab1, tab2, tab3 = st.tabs(
                ["📈 Summary", "💸 Expenses", "💰 Income", "📊 Overview"]
            )

            with tab_summary:
                self.render_summary(expenses_df, income_df)
            with tab1:
                self.render_expense_analysis(expenses_df)
            with tab2:
                self.render_income_analysis(income_df)
            with tab3:
                self.render_overview(expenses_df, income_df)

    def render_overview(self, expenses_df: pd.DataFrame, income_df: pd.DataFrame):
        """Render financial overview"""
        st.subheader("📊 Financial Overview")

        total_income = income_df["Amount"].sum() if not income_df.empty else 0
        total_expenses = expenses_df["Amount"].sum() if not expenses_df.empty else 0
        net_income = total_income - total_expenses

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")

        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")

        with col3:
            delta_color = "normal" if net_income >= 0 else "inverse"
            st.metric(
                "Net Income",
                f"${net_income:,.2f}",
                delta=f"${net_income:,.2f}",
                delta_color=delta_color,
            )


def main():
    """Application entry point"""
    try:
        dashboard = FinanceDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
