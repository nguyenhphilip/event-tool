from viewmodels.shared.viewmodelbase import ViewModelBase

class UserViewModelBase(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.email = self.request_dict.email or ''
        self.password = self.request_dict.password or ''

    def validate_email_and_password(self):
        if not self.email:
            self.error = "You must specify an email."
        elif not self.password:
            self.error = "You must specify a password."