from django.contrib.auth.backends import ModelBackend
from .models import UserProfile

class UserProfileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Get the user profile for the given username
            user_profile = UserProfile.objects.get(user__username=username)

            # Authenticate the user using the password provided
            if user_profile.user.check_password(password):
                return user_profile.user

        except UserProfile.DoesNotExist:
            # If the user profile does not exist, return None
            return None

    