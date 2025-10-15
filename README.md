# PNC Student Management System

A full-stack web application for managing student records at PNC (Passerelles Numériques Cambodia) with a Flask backend and a modern JavaScript frontend. The application allows administrators to perform CRUD operations on student data and export records in CSV or JSON format.

## Features

- View all students in a responsive table
- Add new student records with validation
- Edit existing student details
- Delete student records
- Export student data to CSV or JSON
- Responsive design that works on desktop and mobile
- Modern, user-friendly interface with PNC branding
- Secure data management with CSV backend

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd employee-management-system
   ```

2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the backend server (from the backend directory):
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:8000`

2. In a new terminal, start the frontend server (from the project root):
   ```bash
   cd frontend
   python -m http.server 5500
   ```
   The frontend will be available at `http://localhost:5500`

## API Endpoints

- `GET /api/employees` - Get all employees
- `GET /api/employees/<id>` - Get a specific employee
- `POST /api/employees` - Add a new employee
- `PUT /api/employees/<id>` - Update an employee
- `DELETE /api/employees/<id>` - Delete an employee
- `GET /api/export/csv` - Export all employees as CSV
- `GET /api/export/json` - Export all employees as JSON

## Project Structure

```
myapp/
├── backend/
│   ├── app.py           # Flask application
│   ├── requirements.txt  # Python dependencies
│   └── data/
│       └── employees.csv # Employee data storage
└── frontend/
    ├── index.html       # Main HTML file
    ├── style.css        # Styling
    └── script.js        # Frontend JavaScript
```

## Data Format

Student records are stored in CSV format with the following fields:
- `id`: Unique identifier (integer)
- `name`: Full name (string)
- `age`: Age in years (integer)
- `department`: Department/Class name (string)
- `salary`: Stipend/Scholarship amount (number)
- `email`: Email address (string)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Git (for version control)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/phanphoun/csv-json-xml.git
   cd csv-json-xml
   ```

2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the backend server:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:8000`

2. In a new terminal, start the frontend server:
   ```bash
   cd frontend
   python -m http.server 5500
   ```
   The application will be available at `http://localhost:5500`

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Structure

```
myapp/
├── backend/
│   ├── app.py           # Flask application
│   ├── requirements.txt  # Python dependencies
│   └── data/
│       └── employees.csv # Student data storage
└── frontend/
    ├── index.html       # Main HTML file
    ├── style.css        # Styling
    ├── script.js        # Frontend JavaScript
    └── image/           # Project images and assets
        └── pnc.jpg      # PNC logo
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask and vanilla JavaScript
- Uses Pandas for data manipulation
- Responsive design with CSS Grid and Flexbox
- PNC (Passerelles Numériques Cambodia) for the inspiration