# -*- coding: utf-8 -*-

from django.http.response import Http404
from django.utils.text import slugify
from django_testing.testcases.users import SingleUserTestCase
from python_tools.random_utils import random_alphanum

from tests.test_models.models import TestManagerModel

from .test_models.models import TestModel
from django_testing.user_utils import create_user


class CommonManagerTests(SingleUserTestCase):

    def test_get_or_none(self):
        """Getting an object which returns None if one is not found."""
        test_model = TestModel.objects.create(created_user=self.user,
                                some_unique_field=random_alphanum(),
                                some_unique_field_default=random_alphanum())
        test_model_db = TestModel.objects.get_or_none(id=test_model.id)
        self.assertEqual(test_model, test_model_db)

        self.assertIsNone(TestModel.objects.get_or_none(id=1234567890))

    def test_get_by_id(self):
        """Test getting an object by id."""
        test_model = TestModel.objects.create(created_user=self.user,
                                some_unique_field=random_alphanum(),
                                some_unique_field_default=random_alphanum())
        test_model_db = TestModel.objects.get_by_id(id=test_model.id)
        self.assertEqual(test_model, test_model_db)

    def test_get_by_id_or_404(self):
        """Test getting an object by id."""

        with self.assertRaises(Http404):
            TestModel.objects.get_by_id_or_404(id=123456780)

    def test_get_by_slug(self):
        """Test model manager get by slug."""
        slug = slugify(random_alphanum())
        obj = TestManagerModel.objects.create(created_user=self.user,
                                              slug=slug)
        obj_db = TestManagerModel.objects.get_by_slug(slug=slug)
        self.assertEqual(obj, obj_db)

    def test_get_by_slug_or_404(self):
        """Test model manager get by slug."""
        with self.assertRaises(Http404):
            TestManagerModel.objects.get_by_slug_or_404(slug='123455678')

    def test_get_by_token(self):
        """Test model manager get by token."""
        token = random_alphanum()
        obj = TestManagerModel.objects.create(created_user=self.user,
                                              token=token)
        obj_db = TestManagerModel.objects.get_by_token(token=token)
        self.assertEqual(obj, obj_db)

    def test_get_by_token_or_404(self):
        """Test model manager get by token."""
        with self.assertRaises(Http404):
            TestManagerModel.objects.get_by_token_or_404(token=123455678)

    def test_get_by_user(self):
        """Test model manager get by user."""
        user = create_user()
        obj = TestManagerModel.objects.create(created_user=self.user,
                                              user=user)
        obj_db = TestManagerModel.objects.get_by_user(user=user)
        self.assertEqual(obj, obj_db[0])

    def test_is_slug_available(self):
        """Test if a slug is available."""
        self.assertTrue(TestManagerModel.objects.is_slug_available(
                                                    slug=random_alphanum()))

    def test_not_is_slug_available(self):
        """Test if a slug is not available."""
        slug = slugify(random_alphanum())
        TestManagerModel.objects.create(created_user=self.user,
                                        slug=slug)
        self.assertFalse(TestManagerModel.objects.is_slug_available(slug=slug))

    def test_get_next_slug(self):
        """Test getting next available slug."""
        slug = slugify(random_alphanum())
        TestManagerModel.objects.create(created_user=self.user,
                                        slug=slug)
        next_slug = TestManagerModel.objects.get_next_slug(slug=slug)
        self.assertEqual(next_slug, '{0}-1'.format(slug))