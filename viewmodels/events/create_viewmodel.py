from datetime import datetime
from viewmodels.events.events_viewmodel_base import EventViewModelBase

class EventCreateViewModel(EventViewModelBase):
    def __init__(self):
        super().__init__()
        self.eventname = self.request_dict.eventname or ''
        self.location = self.request_dict.location or ''
        self.description = self.request_dict.description or ''
        self.event_datetime = self.request_dict.event_datetime or ''
        self.parsed_datetime = None

    def validate(self):
        if not self.eventname or not self.location or not self.description:
            self.error = "All fields are required."
            return

        try:
            self.parsed_datetime = datetime.strptime(self.event_datetime, "%Y-%m-%dT%H:%M")
        except Exception:
            self.error = "Invalid datetime format."