from django.db import models
from apps.forum.models import Thread
from django.utils.translation import gettext_lazy as _
from apps.account.models import User, get_sentinel_user


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now=True)
    created_by = models.ForeignKey(
        verbose_name=_("Created By"),
        to=User,
        related_name="questions",
        on_delete=models.SET(get_sentinel_user),
    )
    voted_by = models.ManyToManyField(
        verbose_name=_("Votes"), to=User, blank=True, related_name="voted_questions"
    )

    def __str__(self):
        return self.question_text

    def has_user_voted(self, user):
        # Check if the user has voted on the question.
        return self.voted_by.filter(pk=user.pk).exists()

    class Meta:
        ordering = ["-pub_date"]


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(
        verbose_name=_("No. of Votes"),
        default=0,
    )
    voted_by = models.ManyToManyField(
        verbose_name=_("Votes"), to=User, blank=True, related_name="voted_choices"
    )

    def __str__(self):
        return self.choice_text

    def vote_percentage(self):
        total_votes = self.question.voted_by.count()
        
        if total_votes == 0:
            return '0.00'  # Return a string with two decimal places
        
        percentage = (self.votes / total_votes) * 100
        return '{:.2f}'.format(percentage)

    def vote(self, user):
        if not self.question.has_user_voted(user):
            self.votes += 1
            self.voted_by.add(user)
            self.question.voted_by.add(user)
            self.question.save()
            self.save()
