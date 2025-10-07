from viewmodels.events.events_viewmodel_base import EventViewModelBase
from datetime import datetime

class EventCreateViewModel(EventViewModelBase):
    def __init__(self):
        super().__init__()
        self.eventname = self.request_dict.eventname or ''
        self.location = self.request_dict.location or ''
        self.description = self.request_dict.description or ''
        self.event_datetime = self.request_dict.event_datetime or ''

        self.is_recurring = self.request.form.get("is_recurring") == "true"
        self.num_weeks = int(self.request.form.get("num_weeks", 1))

        try:
            self.parsed_datetime = datetime.strptime(self.event_datetime, "%Y-%m-%dT%H:%M")
        except ValueError:
            self.parsed_datetime = None

    def validate(self):
        if not self.eventname:
            self.error = "Event name is required."
        elif not self.location:
            self.error = "Location is required."
        elif not self.description:
            self.error = "Description is required."

        try:
            self.parsed_datetime = datetime.strptime(self.event_datetime, "%Y-%m-%dT%H:%M")
        except Exception:
            self.error = "Invalid date/time format."