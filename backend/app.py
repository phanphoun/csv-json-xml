from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import os
import json

app = Flask(__name__)
# Configure CORS with specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Data file path
DATA_FILE = 'data/employees.csv'

def initialize_data():
    """Create sample data if it doesn't exist"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # If file doesn't exist or is empty, create it with sample data
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            data = {
                'id': [1, 2, 3, 4],
                'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince'],
                'age': [25, 30, 35, 28],
                'department': ['Engineering', 'Marketing', 'Sales', 'HR'],
                'salary': [50000, 60000, 70000, 55000],
                'email': ['alice@company.com', 'bob@company.com', 'charlie@company.com', 'diana@company.com']
            }
            df = pd.DataFrame(data)
            # Ensure directory exists before writing
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            # Write with explicit encoding and ensure proper line endings
            df.to_csv(DATA_FILE, index=False, encoding='utf-8', lineterminator='\n')
            print(f"Sample data created at: {os.path.abspath(DATA_FILE)}")
            
    except Exception as e:
        print(f"Error initializing data: {str(e)}")
        # If there's an error, try to create a basic CSV file
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                f.write('id,name,age,department,salary,email\n')
                f.write('1,Alice Johnson,25,Engineering,50000,alice@company.com\n')
                f.write('2,Bob Smith,30,Marketing,60000,bob@company.com\n')
                f.write('3,Charlie Brown,35,Sales,70000,charlie@company.com\n')
                f.write('4,Diana Prince,28,HR,55000,diana@company.com\n')
            print("Created basic CSV file with sample data")
        except Exception as e2:
            print(f"Failed to create basic CSV file: {str(e2)}")

# Initialize data on startup
initialize_data()

# API Routes
@app.route('/')
def home():
    return jsonify({"message": "Employee Management API", "version": "1.0"})

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees"""
    try:
        df = pd.read_csv(DATA_FILE)
        employees = df.to_dict('records')
        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get a specific employee by ID"""
    try:
        df = pd.read_csv(DATA_FILE)
        employee = df[df['id'] == employee_id]
        
        if employee.empty:
            return jsonify({"error": "Employee not found"}), 404
        
        return jsonify(employee.to_dict('records')[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees', methods=['POST'])
def add_employee():
    """Add a new employee"""
    try:
        data = request.get_json()
        
        # Read existing data
        df = pd.read_csv(DATA_FILE)
        
        # Generate new ID
        new_id = df['id'].max() + 1 if not df.empty else 1
        
        # Create new employee
        new_employee = {
            'id': new_id,
            'name': data.get('name'),
            'age': data.get('age'),
            'department': data.get('department'),
            'salary': data.get('salary'),
            'email': data.get('email')
        }
        
        # Add to DataFrame
        new_df = pd.DataFrame([new_employee])
        df = pd.concat([df, new_df], ignore_index=True)
        
        # Save back to CSV
        df.to_csv(DATA_FILE, index=False)
        
        return jsonify({"message": "Employee added successfully", "employee": new_employee}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update an existing employee"""
    try:
        data = request.get_json()
        df = pd.read_csv(DATA_FILE)
        
        # Find employee index
        mask = df['id'] == employee_id
        if not mask.any():
            return jsonify({"error": "Employee not found"}), 404
        
        # Update employee data
        for key, value in data.items():
            if key in df.columns and key != 'id':  # Don't update ID
                df.loc[mask, key] = value
        
        # Save back to CSV
        df.to_csv(DATA_FILE, index=False)
        
        updated_employee = df[mask].to_dict('records')[0]
        return jsonify({"message": "Employee updated successfully", "employee": updated_employee})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    try:
        df = pd.read_csv(DATA_FILE)
        
        # Check if employee exists
        mask = df['id'] == employee_id
        if not mask.any():
            return jsonify({"error": "Employee not found"}), 404
        
        # Remove employee
        df = df[~mask]
        
        # Save back to CSV
        df.to_csv(DATA_FILE, index=False)
        
        return jsonify({"message": "Employee deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export data as CSV file"""
    try:
        return send_file(DATA_FILE, as_attachment=True, download_name='employees.csv')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export data as JSON"""
    try:
        df = pd.read_csv(DATA_FILE)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add this new function to handle contact form submissions
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        required_fields = ['name', 'email', 'subject', 'message']
        
        # Validate required fields
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Create or append to contact submissions file
        contact_file = 'data/contact_submissions.csv'
        file_exists = os.path.exists(contact_file)
        
        import csv
        from datetime import datetime
        
        # Generate a new ID
        new_id = 1
        if file_exists:
            with open(contact_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    new_id = max(int(row['id']) for row in rows) + 1
        
        # Prepare new submission
        new_submission = {
            'id': str(new_id),
            'timestamp': datetime.now().isoformat(),
            'name': data['name'].strip(),
            'email': data['email'].strip(),
            'subject': data['subject'].strip(),
            'message': data['message'].strip()
        }
        
        # Write to CSV
        with open(contact_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'timestamp', 'name', 'email', 'subject', 'message'])
            if not file_exists or os.path.getsize(contact_file) == 0:
                writer.writeheader()
            writer.writerow(new_submission)
        
        return jsonify({'message': 'Thank you for your message! We will get back to you soon.'}), 201
        
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

# Add this endpoint to view all contact submissions (for admin/developer)
@app.route('/api/admin/contact-submissions', methods=['GET'])
def get_contact_submissions():
    try:
        contact_file = 'data/contact_submissions.csv'
        if not os.path.exists(contact_file):
            return jsonify([])
            
        import pandas as pd
        df = pd.read_csv(contact_file)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        print(f"Error retrieving contact submissions: {str(e)}")
        return jsonify({'error': 'Failed to retrieve contact submissions'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)