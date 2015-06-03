from urllib.parse import urlsplit

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from connect.accounts.models import UserLink, UserSkill, LinkBrand


def save_paired_items(request, user, formset, Model,
                      item_name, counterpart_name):
    """
    Handle saving skills or links to the database.
    """
    paired_items = []

    for form in formset:
        if form.is_valid():
            item = form.cleaned_data.get(item_name, None)
            counterpart = form.cleaned_data.get(counterpart_name, None)

            if item and counterpart:
                model_instance = Model(user=user)
                setattr(model_instance, item_name, item)
                setattr(model_instance, counterpart_name, counterpart)
                paired_items.append(model_instance)

    # Replace old pairs with new
    # Do this in a transaction to avoid a case where we delete the old
    # but cannot save the new
    try:
        with transaction.atomic():
            Model.objects.filter(user=user).delete()
            Model.objects.bulk_create(paired_items)
    except IntegrityError:
        messages.error(request, _('There was an error updating your profile.'))
        return redirect(reverse('accounts:profile-settings'))


def save_skills(request, user, formset):
    """Wrapper function to save paired skills and proficiencies."""
    save_paired_items(request, user, formset, UserSkill, 'skill',
                      'proficiency')


def save_links(request, user, formset):
    """Wrapper function to save paired link anchors and URLs."""
    save_paired_items(request, user, formset, UserLink, 'anchor', 'url')


def match_link_to_brand(user_links):
    """
    Attempt to match a user's links to recognised brands (LinkBrand).
    This functionality also exists as a custom save() method on the model.
    -- Use this with functions that create and update in bulk.
    """
    for link in user_links:
        domain = urlsplit(link.url).netloc

        try:
            brand = LinkBrand.objects.get(domain=domain)
            link.icon = brand
            link.save()

        except ObjectDoesNotExist:
            pass

    return user_links
