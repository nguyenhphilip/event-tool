from viewmodels.users.user_viewmodel import UserViewModelBase
from services import user_service

class RegisterViewModel(UserViewModelBase):
    def __init__(self):
        super().__init__()
        self.name = self.request_dict.name or ''
        self.email = self.email or ''
        self.password = self.password or ''
        
        # self.user = user_service.find_user_by_id(self.user_id)
        
    def validate(self):

        self.validate_email_and_password()
        if self.error:
            return

        if not self.name or not self.name.strip():
            self.error = 'You must specify a name.'
        elif len(self.password.strip()) < 5:
            self.error = 'The password must be at least 5 characters.'
        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email address already exists.'
        