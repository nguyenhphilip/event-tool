from viewmodels.users.user_viewmodel import UserViewModelBase
from services import user_service

class LoginViewModel(UserViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = None

    def validate(self):
        if not self.email or not self.password:
            self.error = "Email and password are required."
            return

        self.user = user_service.login_user(self.email, self.password)
        if not self.user:
            self.error = "Invalid email or password."