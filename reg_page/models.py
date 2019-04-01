from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Event(models.Model):
    data = models.DateField()

    def __str__(self):
        return '%s' % self.data

    def res_data(self):
        '''methor make restriction to model Event
        output only date >= at data today
        '''
        date_now = datetime.now().date()
        return self.data >= date_now


class Time(models.Model):
    data_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "{data_event}  -  {time}  -  {user}".format(data_event=self.data_event, time=self.time, user=self.user)

    def res_time(self):
        '''methor make restriction to model Time
        output only time >= at time now (-1 min to check connect between db alb app)
        '''
        time_now = (datetime.now() - timedelta(minutes=1)).time()
        date_now = datetime.now().date()
        return self.time >= time_now and self.data_event.data >= date_now


class CalendarEvent:

    actual_date = datetime.now()
    month = 1

    def __init__(self, actual_date, month):
        self.actual_date = actual_date
        self.month = month

    def name_actual_month(self):
        """output name of actual month"""
        return self.actual_date.strftime("%B")

    def month_dec(func):
        def math_month(self):
            "output + n month name"
            year = self.actual_date.year
            next_month = self.actual_date.month + func(self)
            day = 1
            if next_month > 0:
                while next_month > 12:
                    year += 1
                    next_month -= 12
            elif next_month < 0:
                while next_month < 0:
                    year -= 1
                    next_month += 12
            return datetime(year, next_month, day)
        return math_month

    @month_dec
    def add_month(self):
        """output add month"""
        return self.month

    @month_dec
    def sub_month(self):
        """output subtract month """
        return - self.month

    def year(self):
        '''output actual year'''
        return self.actual_date.year

    def range_months(self):
        """output range of actual"""
        import calendar
        return calendar.monthrange(self.year(), self.actual_date.month)[1]

