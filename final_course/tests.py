from django.contrib.auth.models import User
from django.test import TestCase
import unittest

from final_course.models import UserProfile


# Create your tests here.
def test_valid_user_and_avatar_data(self):
    user = User.objects.create(username="test_user")
    # avatar_file = open("test_avatar.png", "rb") # optional
    profile = UserProfile(user=user)
    profile.save()

    assert UserProfile.objects.count() == 1
    assert UserProfile.objects.first().user == user
    # assert UserProfile.objects.first().avatar == "avatars/test_avatar.png"
