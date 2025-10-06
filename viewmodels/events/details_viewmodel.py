from viewmodels.events.events_viewmodel_base import EventViewModelBase

class EventDetailsViewModel(EventViewModelBase):
    def __init__(self, event_slug=None):
        super().__init__(event_slug)
        self.load_event()
        self.attendee_emails = ""
        if self.event:
            self.attendee_emails = ", ".join([a.email for a in self.event.attendees])