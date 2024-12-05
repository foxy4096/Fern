import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Fern.settings")
import django

django.setup()

import random
from faker import Faker
from mdgen import MarkdownPostProvider

from django.utils import timezone
from apps.account.models import User, UserProfile
from django.core.files import File
import requests
from django.core.files.base import ContentFile
from django.core.files import File
from apps.forum.models import Category, Post, Thread
from apps.polls.models import Question, Choice

fake = Faker()
fake.add_provider(MarkdownPostProvider)


def generate_unique_image_url(width=200, height=200):
    return f"https://picsum.photos/{width}/{height}?random={random.randint(1, 1000)}"


def download_image(url):
    response = requests.get(url)
    return ContentFile(response.content) if response.status_code == 200 else None

def create_dummy_users_with_profiles(num_users):
    users = []
    for _ in range(num_users):
        # Create a new user
        user = User.objects.create(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
        )
        image_url = generate_unique_image_url()
        image = download_image(image_url)

        # Create a user profile for the user
        profile = user.userprofile
        profile.bio=fake.paragraph()
        profile.dark_mode=fake.boolean()
        profile.location=fake.city()
        profile.website=fake.url()
        profile.rank=fake.random_int(min=0, max=100)
        profile.avatar=File(image, name=f'{fake.user_name()}_profile_picture.jpg')
        profile.save()
        users.append(user)

    return users

def create_dummy_categories(num_categories):
    return [
        Category.objects.get_or_create(name=fake.word())[0]
        for _ in range(num_categories)
    ]


def create_dummy_threads(num_threads, categories, users):
    threads = []
    for _ in range(num_threads):
        category = random.choice(categories)
        thread = Thread.objects.create(
            title=fake.sentence(),
            category=category,
            creator=random.choice(users),
            is_locked=random.choice([True, False]),
        )
        threads.append(thread)

        for _ in range(5):
            Post.objects.create(
                thread=thread,
                body=fake.post(size='medium'),
                author=random.choice(users),
            )
    return threads


def create_dummy_questions_and_choices(num_questions, choices_per_question, users):
    questions = []
    choices = []
    for _ in range(num_questions):
        created_by = random.choice(users)
        question = Question.objects.create(
            question_text=fake.sentence(),
            pub_date=timezone.now(),
            created_by=created_by,
        )
        questions.append(question)

        for _ in range(choices_per_question):
            choice = Choice.objects.create(question=question, choice_text=fake.word())
            question.voted_by.add(random.choice(users))
            choice.voted_by.add(random.choice(users))
            choices.append(choice)  # Add the choice to the list
    return questions, choices


def generate_dummy_data():
    num_users = 10
    num_categories = 3
    num_threads = 10
    num_questions = 5
    choices_per_question = 3

    users = create_dummy_users_with_profiles(num_users)
    categories = create_dummy_categories(num_categories)
    threads = create_dummy_threads(num_threads, categories, users)
    questions, choices = create_dummy_questions_and_choices(
        num_questions, choices_per_question, users
    )

    # Simulate voting for some questions
    for _ in range(num_questions):
        user = random.choice(users)
        choice = random.choice(choices)
        choice.vote(user)

    print(
        f"Generated {num_users} users, {num_categories} categories, {num_threads} threads, {num_questions} questions, and {num_questions * choices_per_question} choices."
    )


if __name__ == "__main__":
    generate_dummy_data()
