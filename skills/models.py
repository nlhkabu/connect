from django.contrib.auth.models import User
from django.db import models

class Skill(models.Model):
    """
    Represents a skill in the community.
    """
    name = models.CharField(max_length=100)
    owner = models.ManyToManyField(User, through='UserSkill')

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """
    How proficient an individual user is at a particular skill.
    This model joins User and Skill ('through' table).
    """

    BEGINNER = 10
    INTERMEDIATE = 20
    ADVANCED = 30
    EXPERT = 40

    PROFICIENCY_CHOICES = (
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (EXPERT, 'Expert'),
    )

    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    proficiency = models.CharField(max_length=2,
                                      choices=PROFICIENCY_CHOICES,
                                      default=BEGINNER)

    def __str__(self):
        return '{} - {}'.format(self.user, self.skill)
