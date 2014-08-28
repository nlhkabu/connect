from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.views import login
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.six import StringIO
from django.utils.timezone import now

User = get_user_model()


def create_superuser():
    """
    Create a superuser (with moderator privileges) to initiate tests.
    """
    temp_io = StringIO() # Avoid cluttering test output

    call_command(
        "createsuperuser",
        interactive=False,
        email="superuser@test.test",
        stdout=temp_io,
    )

    superuser = User.objects.get(email="superuser@test.test")
    superuser.is_moderator = True

    return superuser


def create_active_standard_user(moderator,
                                email='standard@test.test',
                                first_name='standard',
                                last_name='user',
                                password='default'):
    """
    Create a standard user with an already activated account.
    """
    user = moderator.invite_new_user(email, first_name, last_name)
    user.password = password
    user.is_active = True
    user.activated_datetime = now()
    user.auth_token_is_used = True

    return user


def create_active_moderator(moderator,
                           email='moderator@test.test',
                           first_name='moderator',
                           last_name='user',
                           password='default'):
    """
    Create a moderator with an already activated account.
    """
    user = moderator.invite_new_user(email, first_name, last_name)
    user.password = password
    user.promote_to_moderator()

    user.is_active = True
    user.activated_datetime = now()
    user.auth_token_is_used = True

    return user


class TestTestingUsers(TestCase):
    """
    Test that the mock users are what they should be.
    """

    def test_that_test_superuser_is_superuser(self):
        superuser = create_superuser()
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_moderator)

    def test_that_test_moderator_is_moderator(self):
        superuser = create_superuser()
        moderator = create_active_moderator(superuser)
        self.assertTrue(moderator.is_moderator)

        moderators = Group.objects.get(name='moderators')
        groups = moderator.groups.all()
        self.assertIn(moderators, groups)

    def test_that_test_standard_user_is_standard_user(self):
        superuser = create_superuser()
        standard_user = create_active_standard_user(superuser)
        self.assertFalse(standard_user.is_moderator)

        moderators = Group.objects.get(name='moderators')
        groups = standard_user.groups.all()
        self.assertNotIn(standard_user, groups)


# Models.py

class UserModelTest(TestCase):

    #~def test_standard_user_can_be_promoted_to_moderator(self):

    def test_moderator_can_invite_new_user(self):
        superuser = create_superuser()
        user = superuser.invite_new_user(email='standard@test.test',
                                         first_name='standard',
                                         last_name='user')

    #~def test_standard_user_cannot_invite_new_user(self):
    #~def test_moderator_can_reinvite_user(self):
    #~def test_standard_user_cannot_reinvite_user(self):
    #~def test_moderator_can_approve_user_application(self):
    #~def test_standard_user_cannot_approve_user_application(self):
    #~def test_moderator_can_reject_user_application(self):
    #~def test_standard_user_cannot_reject_user_application(self):


#~class UserSkillTest(TestCase):

    #~def test_proficiency_percentage_calculates_correctly(self):

#~class UserLinkTest(TestCase):
#~
    #~def test_custom_save_method_sets_icon(self):
    #~def test_get_icon_method_gets_correct_icon(self):

#~class LinkBrandTest(TestCase):
    #~def test_custom_save_method_applies_new_brand_to_existing_userlinks(self):


# Forms.py

#~class FormValidationTest(TestCase):
    #~def test_email_availability_validation_passes_with_new_email(self):
    #~def test_email_availability_validation_fails_with_existing_email(self):
#~
#~class RequestInvitationFormValidationTest(TestCase):
    #~def test_closed_account_promts_custom_validation_message(self):
#~
#~class TestActivateAccountFormValidation(TestCase):
    #~def test_password_validation_fails_when_passwords_are_different(self):
    #~def test_password_validation_passes_when_passwords_are_same(self):
#~
#~class BaseSkillFormsetValidationTest(TestCase):
    #~def test_validation_fails_when_userskill_is_not_unique_to_user(self):
    #~def test_validation_passes_when_userskill_is_unique_to_user(self):
    #~def test_validation_fails_when_userskill_has_skill_but_no_proficiency(self):
    #~def test_validation_fails_when_userskill_has_proficicency_but_no_skill(self):
    #~def test_validation_passes_when_userskill_has_skill_and_proficiency(self):
    #~def test_validation_passes_when_both_skill_and_proficiency_are_empty(self):
#~
#~class BaseLinkFormsetValidationTest(TestCase):
    #~def test_validation_fails_when_link_url_is_not_unique_to_user(self):
    #~def test_validation_passes_when_link_url_is_unique_to_user(self):
    #~def test_validation_fails_when_link_anchor_is_not_unique_to_user(self):
    #~def test_validation_passes_when_link_anchor_is_unique_to_user(self):
    #~def test_validation_fails_when_link_has_anchor_but_no_url(self):
    #~def test_validation_fails_when_link_has_url_but_no_anchor(self):
    #~def test_validation_passes_when_link_has_url_and_anchor(self):
    #~def test_validation_passes_when_both_url_and_anchor_are_empty(self):
#~
#~class AccountSettingsFormValidationTest(TestCase):
    #~def test_current_password_matches_users_password(self):
    #~def test_validation_fails_if_user_tries_to_change_password_without_current_password(self):
    #~def test_validation_fails_if_user_tries_to_change_password_without_confirming_password(self):
    #~def test_password_validation_fails_when_passwords_are_different(self):
    #~def test_password_validation_passes_when_passwords_are_same(self):
#~
#~class CloseAccountFormValidationTest(TestCase):
    #~def test_current_password_matches_users_password(self):


# Utils.py

#~class AccountUtilsTest(TestCase):
    #~def test_create_inactive_user_is_not_active(self):
    #~def test_create_inactive_user_is_standard_user(self):
#~
    #~def test_reactivated_account_token_is_reset(self):


# Urls.py and views.py

#~class RequestInvitationTest(TestCase):
    #~def test_request_invitation_url_resolves_to_request_invitation_view(self):
    #~def test_requested_account_is_saved_as_inactive_user(self):


#~class ActivateAccountTest(TestCase):
    #~def test_activate_account_url_resolves_to_activate_account_view(self):
    #~def test_can_activate_account(self):
    #~def test_activated_account_redirects_to_correct_view(self):


#~class ProfileSettingsTest(TestCase):
    #~def test_profile_url_resolves_to_profile_settings_view(self):
    #~def test_profile_is_only_available_to_authenticated_users(self):
    #~def test_profile_form_is_prepopulated_with_users_data(self):
    #~def test_skills_formset_shows_users_skills(self):
    #~def test_links_formset_shows_users_links(self):
    #~def test_can_update_profile(self):
    #~def test_link_is_correctly_matched_to_brand(self):


#~class AccountSettingsTest(TestCase):
    #~def test_account_settings_url_resolves_to_account_settings_view(self):
    #~def test_account_settings_is_only_available_to_autheticated_users(self):
    #~def test_account_settings_form_is_rendered_to_page(self):
    #~def test_email_field_is_prepopulated_with_correct_email(self):
    #~def test_close_account_form_is_rendered_to_page(self):

    #~def test_update_account_url_resolves_to_update_account_view(self):
    #~def test_update_account_is_only_available_to_autheticated_users(self):
    #~def test_update_account_is_only_available_to_POST_data(self):
    #~def test_email_is_updated(self):
    #~def test_password_is_updated_if_submitted(self):
    #~def test_password_is_not_updated_if_it_is_not_submitted(self):

    #~def test_close_account_url_resolves_to_close_account_view(self):
    #~def test_close_account_is_only_available_to_autheticated_users(self):
    #~def test_close_account_is_only_available_to_POST_data(self):
    #~def test_can_close_account(self):
    #~def test_closed_account_is_inactive(self):
    #~def test_closed_account_redirects_to_correct_view(self):
