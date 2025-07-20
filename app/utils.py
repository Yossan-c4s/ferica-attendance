from datetime import datetime
import pytz

def get_japan_time():
    return datetime.now(pytz.timezone("Asia/Tokyo"))