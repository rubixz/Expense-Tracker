from flask import Flask, render_template, request, redirect, url_for, make_response, flash, redirect
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Excel file name defined here
EXCEL_FILE = 'expenses.xlsx'

# Function to ensure Excel file exists on startup
def init_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['id', 'description', 'amount', 'category', 'date'])
        df.to_excel(EXCEL_FILE, index=False)

init_excel()

# Helper function to read expenses from Excel file
def get_expenses():
    df = pd.read_excel(EXCEL_FILE)
    # Convert DataFrame records to list of dictionaries for Jinja2 template
    return df.to_dict(orient='records')

# Helper function to add new expense into Excel file
def add_expense(description, amount, category, date_str=None):
    df = pd.read_excel(EXCEL_FILE)
    
    new_id = len(df) + 1 if not df.empty else 1
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')
        
    new_row = {
        'id': new_id,
        'description': description,
        'amount': float(amount),
        'category': category,
        'date': date_str
    }
    
    # Append row and save back to Excel
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)


# Main route: Show expenses
@app.route('/')
def index():
    expenses = get_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add():

    description = (request.form.get('description') or '').strip()
    amount_str = (request.form.get('amount') or '').strip()
    category = (request.form.get('category') or '').strip()
    date_str = (request.form.get('date') or '').strip()

    if not description or not amount_str or not category:
        flash("Please fill description, amount, and category.", "error")

    try:
        amount = float(amount_str)  
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a valid number.", "error")
        return redirect(url_for('index'))










    print("From received request:", dict(request.form))    
    return make_response("From received request console")






if __name__ == '__main__':
    app.run(debug=True, port=4848)
