import re
from apps.account.models import User


def find_mentioned_users(text):
    mention_pattern = r"@(\w+)"
    return User.objects.filter(username__in=re.findall(mention_pattern, text))
