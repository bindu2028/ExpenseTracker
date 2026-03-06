from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, Response
from datetime import datetime, timedelta
import database as db
import os
import csv
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'receipts'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)

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
    """Landing page showing app features with signup/login options"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate user credentials from database
        is_valid, user_data = db.validate_user(username, password)
        
        if is_valid:
            session['username'] = user_data['username']
            session['user_id'] = user_data['id']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            return render_template('signup.html', error='All fields are required')
        
        if len(username) < 3:
            return render_template('signup.html', error='Username must be at least 3 characters')
        
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        # Create user
        success, message = db.create_user(username, email, password)
        
        if success:
            return render_template('signup.html', success=True)
        else:
            return render_template('signup.html', error=message)
    
    return render_template('signup.html')


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
    net_balance = db.get_net_balance()
    budgets = db.get_budgets(session.get('user_id'))
    
    # Get user theme
    profile = db.get_user_profile(session.get('user_id'))
    if profile:
        session['theme'] = profile.get('theme', 'light')
    
    return render_template('dashboard.html',
                         username=session.get('username'),
                         total_expenses=total_expenses,
                         todays_spending=todays_spending,
                         monthly_spending=monthly_spending,
                         transaction_count=transaction_count,
                         recent_expenses=recent_expenses,
                         insights=insights,
                         net_balance=net_balance,
                         budgets=budgets,
                         theme=session.get('theme', 'light'))

@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add expense page"""
    categories = db.get_categories(session.get('user_id'))
    
    if request.method == 'POST':
        date = request.form.get('date')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        description = request.form.get('description')
        notes = request.form.get('notes', '')
        tags = request.form.get('tags', '')
        
        # Handle receipt upload
        receipt_path = None
        if 'receipt' in request.files:
            receipt = request.files['receipt']
            if receipt.filename:
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{receipt.filename}"
                receipt_path = os.path.join('receipts', filename)
                receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], receipt_path))
        
        db.add_expense_full(date, category, amount, description, notes, tags, receipt_path, session.get('user_id'))
        
        return render_template('add_expense.html', success=True, categories=categories)
    
    return render_template('add_expense.html', categories=categories)

@app.route('/view-expenses')
@login_required
def view_expenses():
    """View all expenses with search and filter"""
    # Get filter parameters
    search = request.args.get('search', '')
    filter_category = request.args.get('category', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    min_amount = request.args.get('min_amount', '')
    max_amount = request.args.get('max_amount', '')
    filter_tags = request.args.get('tags', '')
    
    # Apply filters
    if any([search, filter_category, start_date, end_date, min_amount, max_amount, filter_tags]):
        expenses = db.search_expenses(
            query=search or None,
            category=filter_category or None,
            start_date=start_date or None,
            end_date=end_date or None,
            min_amount=float(min_amount) if min_amount else None,
            max_amount=float(max_amount) if max_amount else None,
            tags=filter_tags or None
        )
    else:
        expenses = db.get_all_expenses()
    
    total = db.get_total_expenses()
    categories = db.get_categories(session.get('user_id'))
    
    expenses_list = [
        {
            'id': exp[0],
            'date': exp[1],
            'category': exp[2],
            'amount': exp[3],
            'description': exp[4],
            'notes': exp[5] if len(exp) > 5 else '',
            'tags': exp[6] if len(exp) > 6 else '',
            'receipt_path': exp[7] if len(exp) > 7 else None
        }
        for exp in expenses
    ]
    
    return render_template('view_expenses.html',
                         expenses=expenses_list,
                         total=total,
                         categories=categories,
                         search=search,
                         filter_category=filter_category,
                         start_date=start_date,
                         end_date=end_date,
                         min_amount=min_amount,
                         max_amount=max_amount,
                         filter_tags=filter_tags)

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


# ============== BUDGET ROUTES ==============

@app.route('/budgets')
@login_required
def budgets():
    """Budget goals page"""
    budgets_list = db.get_budgets(session.get('user_id'))
    categories = db.get_categories(session.get('user_id'))
    return render_template('budgets.html', budgets=budgets_list, categories=categories)


@app.route('/add-budget', methods=['POST'])
@login_required
def add_budget():
    """Add or update a budget"""
    category = request.form.get('category')
    limit = float(request.form.get('limit'))
    
    db.set_budget(session.get('user_id'), category, limit)
    return redirect(url_for('budgets'))


@app.route('/delete-budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    """Delete a budget"""
    db.delete_budget(budget_id)
    return jsonify({'success': True})


# ============== INCOME ROUTES ==============

@app.route('/income')
@login_required
def income():
    """Income tracking page"""
    income_list = db.get_all_income(session.get('user_id'))
    total_income = db.get_total_income()
    monthly_income = db.get_monthly_income()
    net_balance = db.get_net_balance()
    
    income_data = [
        {
            'id': inc[0],
            'date': inc[1],
            'source': inc[2],
            'amount': inc[3],
            'description': inc[4],
            'is_recurring': inc[5]
        }
        for inc in income_list
    ]
    
    return render_template('income.html',
                         income_list=income_data,
                         total_income=total_income,
                         monthly_income=monthly_income,
                         net_balance=net_balance)


@app.route('/add-income', methods=['POST'])
@login_required
def add_income():
    """Add income entry"""
    date = request.form.get('date')
    source = request.form.get('source')
    amount = float(request.form.get('amount'))
    description = request.form.get('description', '')
    is_recurring = 1 if request.form.get('is_recurring') else 0
    
    db.add_income(session.get('user_id'), date, source, amount, description, is_recurring)
    return redirect(url_for('income'))


@app.route('/delete-income/<int:income_id>', methods=['POST'])
@login_required
def delete_income(income_id):
    """Delete income entry"""
    db.delete_income(income_id)
    return jsonify({'success': True})


# ============== CATEGORY ROUTES ==============

@app.route('/categories')
@login_required
def categories():
    """Custom categories page"""
    categories_list = db.get_categories(session.get('user_id'))
    return render_template('categories.html', categories=categories_list)


@app.route('/add-category', methods=['POST'])
@login_required
def add_category():
    """Add custom category"""
    name = request.form.get('name')
    icon = request.form.get('icon', '📁')
    color = request.form.get('color', '#667eea')
    
    success, message = db.add_category(session.get('user_id'), name, icon, color)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': success, 'message': message})
    return redirect(url_for('categories'))


@app.route('/delete-category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete custom category"""
    db.delete_category(category_id)
    return jsonify({'success': True})


# ============== SETTINGS/PROFILE ROUTES ==============

@app.route('/settings')
@login_required
def settings():
    """User settings page"""
    profile = db.get_user_profile(session.get('user_id'))
    return render_template('settings.html', profile=profile)


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    email = request.form.get('email')
    theme = request.form.get('theme')
    
    db.update_user_profile(session.get('user_id'), email=email, theme=theme)
    
    # Update session theme
    if theme:
        session['theme'] = theme
    
    return redirect(url_for('settings'))


@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        profile = db.get_user_profile(session.get('user_id'))
        return render_template('settings.html', profile=profile, error='New passwords do not match')
    
    if len(new_password) < 6:
        profile = db.get_user_profile(session.get('user_id'))
        return render_template('settings.html', profile=profile, error='Password must be at least 6 characters')
    
    success, message = db.change_password(session.get('user_id'), old_password, new_password)
    profile = db.get_user_profile(session.get('user_id'))
    
    if success:
        return render_template('settings.html', profile=profile, success=message)
    return render_template('settings.html', profile=profile, error=message)


@app.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    """Upload profile picture"""
    if 'picture' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    picture = request.files['picture']
    if picture.filename:
        filename = f"profile_{session.get('user_id')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{picture.filename.rsplit('.', 1)[-1]}"
        picture_path = os.path.join('profiles', filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_path))
        
        db.update_profile_picture(session.get('user_id'), picture_path)
        return jsonify({'success': True, 'path': picture_path})
    
    return jsonify({'success': False, 'message': 'Invalid file'})


@app.route('/toggle-theme', methods=['POST'])
@login_required
def toggle_theme():
    """Toggle dark/light theme"""
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    
    session['theme'] = new_theme
    db.update_user_profile(session.get('user_id'), theme=new_theme)
    
    return jsonify({'success': True, 'theme': new_theme})


# ============== EXPORT ROUTES ==============

@app.route('/export/csv')
@login_required
def export_csv():
    """Export expenses as CSV"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    expenses = db.get_expenses_for_export(start_date, end_date, category)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Category', 'Amount', 'Description', 'Notes', 'Tags'])
    
    for exp in expenses:
        writer.writerow([exp['date'], exp['category'], exp['amount'], 
                        exp['description'], exp['notes'], exp['tags']])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename=expenses_{datetime.now().strftime("%Y%m%d")}.csv'}
    )


@app.route('/export/pdf')
@login_required
def export_pdf():
    """Export expenses as PDF (simplified HTML for printing)"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    expenses = db.get_expenses_for_export(start_date, end_date, category)
    total_expenses = sum(exp['amount'] for exp in expenses)
    total_income = db.get_total_income()
    net_balance = total_income - total_expenses
    
    # Get category totals
    category_totals = {}
    for exp in expenses:
        cat = exp['category']
        category_totals[cat] = category_totals.get(cat, 0) + exp['amount']
    category_totals_list = [{'category': k, 'total': v} for k, v in category_totals.items()]
    
    return render_template('export_pdf.html', 
                         expenses=expenses, 
                         total_expenses=total_expenses,
                         total_income=total_income,
                         net_balance=net_balance,
                         category_totals=category_totals_list,
                         current_date=datetime.now().strftime('%Y-%m-%d'),
                         current_year=datetime.now().year,
                         username=session.get('username'))


# ============== RECEIPT ROUTES ==============

@app.route('/upload-receipt/<int:expense_id>', methods=['POST'])
@login_required
def upload_receipt(expense_id):
    """Upload receipt for an expense"""
    if 'receipt' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    receipt = request.files['receipt']
    if receipt.filename:
        filename = f"receipt_{expense_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{receipt.filename.rsplit('.', 1)[-1]}"
        receipt_path = os.path.join('receipts', filename)
        receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], receipt_path))
        
        db.add_receipt_to_expense(expense_id, receipt_path)
        return jsonify({'success': True, 'path': receipt_path})
    
    return jsonify({'success': False, 'message': 'Invalid file'})


@app.route('/view-receipt/<int:expense_id>')
@login_required
def view_receipt(expense_id):
    """View receipt for an expense"""
    receipt_path = db.get_expense_receipt(expense_id)
    if receipt_path:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], receipt_path))
    return jsonify({'error': 'No receipt found'}), 404

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
