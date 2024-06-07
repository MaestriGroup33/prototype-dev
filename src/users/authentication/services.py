from django.contrib.auth.backends import ModelBackend
from src.users.models import User
from src.modules.core.profiles.models import Profile


class UserAuthCPF(ModelBackend):
    def authenticate(self, request, cpf: str, password: str, **kwargs):

        print("this is that", cpf, password)

        try:
            profile: Profile = Profile.objects.get(cpf=cpf)
            print("This is it: ", profile)
            user = User.objects.get(profile=profile)
        except User.DoesNotExist or Profile.DoesNotExist:
            return None

        print("checking password")
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
