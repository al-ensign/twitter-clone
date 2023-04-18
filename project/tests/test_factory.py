import factory
from tweets.models import Tweet, Page, Tag
from django.contrib.auth import get_user_model


User = get_user_model()


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    title = factory.Faker("word")
    description = factory.Faker("word")
    owner = factory.Iterator(User.objects.all())
    is_private = factory.Faker("pybool")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create and extracted:
            for tag in extracted:
                self.tags.add(tag)


class TweetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Tweet

    owner = factory.Iterator(Page.objects.all())
    text = factory.Faker('word')
