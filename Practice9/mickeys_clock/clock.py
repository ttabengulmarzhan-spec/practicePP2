import datetime

class Clock:
    def get_time(self):
        return datetime.datetime.now()

    def get_minute_angle(self, now=None):
        if now is None:
            now = self.get_time()

        minutes = now.minute
        seconds = now.second

        total_seconds = minutes * 60 + seconds
        angle = (total_seconds / 3600) * 360
        return angle

    def get_second_angle(self, now=None):
        if now is None:
            now = self.get_time()

        seconds = now.second
        angle = (seconds / 60) * 360
        return angle