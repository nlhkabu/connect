from urllib.parse import urlsplit
from .models import UserLink, UserSkill, LinkBrand


def save_paired_items(user, formset, Model, item_name, counterpart_name):
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
    Model.objects.filter(user=user).delete()
    Model.objects.bulk_create(paired_items)


def save_skills(user, formset):
    """Wrapper function to save paired skills and proficiencies."""
    save_paired_items(user, formset, UserSkill, 'skill', 'proficiency')


def save_links(user, formset):
    """Wrapper function to save paired link anchors and URLs."""
    save_paired_items(user, formset, UserLink, 'anchor', 'url')


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

        except:
            pass

    return user_links
