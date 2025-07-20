from datetime import datetime, timedelta

def getDateRange(end_date):
    # Define the date format
    date_format = "%Y-%m-%d"
    new_date_format = "%m/%d/%Y"
    # Parse the input string into a datetime object
    original_date = datetime.strptime(end_date, date_format)

    # Subtract 20 days
    date_20_days_before = original_date - timedelta(days=20)

    # Convert date back to string format
    start_date = date_20_days_before.strftime(new_date_format)

    return start_date, end_date