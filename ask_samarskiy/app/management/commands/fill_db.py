import os
from venv import faker
os.environ.setdefault['DJANGO_SETTINGS_MODULE'] = 'ask_samarskiy.settings'
from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, Tags, Questions, Answers, User, Like
from random import randint, choice


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)
        parser.add_argument('--answers', type=int, default=0)

    def create_profiles(self):
        name = factory.Faker('name')
        email = factory.Faker('email')
        passwd = factory.fuzzy.FuzzyText(length=16)
        for i in range(10):
            user = User.objects.create_user(name.generate(), email.generate(), passwd.fuzz())
            user.save()
            p = Profile.objects.create(user=user)
            p.save()

    def create_tags(self):
        tag_word = factory.fuzzy.FuzzyText(length=10)
        for i in range(50):
            tag = Tags.objects.create(title=tag_word, index=i)
            tag.save()

    def create_questions(self):
        tags = Tags.objects.all()
        profiles = Profile.objects.all()
        titles = factory.fuzzy.FuzzyText(length=30)
        text = factory.fuzzy.FuzzyText(length=100)
        likes = factory.fuzzy.FuzzyInteger(-100,100)
        for i in range(100):
            question = Questions.objects.create(title=titles.fuzz(),
                                               text=text.fuzz(),
                                               author=choice(profiles),
                                               likes=likes.fuzz())
            tag_number = randint(1, 8)
            for i in range(tag_number):
                tag = choice(tags)
                question.tags.add(tag)
            question.save()

    def create_answers(self):
        profiles = Profile.objects.all()
        text = factory.fuzzy.FuzzyText(length=100)
        correct = factory.fuzzy.FuzzyChoice(choices=[True, False])
        for question in Questions.objects.all():
            answer_count = randint(1, 10)
            for i in range(answer_count):
                a = Answers.objects.create(text=text.fuzz(), question=question, correct=correct.fuzz(),
                                          author=choice(profiles))
                a.save()

    def create_likes_obj(self, obj, profiles):
        rating = obj.likes
        if rating:
            like_count = randint(abs(rating), 2 * abs(rating))
            sign = rating / abs(rating)
            opposite_max = like_count - abs(rating)
            i = 0
            profile_ind = 0
            if sign > 0:
                while i > -opposite_max:
                    Like.objects.create(content_model=obj, sign=False,
                                        author=profiles[profile_ind])
                    i -= 1
                    profile_ind += 1
                while i < rating:
                    Like.objects.create(content_model=obj, sign=True,
                                        author=profiles[profile_ind])
                    i += 1
                    profile_ind += 1
            else:
                while i < opposite_max:
                    Like.objects.create(content_model=obj, sign=True,
                                        author=profiles[profile_ind])
                    i += 1
                    profile_ind += 1
                while i > rating:
                    Like.objects.create(content_model=obj, sign=False,
                                        author=profiles[profile_ind])
                    i -= 1
                    profile_ind += 1

    def create_likes(self):
        profiles = Profile.objects.all()
        questions = Questions.objects.all()
        answers = Answers.objects.all()
        for question in questions:
            self.create_likes_obj(question, profiles)
        for answer in answers:
            self.create_likes_obj(answer, profiles)

    def handle(self, *args, **options):
        self.create_profiles()
        self.create_tags()
        self.create_questions()
        self.create_answers()
        self.create_likes()