from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from zap.factories import UserFactory, MeepFactory
from zap.models import Meep


class MeepViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.meep = MeepFactory(user=self.user1, body='Test meep')

    def test_home_view_authenticated_user(self):
        meep1 = MeepFactory(user=self.user1)
        meep2 = MeepFactory(user=self.user2)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, meep1.body)
        self.assertContains(response, meep2.body)

    def test_home_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_list_view_authenticated_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_authenticated_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('profile', args=[self.user1.id]))
        self.assertTrue(response.context['user'].is_authenticated)
        home_response = self.client.get(reverse('home'))
        self.assertEqual(home_response.status_code, 200)

    def test_followers_view_authenticated_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('followers', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)

    def test_follows_view_authenticated_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('follows', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)

    def test_login_user_view(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {'username': self.user1.username, 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout_user_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_register_user_view(self):
        response = self.client.post(reverse('register'),
                                    {'username': 'newuser',
                                     'password1': 'newpassword',
                                     'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)
        home_response = self.client.get(reverse('home'))
        self.assertEqual(home_response.status_code, 200)


    def test_update_user_view_authenticated_user(self):
        response = self.client.post(reverse('update_user'), {'username': 'updateduser'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_meep_like_view_authenticated_user(self):
        meep = MeepFactory(user=self.user2)
        response = self.client.get(reverse('meep_like', args=[meep.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_meep_show_view(self):
        meep = MeepFactory(user=self.user1)
        response = self.client.get(reverse('meep_show', args=[meep.id]))
        self.assertEqual(response.status_code, 200)

    def test_unfollow_view_authenticated_user(self):
        response = self.client.get(reverse('unfollow', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_follow_view_authenticated_user(self):
        response = self.client.get(reverse('follow', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_meep_delete_view_authenticated_user(self):
        self.client.force_login(self.user1)
        redirect_url = reverse('home')
        response = self.client.post(reverse('meep_delete', args=[self.meep.id]), HTTP_REFERER=redirect_url)
        self.assertEqual(Meep.objects.filter(id=self.meep.id).exists(), False)
        self.assertRedirects(response, redirect_url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Meep successfully deleted', messages)

    def test_meep_edit_view_authenticated_user(self):
        meep = MeepFactory(user=self.user1)
        response = self.client.post(reverse('meep_edit', args=[meep.id]), {'body': 'Updated body'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_search_view(self):
        response = self.client.post(reverse('search'), {'search': 'test'})
        self.assertEqual(response.status_code, 200)
