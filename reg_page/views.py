from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.views import View
from django.http import Http404
from time import strptime
from .models import(
    CalendarEvent,
    Event,
    Time,
)
from django.views.generic import(
    ListView,
)
from .forms import UsernameForm

class ViewMixed(object):
    '''container union method '''
    hours = (9, 12, 15)

    def get_month(self, num):
        """output actual name month when num ==0 and next name month when num+=1 """
        month = CalendarEvent(datetime.now(), num).add_month().strftime("%B")
        return month

    def get_year(self, num):
        """output actual year when num ==0 and next year when num+=1 month is > 12 """
        year = CalendarEvent(datetime.now(), num).add_month().year
        return year

    def get_date_add_month(self, num):
        """output date month +1 to actual month if num=0 and +num date month to +1 month when num+=1 """
        data_month = CalendarEvent(datetime.now(), num).add_month()
        return data_month

    def get_range_month(self, num):
        """output range actual month and range month num+=1 """
        variable = num
        range_month = CalendarEvent(self.get_date_add_month(variable), variable).range_months()
        return range_month

    def createEvent_data(self, data, request, *args, **kwargs):
        """output create data Event in db or if event exist return value od datetime.date()"""
        create_data_event = Event(data=data)
        all_objects = self.all_ocjects_data_Event()
        data_created = Event.objects.filter(data=data).first()
        if data_created not in all_objects:
            return create_data_event.save()
        else:
            return data_created

    def createEvent_time(self, data, time, data_created_id, user_id, request, *args, **kwargs):
        """output cerate Event time or return exist Event time """
        create_time_Event = Time(time=time, data_event_id=data_created_id, user_id=user_id)
        all_objects = self.all_object_time_Event()
        data_created = Event.objects.filter(data=data).first()
        time_created = Time.objects.filter(time=time, data_event_id=data_created.id).first()
        if time_created not in all_objects:
            messages.success(request, "You have made an appointment successfully !")
            return create_time_Event.save()
        else:
            messages.error(request, "This hour was reserved! Try another")
            return time_created

    def all_ocjects_data_Event(self):
        """output all event in date db"""
        events = Event.objects.all()
        return events

    def all_object_time_Event(self):
        """output all event in time db"""
        times = Time.objects.all()
        return times

    def active_user(self, request):
        """output logged user"""
        active_user = request.user
        user = User.objects.filter(username=active_user).first()
        return user

    def variables_data(self, var, request, *args, **kwargs):
        '''variables data upload from kwargs.
        Output data or time in format datetime from data in last side.
        Input: var = put 'data' or 'time',
        example: for htttp:register/March/2019/8/12 get March/2019/8/12
        and convert to datetime(2019, 3, 9, 12) and output data or time'''
        year = kwargs['year']
        month_num = strptime(kwargs['month'][0:3], '%b').tm_mon
        day = kwargs['day']
        hour = kwargs['hour']
        data = datetime(year, month_num, day, hour).date()
        time = datetime(year, month_num, day, hour).time()
        if var == 'data':
            return data
        elif var == 'time':
            return time

    def get_home_context(self, num=0):
        context = {
            'month': self.get_month(num),
            'year': self.get_year(num),
        }
        return context


class HomeView(ViewMixed, View):
    ''' render index view page '''
    templates = 'reg_page/home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_home_context()
        context['title'] = 'home'
        return render(request, self.templates, context)

class RegisterView(ViewMixed, View):
    ''' render register view page '''
    templates = 'reg_page/register.html'

    def get(self, request, *args, **kwargs):
        for num in range(0, 13):
            context = {
                'title': self.get_month(num),
                'month': self.get_month(num),
                'year': self.get_year(num),
                'next_month': self.get_month(num + 1),
                'next_year': self.get_year(num + 1),
                'beck_month': self.get_month(num - 1),
                'beck_year': self.get_year(num - 1),
                'range_month_past': self.get_list_days(0, self.get_range_day()+1),
                # 'range_month_past': range(self.get_range_day(), self.get_range_month(num)+1),
                'range_month': range(1, self.get_range_month(num)+1),
                'past_days': range(1, self.get_range_day()+1),
                'actual_month': self.get_month(0),
                'actual_year': self.get_year(0),
                'get_list_days': self.get_list_days(num, 1),
            }
            if kwargs['month'] in context['month']:
                return render(request, self.templates, context)
        raise Http404('No page')

    def get_future_day(self):
        """output future list days to reservations.
        Return list days and information about register hours reservation.
        If user booking date then output True else False.
        np.(28, ['False', 'True', 'True'])"""
        list_future = []
        for future_day in range(self.get_range_day(), self.get_range_month(0) + 1):
            list_future.append(self.get_list_days(0)[future_day - 1])
        return list_future


    def get_list_days(self, num, start):
        """output list created event in one month - save memory.
        Return list days and information about register hours reservation.
        If user booking date then output True else False.
        np.(28, ['False', 'True', 'True'])"""
        list_events_days = []
        list_one_day_events = []
        list_TrueOrFalse_Event = []
        list_day_res = []

        year = self.get_year(num)
        month = self.get_month(num)
        month_num = strptime(month[0:3], '%b').tm_mon
        days = self.get_range_month(num) + 1
        days_month = self.get_range_month(num)

        all_objects = self.all_object_time_Event()

        for day in range(start, days):
            data = datetime(year, month_num, day).date()
            data_created = Event.objects.filter(data=data).first()

            for hour in self.hours:

                if data_created:
                    time_created = Time.objects.filter(time=datetime(year, month_num, day, hour).time(),
                                                       data_event_id=data_created.id).first()
                    list_events_days.append(time_created)
                else:
                    list_events_days.append('')


        for events_list in list_events_days:

            if events_list in all_objects:
                list_TrueOrFalse_Event.append('True')

            else:
                list_TrueOrFalse_Event.append('False')

        start_list = 0
        end_list = 3

        while end_list <= len(list_TrueOrFalse_Event):
            list_one_day_events.append(list_TrueOrFalse_Event[start_list:end_list])
            start_list += 3
            end_list += 3

        for day_month in range(start - 1, days_month):
            list_set = (day_month + 1, list_one_day_events[day_month - start + 1], list_one_day_events[day_month - start + 1].count('True'))
            list_day_res.append(list_set)

        return list_day_res

    def get_range_day(self):
        """return past day in actual date """
        range_day = int(((datetime.now()).date()).strftime('%d'))
        return range_day


class RegisterHoursView(ViewMixed, View, LoginRequiredMixin):
    '''render view with selected date and choice hours register visit'''
    templates = 'reg_page/register_hours.html'

    def get_context(self, request, *args, **kwargs):
        """get kwargs from page where user been """

        """convert name month to number of month"""
        num = strptime(kwargs['month'][0:3], '%b').tm_mon

        context = {
            'month': kwargs['month'],
            'year': kwargs['year'],
            'range_month': range(1, self.get_range_month_actual(num) + 1),
            'hours': self.hours,
            'day': kwargs['day'],
            'list_exist': self.get_list_TrueOrFalse_Event(**kwargs),
            'res_hours': self.get_list_hours_reserved(**kwargs),
        }
        return context

    def get_list_hours_reserved(self, **kwargs):
        """output list with hours and information about reservation.
        Empty hour have info like True """
        list_hours = []
        for hour in range(0, len(self.hours)):
            list_h = self.hours[hour], self.get_list_TrueOrFalse_Event(**kwargs)[hour]
            list_hours.append(list_h)
        return list_hours

    def get_list_created_event(self, **kwargs):
        """output list created event"""
        hours = self.hours
        list_created_event = []
        year = kwargs['year']
        month_num = strptime(kwargs['month'][0:3], '%b').tm_mon
        day = kwargs['day']
        for hour in hours:
            data = datetime(year, month_num, day).date()
            data_created = Event.objects.filter(data=data).first()
            if data_created:
                time_created = Time.objects.filter(time=datetime(year, month_num, day, hour).time(), data_event_id=data_created.id).first()
                list_created_event.append(time_created)
            else:
                list_created_event.append('')

        return list_created_event

    def get_list_TrueOrFalse_Event(self, **kwargs):
        """output list Event. If event is in db return True else False """
        list_TrueOrFalse_Event = []
        all_objects = self.all_object_time_Event()
        for events_list in self.get_list_created_event(**kwargs):
            if events_list in all_objects:
                list_TrueOrFalse_Event.append('True')
            else:
                list_TrueOrFalse_Event.append('False')
        return list_TrueOrFalse_Event

    def get_range_month_actual(self, num):
        """output range actual month and range month num+=1 """
        range_month = CalendarEvent(self.get_date_add_month(0), num).range_months()
        return range_month

    def get(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['title'] = kwargs['day']
        if kwargs['day'] in context['range_month']:
            return render(request, self.templates, context)
        raise Http404('No page')


class RegisterHourDetailView(RegisterHoursView, LoginRequiredMixin):
    '''render view to confirm selected date and hours register visit'''
    templates = 'reg_page/register_hours_detail.html'

    def get(self, request, *args, **kwargs):
        '''choice user for superuser'''
        form = UsernameForm()

        'context'
        context = self.get_context(request, *args, **kwargs)
        context['title'] = kwargs['hour']
        context['hour'] = kwargs['hour']
        context['exist'] = self.get_exist(request, *args, **kwargs)
        context['form'] = form

        # print(self.get_month(-1))

        if kwargs['day'] in context['range_month'] and kwargs['hour'] in context['hours']:
            return render(request, self.templates, context)
        raise Http404('No page')

    def get_exist(self, request, *args, **kwargs):
        """if exist data and time in databases output 'exist'.
        Function to don't duplicate value
        and don't register second time in the same value """
        data = self.variables_data('data', request, *args, **kwargs)
        time = self.variables_data('time', request, *args, **kwargs)
        data_created = Event.objects.filter(data=data).first()
        all_objects = self.all_object_time_Event()

        if data_created is not None:
            time_created = Time.objects.filter(time=time, data_event_id=data_created.id).first()
            if time_created in all_objects:
                return 'exist'
            else:
                return "no exist"
        else:
            return "no exist"

    def post(self, request, *args, **kwargs):

        if 'Register' in request.POST:

            """variables"""
            data = self.variables_data('data', request, *args, **kwargs)
            time = self.variables_data('time', request, *args, **kwargs)
            user_id = self.active_user(request).id

            """create date Event"""
            self.createEvent_data(data, request, *args, **kwargs)

            """read data from create Event"""
            data_created_id = Event.objects.filter(data=data).first().id

            """if super user is logged
            Create time Event"""
            if request.user.is_superuser:
                form = UsernameForm(request.POST)
                context_form = {'form': form}
                context = self.get_context(request, *args, **kwargs)
                context.update(context_form)
                username = request.POST['username']
                user = User.objects.filter(username=username).first()

                try:
                    self.createEvent_time(data, time, data_created_id, user.id, request, *args, **kwargs)
                    context = self.get_context(request, *args, **kwargs)
                    return render(request, self.templates, context)

                except:
                    context['error'] = 'error'

                finally:
                    return render(request, self.templates, context)
            else:

                """create time Event"""
                self.createEvent_time(data, time, data_created_id, user_id, request, *args, **kwargs)
                return redirect('list_view')
        else:
            context = self.get_context(request, *args, **kwargs)
            return render(request, self.templates, context)


class RegPageListViewSuperUser(ListView, ViewMixed, LoginRequiredMixin):
    """output list Views register visit"""

    template_name = 'reg_page/list_view.html'
    context_object_name = 'objects'
    paginate_by = 9
    extra_context = {
        'data_now': datetime.now().date(),
        'time_now': datetime.now().time(),
        'month': datetime.now().strftime("%B"),
        'year': datetime.now().year,
                     }

    def get_queryset(self):
        """output all registered queryset when login is superuser
        or output queryset register visit for active user"""
        active_user = self.active_user(request=self.request)
        user_id = self.active_user(self.request).id
        times = Time.objects.all()
        datanow = datetime.now().date()

        if active_user.is_superuser:
            return times.filter(data_event__data__gt=str(datanow)).order_by('data_event__data', 'time')

        else:
            return times.filter(user_id=user_id, data_event__data__gt=str(datanow)).order_by('data_event__data', 'time')


    def post(self, request, *args, **kwargs):
        """When user click in button will delete value from db """

        if request.method == 'POST':
            object_id = request.POST['Delete']
            times_id = Time.objects.filter(id=object_id).first()
            times_id.delete()
            messages.success(request, "You'ar deleted visit")
            return redirect('list_view')



