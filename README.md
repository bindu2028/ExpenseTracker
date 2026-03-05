# 💰 Personal Expense Tracker

A modern, professional web application for tracking and analyzing daily expenses built with **Python** and **Flask**. This application provides a beautiful, responsive dashboard interface for recording expenses, viewing spending history, and analyzing spending patterns with interactive charts.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Framework](https://img.shields.io/badge/framework-Flask-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🌟 Features

### 📊 Dashboard
- **Key Metrics Display**: View total spending, transaction count, and average expense at a glance
- **Interactive Charts**: Pie and bar charts showing spending distribution by category
- **Recent Expenses**: Quick view of the 5 most recent transactions
- **Professional UI**: Modern gradient headers, smooth animations, and responsive design

### ➕ Add Expense
- **Simple Form Interface**: Intuitive expense entry form with real-time validation
- **Multiple Categories**: Food, Travel, Shopping, Bills, and Other
- **Date Picker**: Easy date selection for past or current expenses
- **Flexible Description**: Optional notes for expense details
- **Success Feedback**: Confirmation messages with auto-redirect

### 📋 View Expenses
- **Comprehensive Table**: All expenses displayed in a clean, organized table
- **Advanced Filtering**: Filter by category with dropdown selection
- **Flexible Sorting**: Sort by date (ascending/descending) or amount (ascending/descending)
- **Pagination**: View 5, 10, 15, 20, or all entries per page
- **Export Options**: Download expenses as CSV or Excel files
- **Delete Functionality**: Remove individual expenses with confirmation

### 📈 Analysis
- **Multiple Analysis Views**:
  - **Overview**: Pie charts and bar charts of spending distribution with summary stats
  - **By Category**: Detailed category breakdown with transaction counts
  - **By Time**: Daily expense trends with line charts
  - **Statistics**: Detailed daily and category statistics with top 10 expenses list

---

## 🎨 UI/UX Design

### Modern Features
- **Gradient Design**: Professional purple gradient theme throughout
- **Responsive Layout**: Fully responsive on desktop, tablet, and mobile
- **Card-Based Structure**: Clean cards with subtle shadows for depth
- **Color-Coded Categories**: Distinct colors for each expense category
- **Emoji Icons**: Visual indicators for better UX
- **Interactive Charts**: Chart.js powered interactive visualizations
- **Smooth Transitions**: Button hover effects and animations
- **Professional Typography**: Clear, readable fonts with proper hierarchy

### Color Scheme
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Secondary**: Teal (#4ECDC4)
- **Food**: Red (#FF6B6B)
- **Travel**: Teal (#4ECDC4)
- **Shopping**: Yellow (#FFE66D)
- **Bills**: Mint Green (#95E1D3)
- **Other**: Lavender (#C7CEEA)

---

## 📁 Project Structure

```
expense-tracker/
│
├── app.py                      # Main Flask application
├── database.py                 # SQLite database operations
├── requirements.txt            # Python dependencies
├── expenses.db                 # SQLite database (auto-created)
├── README.md                   # Project documentation
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Dashboard page
│   ├── add_expense.html       # Add expense form
│   ├── view_expenses.html     # View expenses table
│   ├── analysis.html          # Analysis and charts page
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
│
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # Main JavaScript file
│
└── utils/
    ├── __init__.py
    └── charts.py              # Chart utilities (minimal)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
# Using Git
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Or download and extract the ZIP file
cd c:\Users\BINDU SREE\Desktop\PROJECTS\expense-tracker
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000` in your browser.

```
========================================================
💰 Personal Expense Tracker
========================================================

✓ Starting Expense Tracker Application...
✓ Open your browser and go to: http://localhost:5000

Press CTRL+C to stop the server.

========================================================
```

---

## 💻 Usage Guide

### Adding an Expense

1. Click on **"➕ Add Expense"** in the navigation menu
2. Fill in the following details:
   - **Date**: Select the date of the expense
   - **Category**: Choose from Food, Travel, Shopping, Bills, or Other
   - **Amount**: Enter the expense amount in Rupees
   - **Description**: Add optional notes about the expense
3. Click **"✅ Add Expense"** button
4. See the confirmation message and get redirected to View Expenses

### Viewing Expenses

1. Click on **"📋 View Expenses"** in the navigation menu
2. Use the filters:
   - Filter by category using the dropdown
   - Sort by date or amount (ascending or descending)
   - Select entries per page (5, 10, 15, 20, or all)
3. Download your expenses:
   - Click **"📥 CSV"** for spreadsheet format
   - Click **"📊 Excel"** for Excel format
4. Delete individual expenses with the 🗑️ button

### Analyzing Spending

1. Click on **"📈 Analysis"** in the navigation menu
2. Choose from four analysis tabs:
   - **📊 Overview**: Quick visual summary with charts and metrics
   - **🏷️ By Category**: Category-wise analysis with transaction details
   - **📅 By Time**: Daily expense trends and comparisons
   - **📉 Statistics**: Detailed tables and top expenses list

### Dashboard Overview

The **"📊 Dashboard"** shows:
- Total spending amount in Rupees
- Number of transactions recorded
- Average expense value
- Visual pie and bar charts
- Recent expense list
- All-in-one overview of your finances

---

## 🔧 Technical Details

### Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core programming language |
| **Flask 3.0** | Web framework for the backend |
| **SQLite 3** | Local database for data persistence |
| **Pandas 2.2** | Data manipulation and analysis |
| **Chart.js 4.4** | Interactive frontend charts |
| **HTML5 & CSS3** | Frontend markup and styling |
| **JavaScript** | Frontend interactivity |

### Database Schema

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,                    -- Expense date (YYYY-MM-DD)
    category TEXT NOT NULL,                -- Category (Food, Travel, etc.)
    amount REAL NOT NULL,                  -- Expense amount in Rupees
    description TEXT,                      -- Optional description
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Record creation time
)
```

### API Endpoints

#### GET Routes
- `/` - Dashboard page
- `/add` - Add expense form page
- `/view` - View expenses page
- `/analysis` - Analysis page

#### API Routes (JSON)
- `GET /api/expenses` - Get all expenses (with filtering & sorting)
- `GET /api/dashboard-stats` - Get dashboard statistics
- `GET /api/analysis-data` - Get analysis data
- `GET /api/export-csv` - Download expenses as CSV
- `GET /api/export-excel` - Download expenses as Excel
- `POST /api/add-expense` - Add new expense
- `DELETE /api/delete-expense/<id>` - Delete an expense

---

## 🐛 Troubleshooting

### Issue: Application won't start
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete `expenses.db` to reset the database (will be auto-created on next run):
```bash
del expenses.db  # On Windows
rm expenses.db   # On macOS/Linux
```

### Issue: Port 5000 already in use
**Solution**: Modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Issue: Charts not displaying
**Solution**: Ensure Chart.js is loaded from CDN and clear browser cache (Ctrl+Shift+Delete)

### Issue: Import errors
**Solution**: Make sure you've activated the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## 📊 Example Usage Scenarios

### Scenario 1: Daily Expense Tracking
1. Open the app and go to "Add Expense"
2. Record your daily expenses (food, transport, etc.)
3. Use the Dashboard to see your spending patterns
4. Identify which categories consume most of your budget

### Scenario 2: Monthly Report Generation
1. Go to "View Expenses"
2. Use filters and sorting to organize your expenses
3. Download as Excel for record-keeping
4. Share with family or accountant

### Scenario 3: Budget Analysis
1. Go to "Analysis" section
2. Review statistics and category breakdowns
3. Identify spending trends
4. Plan budget for next month

---

## 🚀 Future Enhancements

- [ ] Budget setting and alerts
- [ ] Monthly/Yearly reports
- [ ] User authentication (multi-user support)
- [ ] Recurring expense automation
- [ ] Email expense notifications
- [ ] Mobile app
- [ ] Cloud backup
- [ ] Expense categories customization
- [ ] Receipt image upload
- [ ] Dark mode toggle

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the FAQ section below

---

## ❓ FAQ

**Q: Can I use this on my phone?**  
A: Yes! The application is fully responsive and works on mobile devices.

**Q: Where is my data stored?**  
A: All your data is stored locally in an `expenses.db` SQLite database file in the project directory.

**Q: Is my data secure?**  
A: Your data is stored locally on your computer. For online backup, you can download the Excel export regularly.

**Q: Can I import data from other apps?**  
A: Currently, you need to add expenses manually. CSV import is a planned enhancement.

**Q: What if I delete an expense?**  
A: You can delete expenses by clicking the delete button. This action cannot be undone, so be careful!

**Q: Can I edit an expense after adding it?**  
A: Currently, you need to delete and re-add it. Edit functionality is planned for future versions.

---

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [SQLite Tutorial](https://www.sqlite.org/docs.html)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [HTML & CSS Guide](https://developer.mozilla.org/en-US/docs/Web/HTML)

---

## 🎯 Quick Start Checklist

- [ ] Clone/download the project
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run the app: `python app.py`
- [ ] Open browser at `http://localhost:5000`
- [ ] Start adding and tracking expenses!

---

## 📊 Project Statistics

- **Lines of Code**: ~2,500+
- **Modules**: 4
- **Database Tables**: 1
- **Pages**: 4
- **API Routes**: 8+
- **Interactive Charts**: 4
- **Supported Categories**: 5
- **Features**: 25+

---

## ⭐ Give it a Star!

If you find this project helpful, please consider giving it a star on GitHub! ⭐

---

## 🎉 Thank You!

Thank you for using the Personal Expense Tracker. Happy expense tracking! 💰

---

**Last Updated**: March 5, 2026  
**Version**: 2.0.0 (Flask Edition)  
**License**: MIT


---

## 🌟 Features

### 📊 Dashboard
- **Key Metrics Display**: View total spending, transaction count, and average expense at a glance
- **Visual Analytics**: Interactive pie charts, bar charts, and trend lines
- **Quick Statistics**: Sidebar with category breakdown and quick stats
- **Professional UI**: Modern gradient headers, color-coded cards, and responsive design

### ➕ Add Expense
- **Simple Form Interface**: Intuitive expense entry form with validation
- **Multiple Categories**: Food, Travel, Shopping, Bills, and Other
- **Date Picker**: Easy date selection for past or current expenses
- **Flexible Description**: Optional notes for expense details
- **Success Feedback**: Celebratory balloons and confirmation messages

### 📋 View Expenses
- **Comprehensive Table**: All expenses displayed in a clean, organized table
- **Advanced Filtering**: Filter by category with dropdown selection
- **Flexible Sorting**: Sort by date (ascending/descending) or amount (ascending/descending)
- **Pagination**: View 5, 10, 15, 20, or all entries per page
- **Export Options**: Download expenses as CSV or Excel files
- **Summary Statistics**: Total, count, average, and highest expense metrics

### 📈 Analysis
- **Multiple Analysis Views**:
  - **Overview**: Pie charts and bar charts of spending distribution
  - **By Category**: Category-wise breakdown with daily tracking
  - **By Time**: Expense trends over time with date-range filtering
  - **Statistics**: Detailed daily and category statistics with top 10 expenses

---

## 🎨 UI/UX Design

### Modern Interface Features
- **Gradient Backgrounds**: Professional purple gradient theme
- **Card-Based Layout**: Clean cards with shadows for depth
- **Color-Coded Categories**: Distinct colors for each expense category
- **Emoji Icons**: Visual indicators for better UX
- **Responsive Design**: Works seamlessly on different screen sizes
- **Professional Typography**: Clear, readable fonts with proper hierarchy
- **Interactive Charts**: Plotly-based interactive visualizations with hover details
- **Smooth Transitions**: Button hover effects and visual feedback

### Color Scheme
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Food**: Red (#FF6B6B)
- **Travel**: Teal (#4ECDC4)
- **Shopping**: Yellow (#FFE66D)
- **Bills**: Mint Green (#95E1D3)
- **Other**: Lavender (#C7CEEA)

---

## 📁 Project Structure

```
expense-tracker/
│
├── app.py                      # Main Streamlit application
├── database.py                 # SQLite database operations
├── requirements.txt            # Python dependencies
├── expenses.db                 # SQLite database (auto-created)
├── README.md                   # Project documentation
│
└── utils/
    ├── __init__.py             # Package initialization
    └── charts.py               # Visualization functions
```

### File Descriptions

#### `app.py`
- Main Streamlit application with the complete UI
- Contains all page implementations (Dashboard, Add Expense, View Expenses, Analysis)
- Handles sidebar navigation and custom CSS styling
- Manages form submission and data display

#### `database.py`
- SQLite database management module
- Functions for CRUD operations (Create, Read, Update, Delete)
- Date-range filtering and category-based queries
- Statistical calculations (total spending, spending by category, etc.)

#### `utils/charts.py`
- Visualization module using Plotly
- **Functions**:
  - `create_category_pie_chart()`: Pie chart of spending distribution
  - `create_expense_trend_chart()`: Line chart of daily expenses
  - `create_category_bar_chart()`: Bar chart of category spending
  - `create_category_comparison_chart()`: Stacked bar chart of daily spending by category

#### `requirements.txt`
- All Python package dependencies with specific versions
- Includes Streamlit, Pandas, Plotly, and other utilities

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone or Download the Project

```bash
# Using Git
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Or download and extract the ZIP file
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

---

## 💻 Usage Guide

### Adding an Expense

1. Click on **"➕ Add Expense"** in the sidebar
2. Fill in the following details:
   - **Date**: Select the date of the expense
   - **Category**: Choose from Food, Travel, Shopping, Bills, or Other
   - **Amount**: Enter the expense amount in Rupees
   - **Description**: Add optional notes about the expense
3. Click **"✅ Add Expense"** button
4. See the confirmation message and your data is saved!

### Viewing Expenses

1. Click on **"📋 View Expenses"** in the sidebar
2. Use the filters:
   - Filter by category using the dropdown
   - Sort by date or amount
   - Select entries per page
3. Download your expenses:
   - Click **📥 Download as CSV** for spreadsheet format
   - Click **📊 Download as Excel** for Excel format

### Analyzing Spending

1. Click on **"📈 Analysis"** in the sidebar
2. Choose from four analysis tabs:
   - **📊 Overview**: Quick visual summary with pie and bar charts
   - **🏷️ By Category**: Category-wise analysis with daily tracking
   - **📅 By Time**: Expense trends and date-range analysis
   - **📉 Statistics**: Detailed statistical breakdown and top expenses

### Dashboard Overview

The **"📊 Dashboard"** shows:
- Total spending amount
- Number of transactions
- Average expense value
- Visual charts and trends
- All-in-one overview of your finances

---

## 🔧 Technical Details

### Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python** | Core programming language |
| **Streamlit** | Web framework for the UI |
| **SQLite** | Local database for data storage |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive data visualizations |
| **Matplotlib** | Additional charting capabilities |

### Database Schema

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,                    -- Expense date (YYYY-MM-DD)
    category TEXT NOT NULL,                -- Category (Food, Travel, etc.)
    amount REAL NOT NULL,                  -- Expense amount
    description TEXT,                      -- Optional description
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Record creation time
)
```

### API Functions

#### Database Operations (`database.py`)

```python
initialize_database()              # Initialize SQLite database
add_expense(date, category, amount, description)  # Add new expense
get_all_expenses()                # Retrieve all expenses
get_expenses_by_category(category)  # Filter by category
get_expenses_by_date_range(start, end)  # Filter by date range
delete_expense(expense_id)         # Delete specific expense
update_expense(id, date, cat, amt, desc)  # Update expense
get_total_spending()               # Calculate total spending
get_spending_by_category()         # Get category breakdown
get_expense_count()                # Get total transactions
```

#### Visualization Functions (`utils/charts.py`)

```python
create_category_pie_chart(spending_by_category)  # Pie chart
create_expense_trend_chart(expenses_df)          # Trend line chart
create_category_bar_chart(spending_by_category)  # Bar chart
create_category_comparison_chart(expenses_df)    # Stacked bar chart
```

---

## 📊 Example Usage Scenarios

### Scenario 1: Monthly Budget Review
1. Open the Dashboard to see total monthly spending
2. View the pie chart to understand where money is going
3. Analyze spending trends in the Analysis section
4. Export the data to share with family or accountant

### Scenario 2: Category Spending Analysis
1. Go to Analysis → By Category
2. View detailed category breakdown
3. Identify spending patterns
4. Set budget goals for next month

### Scenario 3: Data Export for Record Keeping
1. Go to View Expenses
2. Filter by date range if needed
3. Download as Excel for record keeping
4. Keep annual records in organized folders

---

## 🐛 Troubleshooting

### Issue: Application won't start
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete `expenses.db` to reset the database:
```bash
# The database will be automatically recreated on next run
del expenses.db
```

### Issue: Port already in use
**Solution**: Run Streamlit on a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Charts not displaying
**Solution**: Update Plotly:
```bash
pip install --upgrade plotly
```

---

## 📈 Future Enhancements

- [ ] Budget setting and alerts
- [ ] Monthly/Yearly expense reports
- [ ] Multi-user support with authentication
- [ ] Recurring expenses automation
- [ ] Mobile-responsive improvements
- [ ] Dark mode toggle
- [ ] Expense tags for better categorization
- [ ] Bill reminders and notifications
- [ ] Cloud backup integration
- [ ] Data import from banking apps

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Support

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Contact the development team
- Check the troubleshooting section above

---

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [SQLite Tutorial](https://www.sqlite.org/docs.html)
- [Pandas Guide](https://pandas.pydata.org/docs/)

---

## 🎯 Quick Start Checklist

- [ ] Clone/download the project
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run the app: `streamlit run app.py`
- [ ] Open browser at `http://localhost:8501`
- [ ] Start adding expenses!

---

## 📊 Statistics

- **Lines of Code**: ~2000+
- **Modules**: 3
- **Database Tables**: 1
- **Pages**: 4
- **Charts**: 4+
- **Features**: 20+

---

## ⭐ Give it a Star!

If you find this project helpful, please consider giving it a star on GitHub! ⭐

---

**Happy Expense Tracking! 💰**

Last Updated: March 5, 2026  
Version: 1.0.0
