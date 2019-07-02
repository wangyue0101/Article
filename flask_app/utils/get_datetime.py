from datetime import datetime, date
import pytz


LOCAL_TIMEZONE = pytz.timezone("Asia/Shanghai")


def get_midnight_today_to_utc():
    naive_midnight = datetime.now()
    local_midnight = LOCAL_TIMEZONE.localize(naive_midnight)
    return local_midnight
