from datetime import datetime, timedelta

def get_current_time():
    utc_now = datetime.utcnow()
    time_plus_5_30 = utc_now + timedelta(hours=5, minutes=30)
    return time_plus_5_30.strftime('%I:%M %p')

def get_current_date():
    current_date = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return current_date.strftime('%d %B, %Y')