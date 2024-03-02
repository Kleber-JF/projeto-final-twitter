from django.test import TestCase
from zap.factories import UserFactory, MeepFactory
from zap.models import Meep, Profile

class MeepProfileTestCase(TestCase):

    def setUp(self):
        # Configuração inicial para todos os testes, se necessário
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_create_meep(self):
        # Create a Meep instance using the factory
        meep = MeepFactory(user=self.user1)

        # Check if Meep is saved correctly
        self.assertEqual(Meep.objects.count(), 1)
        self.assertEqual(meep.user, self.user1)
        self.assertIsNotNone(meep.created_at)

    def test_add_likes(self):
        # Create a Meep using the factory
        meep = MeepFactory(user=self.user1)

        # Create another user using the factory for liking
        liker = UserFactory()

        # Add likes to the Meep
        meep.likes.add(liker)

        # Check if likes are correctly added
        self.assertEqual(meep.number_of_likes(), 1)

    def test_create_profile(self):
        # Check if a Profile is created for the test user
        profile = Profile.objects.get(user=self.user1)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.follows.count(), 1)  # Check if the user follows themselves

    def test_modify_profile(self):
        # No need to create a Profile using the factory, as it should be created automatically by the signal
        # Retrieve the profile associated with user1
        profile = Profile.objects.get(user=self.user1)

        # Modify Profile fields and check if changes are reflected
        profile.profile_bio = 'New bio'
        profile.save()

        # Retrieve the profile again to ensure changes are reflected
        updated_profile = Profile.objects.get(user=self.user1)
        self.assertEqual(updated_profile.profile_bio, 'New bio')

    def test_followers(self):
        # Make the test user follow user2
        profile = Profile.objects.get(user=self.user1)
        profile.follows.add(Profile.objects.get(user=self.user2))

        # Check if the follow relationship is correctly established
        self.assertEqual(profile.follows.count(), 2)  # Including the self-follow

    def test_signal_functionality(self):
        # Create a new user using the factory and check if a Profile is created for them via the signal
        new_user = UserFactory()
        self.assertIsNotNone(Profile.objects.get(user=new_user))
