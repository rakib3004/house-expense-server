# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection parameters
DB_CONFIG = {
    'host': '172.27.108.250',
    'port': 5432,
    'database': 'house_expense',
    'user': 'postgres',
    'password': 'P0StGr35'
}

def get_db_connection():
    """Establish and return a database connection"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@app.route('/api/monthly-expenses', methods=['GET'])
def get_monthly_expenses():
    """Get expenses for a specific month and year"""
    try:
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        
        if not month or not year:
            return jsonify({"error": "Month and year are required"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Call the stored procedure
        cursor.execute(
            "CALL get_monthly_expenses(%s, %s)",
            (month, year)
        )
        
        # Fetch results from the temporary table created by the stored procedure
        cursor.execute("SELECT * FROM temp_monthly_expenses")
        expenses = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for row in expenses:
            expense_dict = dict(row)
            # Convert date objects to string for JSON serialization
            if 'date' in expense_dict and isinstance(expense_dict['date'], datetime):
                expense_dict['date'] = expense_dict['date'].strftime('%Y-%m-%d')
            result.append(expense_dict)
        
        cursor.close()
        conn.close()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/category-expenses', methods=['GET'])
def get_category_expenses():
    """Get expenses for a specific category within a date range"""
    try:
        category = request.args.get('category')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not category or not start_date or not end_date:
            return jsonify({"error": "Category, start date and end date are required"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Call the stored procedure
        cursor.execute(
            "CALL get_category_expenses(%s, %s, %s)",
            (category, start_date, end_date)
        )
        
        # Fetch results from the temporary table created by the stored procedure
        cursor.execute("SELECT * FROM temp_category_expenses")
        expenses = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for row in expenses:
            expense_dict = dict(row)
            # Convert date objects to string for JSON serialization
            if 'date' in expense_dict and isinstance(expense_dict['date'], datetime):
                expense_dict['date'] = expense_dict['date'].strftime('%Y-%m-%d')
            result.append(expense_dict)
        
        cursor.close()
        conn.close()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/custom-expenses', methods=['GET'])
def get_custom_expenses():
    """Get expenses based on amount range and date range"""
    try:
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if min_amount is None or max_amount is None or not start_date or not end_date:
            return jsonify({"error": "Min amount, max amount, start date and end date are required"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Call the stored procedure
        cursor.execute(
            "CALL get_custom_expenses(%s, %s, %s, %s)",
            (min_amount, max_amount, start_date, end_date)
        )
        
        # Fetch results from the temporary table created by the stored procedure
        cursor.execute("SELECT * FROM temp_custom_expenses")
        expenses = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for row in expenses:
            expense_dict = dict(row)
            # Convert date objects to string for JSON serialization
            if 'date' in expense_dict and isinstance(expense_dict['date'], datetime):
                expense_dict['date'] = expense_dict['date'].strftime('%Y-%m-%d')
            result.append(expense_dict)
        
        cursor.close()
        conn.close()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)