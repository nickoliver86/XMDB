from django.test import TestCase
from django.test.client import Client
from django.http import HttpResponse
from django_test_mixins import HttpCodeTestCase, FormValidationTestCase
from movies.models import *
from movies.views import *
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.models import User
import os
import pdb
# Create your tests here.

class HomePageTestCase(TestCase):

    fixtures = ['dump.json']

    def setUp(self):
        self.client = Client()

    def test_200_on_landing(self):
        response = self.client.get(reverse('movies:IndexTest'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post('/signin/', {'username': 'nick', 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_unsuccessful_login(self):
        response = self.client.post('/signin/', {'username': 'notindb', 'password': 'asdfg'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, HttpResponse('Invalid login details supplied.').content)
        self.assertEqual(response.content, b'Invalid login details supplied.')

class SignUpTestCase(HttpCodeTestCase, FormValidationTestCase):
    def form_params(self):
        return {'username': 'zzz', 'email': 'zzz@test.com',
                'password1': 'password', 'password2': 'password'}

    def test_user_created(self):
        params = self.form_params()
        expected_username = params['username']
        response = self.client.post(reverse('movies:UserSignUp'), self.form_params())
        self.assertTrue(User.objects.filter(username=expected_username).exists(),
                        "User was not created.")

class MovieListTestCase(TestCase):

    fixtures = ['dump.json']

    def test_200_when_signed_in(self):
        self.client.post('/signin/', {'username': 'nick', 'password': 'password'})
        response = self.client.get(reverse('movies:MovieList'))
        self.assertEqual(response.status_code, 200)

    def test_302_when_not_signed_in(self):
        response = self.client.get(reverse('movies:MovieList'))
        self.assertEqual(response.status_code, 302)

    def test_movie_list_content(self):
        self.client.login(username='nick', password='password')
        response = self.client.get(reverse('movies:MovieList'))
        self.assertNotEqual(response.content, '')

class SearchTestCase(TestCase):

    fixtures = ['dump.json']

    def test_search_returns_movie_summary(self):
        response = self.client.post('/search/', {'search_query': 'Ted'}, follow=True)
        self.assertContains(response, '<h2>Ted (2012)</h2>')

    def test_search_adds_to_db(self):
        try:
            Movie.objects.get(name='Ted')
            self.fail("Ted was already in the db so search wasn't called")
        except Movie.DoesNotExist:
            print("\nSearch being called...")
            self.client.post('/search/', {'search_query': 'Ted'}, follow=True)
            try:
                Movie.objects.get(name='Ted')
                print("Ted was found and added to db successfully")
            except Movie.DoesNotExist:
                self.fail("Something went wrong, Ted was not added to the db")

    def test_fail_on_summary_when_not_logged_in(self):
        try:
            response = self.client.get('/movie_summary/tt1853728/')
            self.fail("You should not be able to view this page before logging in.")
        except AttributeError:
            None

    def test_get_movie_summary_by_url(self):
        #Django Unchained is a movie in the db with imdbId: tt1853728
        #Terminator is not in the db with imdbId: tt1994570
        self.client.login(username='nick', password='password')
        response = self.client.get('/movie_summary/tt1853728/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Django Unchained (2012)</h2>')
        try:
            self.client.get('/movie_summary/tt1994570/')
            self.fail('Terminator is not in db so you should not see this summary without searching.')
        except AttributeError:
            None