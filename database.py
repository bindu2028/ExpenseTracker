"""
Database module for managing SQLite operations.
Handles all expense-related database interactions.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import pandas as pd
import hashlib
import secrets

# Database configuration
DB_NAME = "expenses.db"


def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """
    Hash a password with a salt using SHA-256.
    
    Args:
        password (str): The plain text password
        salt (str): Optional salt, generates new one if not provided
    
    Returns:
        Tuple[str, str]: (hashed_password, salt)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt


def create_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    """
    Create a new user in the database.
    
    Args:
        username (str): The username
        email (str): The email address
        password (str): The plain text password
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "Email already registered"
        
        # Hash password and create user
        hashed_password, salt = hash_password(password)
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, salt)
            VALUES (?, ?, ?, ?)
        """, (username, email, hashed_password, salt))
        
        conn.commit()
        conn.close()
        return True, "Account created successfully"
    except sqlite3.Error as e:
        print(f"✗ Error creating user: {e}")
        return False, "Database error occurred"


def validate_user(username: str, password: str) -> Tuple[bool, Optional[Dict]]:
    """
    Validate user credentials.
    
    Args:
        username (str): The username
        password (str): The plain text password
    
    Returns:
        Tuple[bool, Optional[Dict]]: (is_valid, user_data)
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, salt
            FROM users WHERE username = ?
        """, (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return False, None
        
        # Verify password
        stored_hash = user[3]
        salt = user[4]
        hashed_input, _ = hash_password(password, salt)
        
        if hashed_input == stored_hash:
            return True, {"id": user[0], "username": user[1], "email": user[2]}
        return False, None
    except sqlite3.Error as e:
        print(f"✗ Error validating user: {e}")
        return False, None


def initialize_database():
    """
    Initialize the SQLite database and create tables if they don't exist.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                profile_picture TEXT DEFAULT NULL,
                theme TEXT DEFAULT 'light',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create categories table (for custom categories)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                icon TEXT DEFAULT '📁',
                color TEXT DEFAULT '#667eea',
                is_default INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Insert default categories if not exists
        cursor.execute("SELECT COUNT(*) FROM categories WHERE is_default = 1")
        if cursor.fetchone()[0] == 0:
            default_categories = [
                ('Food', '🍕', '#FF6B6B', 1),
                ('Travel', '✈️', '#4ECDC4', 1),
                ('Shopping', '🛒', '#FFE66D', 1),
                ('Bills', '📄', '#95E1D3', 1),
                ('Entertainment', '🎬', '#DDA0DD', 1),
                ('Healthcare', '🏥', '#98D8C8', 1),
                ('Education', '📚', '#F7DC6F', 1),
                ('Other', '📦', '#C7CEEA', 1)
            ]
            cursor.executemany("""
                INSERT INTO categories (name, icon, color, is_default, user_id)
                VALUES (?, ?, ?, ?, NULL)
            """, default_categories)
        
        # Create expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                notes TEXT,
                tags TEXT,
                receipt_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Create income table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                source TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                is_recurring INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Create budgets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT NOT NULL,
                monthly_limit REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
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
            SELECT id, date, category, amount, description, notes, tags, receipt_path, created_at
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


# ============== BUDGET FUNCTIONS ==============

def set_budget(user_id: int, category: str, monthly_limit: float) -> bool:
    """Set or update a budget for a category"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Check if budget exists
        cursor.execute("""
            SELECT id FROM budgets WHERE user_id = ? AND category = ?
        """, (user_id, category))
        
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE budgets SET monthly_limit = ? WHERE id = ?
            """, (monthly_limit, existing[0]))
        else:
            cursor.execute("""
                INSERT INTO budgets (user_id, category, monthly_limit)
                VALUES (?, ?, ?)
            """, (user_id, category, monthly_limit))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error setting budget: {e}")
        return False


def get_budgets(user_id: int = None) -> List[Dict]:
    """Get all budgets with current spending"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Get current month's first day
        from datetime import datetime
        first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT b.id, b.category, b.monthly_limit,
                   COALESCE(SUM(e.amount), 0) as spent
            FROM budgets b
            LEFT JOIN expenses e ON b.category = e.category 
                AND e.date BETWEEN ? AND ?
            GROUP BY b.id, b.category, b.monthly_limit
        """, (first_day, today))
        
        budgets = []
        for row in cursor.fetchall():
            spent = row[3]
            limit = row[2]
            percentage = (spent / limit * 100) if limit > 0 else 0
            budgets.append({
                'id': row[0],
                'category': row[1],
                'limit': limit,
                'spent': spent,
                'remaining': limit - spent,
                'percentage': min(percentage, 100)
            })
        
        conn.close()
        return budgets
    except sqlite3.Error as e:
        print(f"✗ Error getting budgets: {e}")
        return []


def delete_budget(budget_id: int) -> bool:
    """Delete a budget"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error deleting budget: {e}")
        return False


# ============== INCOME FUNCTIONS ==============

def add_income(user_id: int, date: str, source: str, amount: float, 
               description: str = "", is_recurring: int = 0) -> bool:
    """Add a new income entry"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO income (user_id, date, source, amount, description, is_recurring)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, date, source, amount, description, is_recurring))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error adding income: {e}")
        return False


def get_all_income(user_id: int = None) -> List[Tuple]:
    """Get all income entries"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, date, source, amount, description, is_recurring
            FROM income
            ORDER BY date DESC
        """)
        
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"✗ Error getting income: {e}")
        return []


def get_total_income() -> float:
    """Get total income"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM income")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return 0.0


def get_monthly_income() -> float:
    """Get current month's income"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        from datetime import datetime
        first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM income
            WHERE date >= ?
        """, (first_day,))
        
        total = cursor.fetchone()[0]
        conn.close()
        return total
    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        return 0.0


def delete_income(income_id: int) -> bool:
    """Delete an income entry"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error deleting income: {e}")
        return False


# ============== CATEGORY FUNCTIONS ==============

def get_categories(user_id: int = None) -> List[Dict]:
    """Get all categories (default + user custom)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, icon, color, is_default
            FROM categories
            WHERE is_default = 1 OR user_id = ?
            ORDER BY is_default DESC, name ASC
        """, (user_id,))
        
        categories = []
        for row in cursor.fetchall():
            categories.append({
                'id': row[0],
                'name': row[1],
                'icon': row[2],
                'color': row[3],
                'is_default': row[4] == 1
            })
        
        conn.close()
        return categories
    except sqlite3.Error as e:
        print(f"✗ Error getting categories: {e}")
        return []


def add_category(user_id: int, name: str, icon: str = '📁', color: str = '#667eea') -> Tuple[bool, str]:
    """Add a custom category"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Check if category exists
        cursor.execute("""
            SELECT id FROM categories 
            WHERE name = ? AND (is_default = 1 OR user_id = ?)
        """, (name, user_id))
        
        if cursor.fetchone():
            conn.close()
            return False, "Category already exists"
        
        cursor.execute("""
            INSERT INTO categories (user_id, name, icon, color, is_default)
            VALUES (?, ?, ?, ?, 0)
        """, (user_id, name, icon, color))
        
        conn.commit()
        conn.close()
        return True, "Category added successfully"
    except sqlite3.Error as e:
        print(f"✗ Error adding category: {e}")
        return False, "Database error"


def delete_category(category_id: int) -> bool:
    """Delete a custom category (not default ones)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ? AND is_default = 0", (category_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error deleting category: {e}")
        return False


# ============== PROFILE FUNCTIONS ==============

def update_user_profile(user_id: int, email: str = None, theme: str = None) -> bool:
    """Update user profile"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if email:
            updates.append("email = ?")
            values.append(email)
        if theme:
            updates.append("theme = ?")
            values.append(theme)
        
        if updates:
            values.append(user_id)
            cursor.execute(f"""
                UPDATE users SET {', '.join(updates)} WHERE id = ?
            """, values)
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error updating profile: {e}")
        return False


def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
    """Change user password"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Get current password hash and salt
        cursor.execute("""
            SELECT password_hash, salt FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            conn.close()
            return False, "User not found"
        
        # Verify old password
        stored_hash, salt = user
        old_hash, _ = hash_password(old_password, salt)
        
        if old_hash != stored_hash:
            conn.close()
            return False, "Current password is incorrect"
        
        # Set new password
        new_hash, new_salt = hash_password(new_password)
        cursor.execute("""
            UPDATE users SET password_hash = ?, salt = ? WHERE id = ?
        """, (new_hash, new_salt, user_id))
        
        conn.commit()
        conn.close()
        return True, "Password changed successfully"
    except sqlite3.Error as e:
        print(f"✗ Error changing password: {e}")
        return False, "Database error"


def get_user_profile(user_id: int) -> Optional[Dict]:
    """Get user profile info"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, profile_picture, theme, created_at
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'profile_picture': user[3],
                'theme': user[4] or 'light',
                'created_at': user[5]
            }
        return None
    except sqlite3.Error as e:
        print(f"✗ Error getting profile: {e}")
        return None


def update_profile_picture(user_id: int, picture_path: str) -> bool:
    """Update user profile picture"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (picture_path, user_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error updating profile picture: {e}")
        return False


# ============== SEARCH & FILTER FUNCTIONS ==============

def search_expenses(query: str = None, category: str = None, 
                   start_date: str = None, end_date: str = None,
                   min_amount: float = None, max_amount: float = None,
                   tags: str = None) -> List[Tuple]:
    """Search and filter expenses"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        sql = "SELECT id, date, category, amount, description, notes, tags, receipt_path FROM expenses WHERE 1=1"
        params = []
        
        if query:
            sql += " AND (description LIKE ? OR notes LIKE ? OR tags LIKE ?)"
            params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        if start_date:
            sql += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            sql += " AND date <= ?"
            params.append(end_date)
        
        if min_amount is not None:
            sql += " AND amount >= ?"
            params.append(min_amount)
        
        if max_amount is not None:
            sql += " AND amount <= ?"
            params.append(max_amount)
        
        if tags:
            sql += " AND tags LIKE ?"
            params.append(f'%{tags}%')
        
        sql += " ORDER BY date DESC"
        
        cursor.execute(sql, params)
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"✗ Error searching expenses: {e}")
        return []


# ============== EXPORT FUNCTIONS ==============

def get_expenses_for_export(start_date: str = None, end_date: str = None, 
                           category: str = None) -> List[Dict]:
    """Get expenses formatted for export"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        sql = """
            SELECT date, category, amount, description, notes, tags
            FROM expenses WHERE 1=1
        """
        params = []
        
        if start_date:
            sql += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            sql += " AND date <= ?"
            params.append(end_date)
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        sql += " ORDER BY date DESC"
        
        cursor.execute(sql, params)
        
        expenses = []
        for row in cursor.fetchall():
            expenses.append({
                'date': row[0],
                'category': row[1],
                'amount': row[2],
                'description': row[3] or '',
                'notes': row[4] or '',
                'tags': row[5] or ''
            })
        
        conn.close()
        return expenses
    except sqlite3.Error as e:
        print(f"✗ Error getting expenses for export: {e}")
        return []


# ============== RECEIPT FUNCTIONS ==============

def add_receipt_to_expense(expense_id: int, receipt_path: str) -> bool:
    """Add receipt path to an expense"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET receipt_path = ? WHERE id = ?", (receipt_path, expense_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error adding receipt: {e}")
        return False


def get_expense_receipt(expense_id: int) -> Optional[str]:
    """Get receipt path for an expense"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT receipt_path FROM expenses WHERE id = ?", (expense_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"✗ Error getting receipt: {e}")
        return None


# ============== ENHANCED EXPENSE FUNCTIONS ==============

def add_expense_full(date: str, category: str, amount: float, description: str,
                    notes: str = None, tags: str = None, receipt_path: str = None,
                    user_id: int = None) -> int:
    """Add expense with all optional fields"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO expenses (user_id, date, category, amount, description, notes, tags, receipt_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, date, category, float(amount), description, notes, tags, receipt_path))
        
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        return expense_id
    except sqlite3.Error as e:
        print(f"✗ Error adding expense: {e}")
        return None


def update_expense(expense_id: int, date: str = None, category: str = None,
                  amount: float = None, description: str = None,
                  notes: str = None, tags: str = None) -> bool:
    """Update an existing expense"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if date:
            updates.append("date = ?")
            values.append(date)
        if category:
            updates.append("category = ?")
            values.append(category)
        if amount is not None:
            updates.append("amount = ?")
            values.append(amount)
        if description is not None:
            updates.append("description = ?")
            values.append(description)
        if notes is not None:
            updates.append("notes = ?")
            values.append(notes)
        if tags is not None:
            updates.append("tags = ?")
            values.append(tags)
        
        if updates:
            values.append(expense_id)
            cursor.execute(f"""
                UPDATE expenses SET {', '.join(updates)} WHERE id = ?
            """, values)
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"✗ Error updating expense: {e}")
        return False


def get_net_balance() -> Dict:
    """Get net balance (income - expenses)"""
    try:
        total_income = get_total_income()
        total_expenses = get_total_expenses()
        monthly_income = get_monthly_income()
        monthly_expenses = get_monthly_spending()
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_balance': total_income - total_expenses,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'monthly_balance': monthly_income - monthly_expenses
        }
    except Exception as e:
        print(f"✗ Error getting net balance: {e}")
        return {
            'total_income': 0, 'total_expenses': 0, 'total_balance': 0,
            'monthly_income': 0, 'monthly_expenses': 0, 'monthly_balance': 0
        }
