import calendar
import datetime
import random


def irregular(now=None):
    now = datetime.datetime.utcnow() if now is None else now
    date = now.date()
    while True:
        seed = calendar.timegm(date.timetuple())
        chooser = random.Random(seed)
        offset = seconds=chooser.randint(0, 86400)
        release = datetime.datetime.fromordinal(date.toordinal())
        release = release + datetime.timedelta(seconds=offset)
        if release < now:
            break
        date = date - datetime.timedelta(days=1)
    return release
