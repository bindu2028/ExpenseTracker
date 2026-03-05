// Personal Expense Tracker - Main JavaScript

// Utility function to format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Utility function to format date
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-IN');
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    const container = document.body;
    container.insertBefore(notification, container.firstChild);
    
    setTimeout(() => notification.remove(), 3000);
}

// Format large numbers
function formatNumber(num) {
    return num.toLocaleString('en-IN');
}

// Debounce function
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// Initialize tooltips or popovers if needed
document.addEventListener('DOMContentLoaded', function() {
    console.log('Personal Expense Tracker initialized');
});

// Export utility
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    downloadFile(csv, filename, 'text/csv');
}

function convertToCSV(data) {
    if (!Array.isArray(data) || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(obj => headers.map(header => JSON.stringify(obj[header] || '')).join(','));
    
    return [headers.join(','), ...rows].join('\n');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// API error handler
function handleAPIError(error) {
    console.error('API Error:', error);
    if (error.response?.data?.message) {
        showNotification('Error: ' + error.response.data.message, 'error');
    } else {
        showNotification('An error occurred. Please try again.', 'error');
    }
}
