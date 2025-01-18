from datetime import datetime, timedelta, timezone


class DatetimeUtil:
    JST: timezone = timezone(timedelta(hours=9))

    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now(tz=DatetimeUtil.JST)
