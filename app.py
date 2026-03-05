from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import database as db
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
db.initialize_database()

# Middleware to check login
def login_required(f):
    """Decorator to check if user is logged in"""
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """Redirect to dashboard if logged in, otherwise to login"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (for demo purposes)
        if username == 'demo' and password == 'password123':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Use demo/password123'
            return render_template('login.html', error=error)
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page with metrics and recent transactions"""
    total_expenses = db.get_total_expenses()
    todays_spending = db.get_todays_spending()
    monthly_spending = db.get_monthly_spending()
    transaction_count = db.get_transaction_count()
    recent_expenses = db.get_recent_expenses(5)
    insights = db.get_spending_insights()
    
    return render_template('dashboard.html',
                         username=session.get('username'),
                         total_expenses=total_expenses,
                         todays_spending=todays_spending,
                         monthly_spending=monthly_spending,
                         transaction_count=transaction_count,
                         recent_expenses=recent_expenses,
                         insights=insights)

@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add expense page"""
    if request.method == 'POST':
        date = request.form.get('date')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        description = request.form.get('description')
        
        db.add_expense(date, category, amount, description)
        
        return render_template('add_expense.html', success=True)
    
    return render_template('add_expense.html')

@app.route('/view-expenses')
@login_required
def view_expenses():
    """View all expenses"""
    expenses = db.get_all_expenses()
    total = db.get_total_expenses()
    
    expenses_list = [
        {
            'id': exp[0],
            'date': exp[1],
            'category': exp[2],
            'amount': exp[3],
            'description': exp[4]
        }
        for exp in expenses
    ]
    
    return render_template('view_expenses.html',
                         expenses=expenses_list,
                         total=total)

@app.route('/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    success = db.delete_expense(expense_id)
    if success:
        return jsonify({'success': True, 'message': 'Expense deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete expense'}), 500

@app.route('/analysis')
@login_required
def analysis():
    """Analysis page with charts"""
    category_breakdown = db.get_category_breakdown()
    monthly_breakdown = db.get_monthly_breakdown()
    suggestions = db.get_smart_suggestions()
    
    # Prepare category data for pie chart
    categories = [item[0] for item in category_breakdown]
    category_amounts = [item[1] for item in category_breakdown]
    
    # Prepare monthly data for bar chart (reverse for chronological order)
    monthly_breakdown_reversed = list(reversed(monthly_breakdown))
    months = [item[0] for item in monthly_breakdown_reversed]
    monthly_amounts = [item[1] for item in monthly_breakdown_reversed]
    
    # Generate spending trend for line chart
    all_expenses = db.get_all_expenses()
    daily_spending = {}
    for exp in all_expenses:
        date = exp[1]
        amount = exp[3]
        daily_spending[date] = daily_spending.get(date, 0) + amount
    
    sorted_dates = sorted(daily_spending.keys())
    trend_dates = sorted_dates[-30:] if len(sorted_dates) > 30 else sorted_dates
    trend_amounts = [daily_spending[date] for date in trend_dates]
    
    return render_template('analysis.html',
                         categories=categories,
                         category_amounts=category_amounts,
                         months=months,
                         monthly_amounts=monthly_amounts,
                         trend_dates=trend_dates,
                         trend_amounts=trend_amounts,
                         suggestions=suggestions)

@app.route('/api/expenses')
@login_required
def get_expenses_api():
    """API endpoint for getting expenses as JSON"""
    expenses = db.get_all_expenses()
    expenses_list = [
        {
            'id': exp[0],
            'date': exp[1],
            'category': exp[2],
            'amount': exp[3],
            'description': exp[4]
        }
        for exp in expenses
    ]
    return jsonify(expenses_list)

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
