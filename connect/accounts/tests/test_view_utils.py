from django.contrib.auth import get_user_model
from django.forms.formsets import formset_factory

from connect.accounts.factories import (
    BrandFactory, SkillFactory, UserLinkFactory, UserFactory
)
from connect.accounts.forms import (
    BaseLinkFormSet, BaseSkillFormSet, LinkForm, SkillForm
)
from connect.accounts.models import UserLink, UserSkill
from connect.accounts.view_utils import (
    match_link_to_brand, save_links, save_skills
)
from connect.tests import BoostedTestCase as TestCase


User = get_user_model()


class ViewUtilsTest(TestCase):
    def setUp(self):
        self.standard_user = UserFactory()

    def test_can_save_skills(self):
        django = SkillFactory(name='django')
        python = SkillFactory(name='python')

        SkillFormSet = formset_factory(SkillForm, max_num=None,
                                       formset=BaseSkillFormSet)

        formset = SkillFormSet(
            data={
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-0-skill': django.id,
                'form-0-proficiency': UserSkill.BEGINNER,
                'form-1-skill': python.id,
                'form-1-proficiency': UserSkill.INTERMEDIATE,
            }
        )

        save_skills(self.client.request, self.standard_user, formset)

        user = User.objects.get(id=self.standard_user.id)
        user_skills = UserSkill.objects.filter(user=user)

        skill_names = [skill.skill for skill in user_skills]
        skill_proficencies = [skill.proficiency for skill in user_skills]

        self.assertEqual(len(user_skills), 2)
        self.assertIn(django, skill_names)
        self.assertIn(python, skill_names)
        self.assertIn(UserSkill.BEGINNER, skill_proficencies)
        self.assertIn(UserSkill.INTERMEDIATE, skill_proficencies)

    def test_can_save_links(self):
        LinkFormSet = formset_factory(LinkForm, max_num=None,
                                      formset=BaseLinkFormSet)

        formset = LinkFormSet(
            data={
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-0-anchor': 'Anchor 1',
                'form-0-url': 'http://link1.com/',
                'form-1-anchor': 'Anchor 2',
                'form-1-url': 'http://link2.com/',
            }
        )

        save_links(self.client.request, self.standard_user, formset)

        user = User.objects.get(id=self.standard_user.id)
        user_links = UserLink.objects.filter(user=user)

        link_anchors = [link.anchor for link in user_links]
        link_urls = [link.url for link in user_links]

        self.assertEqual(len(user_links), 2)
        self.assertIn('Anchor 1', link_anchors)
        self.assertIn('Anchor 2', link_anchors)
        self.assertIn('http://link1.com/', link_urls)
        self.assertIn('http://link2.com/', link_urls)

    def test_can_match_link_to_brand(self):
        github = BrandFactory()
        link_user = UserFactory()
        link = UserLinkFactory(
            user=link_user,
            anchor='Github',
            url='http://github.com/myaccount/',
        )
        userlinks = [link]

        match_link_to_brand(userlinks)
        link = UserLink.objects.get(user=link_user)

        self.assertEqual(link.icon, github)
