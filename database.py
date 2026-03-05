"""
Database module for managing SQLite operations.
Handles all expense-related database interactions.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple
import pandas as pd

# Database configuration
DB_NAME = "expenses.db"


def initialize_database():
    """
    Initialize the SQLite database and create the expenses table if it doesn't exist.
    Table schema: id (primary key), date, category, amount, description, created_at
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Create expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("✓ Database initialized successfully")
    except sqlite3.Error as e:
        print(f"✗ Database initialization error: {e}")


def add_expense(date: str, category: str, amount: float, description: str) -> bool:
    """
    Add a new expense to the database.
    
    Args:
        date (str): Expense date in YYYY-MM-DD format
        category (str): Expense category
        amount (float): Expense amount
        description (str): Expense description
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        """, (date, category, float(amount), description))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error adding expense: {e}")
        return False


def delete_expense(expense_id: int) -> bool:
    """
    Delete an expense from the database.
    
    Args:
        expense_id (int): The ID of the expense to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error deleting expense: {e}")
        return False


def get_all_expenses():
    """
    Retrieve all expenses from the database.
    
    Returns:
        list: List of tuples containing all expenses sorted by date (newest first)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, date, category, amount, description, created_at
            FROM expenses
            ORDER BY date DESC
        """)
        
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    except sqlite3.Error as e:
        print(f"✗ Error retrieving expenses: {e}")
        return []


def get_expenses_by_category(category: str) -> pd.DataFrame:
    """
    Retrieve expenses for a specific category.
    
    Args:
        category (str): Category to filter by
    
    Returns:
        pd.DataFrame: DataFrame containing expenses for the specified category
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        
        query = """
            SELECT id, date, category, amount, description, created_at
            FROM expenses
            WHERE category = ?
            ORDER BY date DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(category,))
        conn.close()
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
        
        return df
    except sqlite3.Error as e:
        print(f"✗ Error retrieving expenses by category: {e}")
        return pd.DataFrame()


def get_expenses_by_date_range(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Retrieve expenses within a specific date range.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    
    Returns:
        pd.DataFrame: DataFrame containing expenses within the date range
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        
        query = """
            SELECT id, date, category, amount, description, created_at
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
        
        return df
    except sqlite3.Error as e:
        print(f"✗ Error retrieving expenses by date range: {e}")
        return pd.DataFrame()


def delete_expense(expense_id: int) -> bool:
    """
    Delete a specific expense by ID.
    
    Args:
        expense_id (int): ID of the expense to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error deleting expense: {e}")
        return False


def update_expense(expense_id: int, date: str, category: str, 
                   amount: float, description: str) -> bool:
    """
    Update an existing expense.
    
    Args:
        expense_id (int): ID of the expense to update
        date (str): Updated date
        category (str): Updated category
        amount (float): Updated amount
        description (str): Updated description
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE expenses
            SET date = ?, category = ?, amount = ?, description = ?
            WHERE id = ?
        """, (date, category, float(amount), description, expense_id))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error updating expense: {e}")
        return False


def get_total_spending() -> float:
    """
    Calculate total spending across all expenses.
    
    Returns:
        float: Total amount spent
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(amount) FROM expenses")
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] is not None else 0.0
    except sqlite3.Error as e:
        print(f"✗ Error calculating total spending: {e}")
        return 0.0


def get_spending_by_category() -> Dict[str, float]:
    """
    Get total spending for each category.
    
    Returns:
        Dict[str, float]: Dictionary with categories as keys and total amounts as values
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        
        query = """
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            return dict(zip(df['category'], df['total']))
        return {}
    except sqlite3.Error as e:
        print(f"✗ Error calculating spending by category: {e}")
        return {}


def get_expense_count() -> int:
    """
    Get the total number of expenses recorded.
    
    Returns:
        int: Total number of expenses
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM expenses")
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] is not None else 0
    except sqlite3.Error as e:
        print(f"✗ Error counting expenses: {e}")
        return 0


# ============================================================================
# MODERN FINTECH DASHBOARD FUNCTIONS
# ============================================================================

def init_db():
    """Alias for initialize_database for compatibility"""
    initialize_database()

def get_total_expenses():
    """Alias for get_total_spending"""
    return get_total_spending()

def get_transaction_count():
    """Alias for get_expense_count"""
    return get_expense_count()

def get_todays_spending():
    """Get today's total spending"""
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE date = ?', (today,))
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return 0

def get_monthly_spending():
    """Get current month's total spending"""
    from datetime import datetime
    today = datetime.now()
    month_start = today.replace(day=1).strftime('%Y-%m-%d')
    month_end = today.strftime('%Y-%m-%d')
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE date BETWEEN ? AND ?
        ''', (month_start, month_end))
        
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return 0

def get_recent_expenses(limit=5):
    """Get recent expenses"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, category, amount, description
            FROM expenses
            ORDER BY date DESC, created_at DESC
            LIMIT ?
        ''', (limit,))
        
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return []

def get_category_breakdown():
    """Get expenses grouped by category"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return []

def get_monthly_breakdown():
    """Get monthly spending for the last 6 months"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM expenses
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
            LIMIT 6
        ''')
        
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return []

def get_spending_insights():
    """Generate AI-style spending insights"""
    from datetime import datetime, timedelta
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Get average spending per category this week
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
        ''', (week_ago, today))
        
        week_data = cursor.fetchall()
        
        # Get average spending per category last week
        two_weeks_ago = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
        last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
        ''', (two_weeks_ago, last_week))
        
        last_week_data = cursor.fetchall()
        conn.close()
        
        insights = []
        
        # Compare this week vs last week
        if week_data:
            total_this_week = sum(x[1] for x in week_data)
            total_last_week = sum(x[1] for x in last_week_data) if last_week_data else total_this_week
            
            if total_last_week > 0:
                increase = ((total_this_week - total_last_week) / total_last_week) * 100
                if increase > 10:
                    insights.append(f"💡 You spent {increase:.0f}% more this week. Consider reducing expenses.")
                elif increase < -10:
                    insights.append(f"✅ Great! You spent {abs(increase):.0f}% less this week.")
            
            # Top category insight
            if week_data:
                top_cat = week_data[0]
                insights.append(f"📊 Your biggest expense category is {top_cat[0]} (₹{top_cat[1]:,.0f}).")
        
        if not insights:
            insights.append("💰 No spending data for this week yet.")
        
        return insights[:3]  # Return top 3 insights
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return []

def get_smart_suggestions():
    """Generate smart financial suggestions"""
    try:
        suggests = []
        category_breakdown = get_category_breakdown()
        monthly_total = get_monthly_spending()
        
        if monthly_total > 0:
            for category, total, count in category_breakdown:
                percentage = (total / monthly_total) * 100
                if percentage > 30:
                    savings = total * 0.1
                    suggests.append(f"🎯 Reduce {category} spending by 10% to save ₹{savings:,.0f} monthly.")
                
                if category == "Food" and total > 5000:
                    suggests.append(f"🍔 High Food expenses detected. Try meal planning to save money.")
                elif category == "Travel" and total > 3000:
                    suggests.append(f"🚗 Consider carpooling or public transport to reduce Travel costs.")
                elif category == "Shopping" and total > 2000:
                    suggests.append(f"🛍️ Set a budget for Shopping to maintain spending control.")
        
        if not suggests:
            suggests.append("💝 Keep tracking your expenses to get personalized suggestions!")
        
        return suggests[:3]  # Return top 3 suggestions
    except Exception as e:
        print(f"✗ Error: {e}")
        return []
