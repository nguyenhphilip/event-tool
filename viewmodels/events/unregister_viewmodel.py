from viewmodels.events.events_viewmodel_base import EventViewModelBase
from data.attendee import Attendee

class EventUnregisterViewModel(EventViewModelBase):
    def __init__(self):
        super().__init__()
        self.load_event()
        self.email = (self.request_dict.email or '').lower().strip()
        self.attendee = None

    def validate(self):
        if not self.email:
            self.error = "Email is required."
            return
        if not self.event:
            self.error = "Event not found."
            return
        self.attendee = self.session.query(Attendee).filter_by(event_id=self.event.id, email=self.email).first()
        if not self.attendee:
            self.error = "This email is not registered for the event."