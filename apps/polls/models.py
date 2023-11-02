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
        ordering = ['-pub_date']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(
        verbose_name=_("No. of Votes"),
        default=0,
    )

    def __str__(self):
        return self.choice_text

    def vote_choice(self, user):
        """
        Add a vote to the choice
        """
        if not self.question.has_user_voted(user):
            self.votes += 1
            self.save()
            self.question.voted_by.add(user)
            self.question.save()
