import datetime

import pytz


class DateHelpers:
    @staticmethod
    def get_jamaica_timezone():
        return pytz.timezone("America/Jamaica")

    @staticmethod
    def get_current_bogota_datetime():
        d = datetime.datetime.now()
        timezone = pytz.timezone("America/Bogota")
        d_aware = timezone.localize(d)
        return  d_aware
