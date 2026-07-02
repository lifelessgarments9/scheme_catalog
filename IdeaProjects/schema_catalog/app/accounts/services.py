from django.contrib.auth.hashers import make_password

from .models import User


class AccountService:

    @staticmethod
    def get_profile(user_id: int) -> User:
        return User.objects.get(id=user_id)

    @staticmethod
    def update_profile(user_id: int, data: dict) -> User:
        allowed_fields = {"bio", "avatar"}
        clean = {k: v for k, v in data.items() if k in allowed_fields}
        User.objects.filter(id=user_id).update(**clean)
        return User.objects.get(id=user_id)

    @staticmethod
    def register(username: str, email: str, password: str) -> User:
        if User.objects.filter(username=username).exists():
            raise ValueError("Username already taken")
        if User.objects.filter(email=email).exists():
            raise ValueError("Email already registered")
        return User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )
