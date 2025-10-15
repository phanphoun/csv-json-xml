const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const employeeForm = document.getElementById('employeeForm');
const employeesList = document.getElementById('employeesList');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');

// Show/hide loading and error messages
function showLoading() {
    loadingElement.classList.remove('hidden');
    errorElement.classList.add('hidden');
}

function hideLoading() {
    loadingElement.classList.add('hidden');
}

function showError(message) {
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
}

function hideError() {
    errorElement.classList.add('hidden');
}

// API Functions
async function apiCall(endpoint, options = {}) {
    const requestOptions = {
        method: options.method || 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };

    // For POST/PUT requests, ensure body is stringified
    if (requestOptions.body && typeof requestOptions.body !== 'string') {
        requestOptions.body = JSON.stringify(requestOptions.body);
    }

    console.log(`API Call: ${requestOptions.method} ${API_BASE_URL}${endpoint}`);
    
    try {
        showLoading();
        hideError();
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, requestOptions);
        const responseData = await response.json().catch(() => ({}));
        
        console.log(`Response Status: ${response.status}`, responseData);

        if (!response.ok) {
            const errorMessage = responseData.error || response.statusText || 'Unknown error occurred';
            throw new Error(`HTTP ${response.status}: ${errorMessage}`);
        }

        return responseData;
    } catch (error) {
        console.error('API call failed:', {
            endpoint,
            options,
            error: error.message,
            stack: error.stack
        });
        
        // More specific error messages
        if (error.message.includes('Failed to fetch')) {
            showError('Cannot connect to the server. Please make sure the backend is running.');
        } else {
            showError(`Error: ${error.message}`);
        }
        
        throw error;
    } finally {
        hideLoading();
    }
}

// Load and display employees
async function loadEmployees() {
    try {
        const employees = await apiCall('/employees');
        displayEmployees(employees);
    } catch (error) {
        // Error already handled in apiCall
    }
}

function displayEmployees(employees) {
    if (employees.length === 0) {
        employeesList.innerHTML = '<p>No employees found.</p>';
        return;
    }

    employeesList.innerHTML = employees.map(employee => `
        <div class="employee-card" data-id="${employee.id}">
            <div class="employee-info">
                <h3>${employee.name}</h3>
                <p><strong>Department:</strong> ${employee.department}</p>
                <p><strong>Age:</strong> ${employee.age} | <strong>Salary:</strong> $${employee.salary.toLocaleString()}</p>
                <p><strong>Email:</strong> ${employee.email}</p>
            </div>
            <div class="employee-actions">
                <button class="btn-edit" onclick="editEmployee(${employee.id})">Edit</button>
                <button class="btn-delete" onclick="deleteEmployee(${employee.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Add new employee
employeeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        department: document.getElementById('department').value,
        salary: parseInt(document.getElementById('salary').value),
        email: document.getElementById('email').value
    };

    try {
        await apiCall('/employees', {
            method: 'POST',
            body: JSON.stringify(formData)
        });

        // Clear form and refresh list
        employeeForm.reset();
        await loadEmployees();
        
        // Show success message
        showError('Employee added successfully!');
        errorElement.style.background = '#d4edda';
        errorElement.style.color = '#155724';
        setTimeout(hideError, 3000);
    } catch (error) {
        // Error already handled in apiCall
    }
});

// Edit employee (placeholder - you can implement a modal)
async function editEmployee(id) {
    try {
        const employee = await apiCall(`/employees/${id}`);
        
        // In a real app, you'd show a modal or edit form
        const newName = prompt('Enter new name:', employee.name);
        const newSalary = prompt('Enter new salary:', employee.salary);
        
        if (newName && newSalary) {
            await apiCall(`/employees/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    name: newName,
                    salary: parseInt(newSalary)
                })
            });
            
            await loadEmployees();
        }
    } catch (error) {
        // Error already handled in apiCall
    }
}

// Delete employee
async function deleteEmployee(id) {
    if (confirm('Are you sure you want to delete this employee?')) {
        try {
            await apiCall(`/employees/${id}`, {
                method: 'DELETE'
            });
            
            await loadEmployees();
        } catch (error) {
            // Error already handled in apiCall
        }
    }
}

// Export functions
async function exportCSV() {
    try {
        const response = await fetch(`${API_BASE_URL}/export/csv`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'employees.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        showError(`Export failed: ${error.message}`);
    }
}

async function exportJSON() {
    try {
        const data = await apiCall('/export/json');
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'employees.json';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        // Error already handled in apiCall
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadEmployees();
});