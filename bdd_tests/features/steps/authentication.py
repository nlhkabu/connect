from behave import *

@given('the login page')
def step_impl(context):
    assert False

@when('we put in a valid username and password')
def step_impl(context):
    assert False

@then('we are redirected to the dashboard')
def step_impl(context):
    assert False

@when('we put in an invalid email')
def step_impl(context):
    assert False

@then('we are told it is invalid')
def step_impl(context):
    assert False

@when('we put in an unregistered email')
def step_impl(context):
    assert False

@then('we are told it is unregistered')
def step_impl(context):
    assert False

@when('we put in the incorrect password')
def step_impl(context):
    assert False

@then('we are told it is incorrect')
def step_impl(context):
    assert False
