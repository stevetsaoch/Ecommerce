from account.models import UserBase
from django.test import TestCase, RequestFactory
from store.models import Category
from store.context_processors import categories


class StoreContextPorcessTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserBase.objects.create_user(email="a@a.com", user_name="steve", password="abc123123")
        
        return super().setUp()

    def test_categories(self):
        # Creating new item in category table
        Category.objects.create(id=1, name="Django", slug="django")
        _cateories = Category.objects.all()
        # fake request
        request = self.factory.get("/")
        test_categories = categories(request)

        self.assertEqual(list(_cateories), list(test_categories["categories"]))
