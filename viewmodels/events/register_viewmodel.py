from viewmodels.events.events_viewmodel_base import EventViewModelBase

class EventRegisterViewModel(EventViewModelBase):
    def __init__(self):
        super().__init__()
        self.load_event()
        self.name = self.request_dict.name or ''
        self.email = (self.request_dict.email or '').lower().strip()

    def validate(self):
        if not self.name or not self.email:
            self.error = "Name and email are required."