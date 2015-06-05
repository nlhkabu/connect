from datetime import datetime
from datetime import timedelta
from behave import *

from django.utils import timezone

from connect.moderation.factories import LogFactory
from connect.moderation.models import ModerationLogMsg


# Background
@given('the following logs exist')
def impl(context):

    # As we are querying these through the local timezone, we need to create
    # these based on our local time for our tests to work

    local_tz = timezone.get_current_timezone()
    today = timezone.now().astimezone(local_tz)

    yesterday = today - timedelta(days=1)
    three_days_ago = today - timedelta(days=3)
    one_month_ago = today - timedelta(days=30)
    two_months_ago = today - timedelta(days=60)

    LogFactory(msg_datetime=today) # Defaults to invitation
    LogFactory(msg_datetime=yesterday) # Defaults to invitation
    LogFactory(msg_type=ModerationLogMsg.REINVITATION, msg_datetime=yesterday)
    LogFactory(msg_datetime=three_days_ago) # Defaults to invitation
    LogFactory(msg_type=ModerationLogMsg.BANNING, msg_datetime=one_month_ago)
    LogFactory(msg_type=ModerationLogMsg.WARNING, msg_datetime=two_months_ago)


# Unique to Scenario: User views logs page
@then('I see a table with six logs in it')
def impl(context):
    assert context.browser.is_element_present_by_css('table.logs-table')
    logs = context.browser.find_by_css('table.logs-table tbody tr')
    assert len(logs) == 6


# Unique to Scenario Outline: Filter logs by type and period
@then('I see "{count}" logs')
def impl(context, count):
    logs = context.browser.find_by_css('table.logs-table tbody tr')
    assert len(logs) == int(count)


# Unique to Scenario: Date fields appear when 'custom' period is selected
@then('the "{field_name}" field appears')
def impl(context, field_name):
    field_name = field_name.replace(" ", "_")
    assert context.browser.is_element_present_by_name(field_name)


# Unique to Scenario: Filter logs by custom date range
@when('I input a date from a month ago in the start date field')
def impl(context):
    date = datetime.today() - timedelta(days=35)
    date_as_string = date.strftime('%d/%m/%Y')
    context.browser.fill('start_date', date_as_string)

@when('I input todays date in the end date field')
def impl(context):
    today = datetime.today()
    today_as_string = today.strftime('%d/%m/%Y')
    context.browser.fill('end_date', today_as_string)


# Unique to Scenario: Attempt to filter logs by custom date range, without specifying a date
@when('I do not select a date')
def impl(context):
    pass







