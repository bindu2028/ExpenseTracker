"""
Chart utilities for the Expense Tracker application.
Note: Charts are now handled by Chart.js on the frontend for better performance and UX.
Keep this module available for future backend enhancements.
"""

import base64
from io import BytesIO


def generate_pie_chart_base64(spending_by_category):
    """
    Generate a pie chart as base64 for inclusion in email/reports (optional).
    
    Args:
        spending_by_category (Dict[str, float]): Category spending data
    
    Returns:
        str: Base64 encoded image string
    
    Note: Currently unused, kept for future enhancement.
    """
    pass

