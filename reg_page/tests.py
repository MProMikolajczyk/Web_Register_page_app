from django.test import TestCase
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import (
    Event,
    Time,
    CalendarEvent,
)

class EventModelTest(TestCase):
    def test_res_data_past(self):
        '''return false if user choice yesterday data or past data '''
        past = datetime.now().date() - timedelta(days=1)
        event = Event(data=past)
        self.assertIs(event.res_data(), False)

    def test_res_data_future(self):
        '''return True if user choice next data'''
        future = datetime.now().date() + timedelta(days=1)
        event = Event(data=future)
        self.assertIs(event.res_data(), True)

    def test_res_data_equal(self):
        '''return TRue if user choice today data'''
        equal = datetime.now().date()
        event = Event(data=equal)
        self.assertIs(event.res_data(), True)


class TimeModelTest(TestCase):
    '''return false if choice data is earlier then data now and choice time is earlier them time now'''
    event = Event(data=datetime.now().date())
    user = User.objects.filter(username='User').first()

    def test_res_time_past(self):
        """return false if choice time is earlier then time now"""
        time_event = Time(time=(datetime.now() - timedelta(hours=1)).time(), user_id=self.user.id, data_event=self.event)
        self.assertIs(time_event.res_time(), False)

    def test_res_timet_equal(self):
        """return True if choice time is equal time now"""
        time_event = Time(time=datetime.now().time(), user_id=self.user.id, data_event=self.event)
        self.assertIs(time_event.res_time(), True)

    def test_res_time_future(self):
        """return True if choice time is later then time now"""
        time_event = Time(time=(datetime.now() + timedelta(hours=1)).time(), user_id=self.user.id, data_event=self.event)
        self.assertIs(time_event.res_time(), True)

class CalendarEventTest(TestCase):

    test_actual_date = datetime(2019, 6, 1)
    cal = CalendarEvent(test_actual_date, 3)
    cal_28 = CalendarEvent(test_actual_date, 28)

    def test_name_actual_month(self):
        '''chcek name of actual month'''
        self.assertEqual(self.cal.name_actual_month(), "June")

    def test_add_month_3_month(self):
        "check name of month when add 3 month"
        self.assertEqual(self.cal.add_month().strftime("%B"), "September")

    def test_add_month_28_month(self):
        "check name of month when add 28 month"
        self.assertEqual(self.cal_28.add_month().strftime("%B"), "October")

    def test_sub_month_3_month(self):
        "check name of month when sub 3 month"
        self.assertEqual(self.cal.sub_month().strftime("%B"), "March")

    def test_sub_month_28_month(self):
        "check name of month when sub 28 month"
        self.assertEqual(self.cal_28.sub_month().strftime("%B"), "February")

    def test_year(self):
        """check int value of year"""
        self.assertEqual(self.cal.year(), 2019)

    def test_range_months(self):
        """check quantity of days in given month"""
        self.assertEqual(self.cal.range_months(), 30)








# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)
#
#
# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )
#
#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )
#
#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )
#



# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         """
#         The detail view of a question with a pub_date in the future
#         returns a 404 not found.
#         """
#         future_question = create_question(question_text='Future question.', days=5)
#         url = reverse('polls:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_question(self):
#         """
#         The detail view of a question with a pub_date in the past
#         displays the question's text.
#         """
#         past_question = create_question(question_text='Past Question.', days=-5)
#         url = reverse('polls:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)
