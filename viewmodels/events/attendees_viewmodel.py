from viewmodels.events.events_viewmodel_base import EventViewModelBase

class EventAttendeesViewModel(EventViewModelBase):
    def __init__(self, event_slug=None):
        super().__init__(event_slug)
        self.load_event()
        self.attendees = []
        self.not_authorized = False

        if not self.event:
            return

        # Restrict: only host (creator) can view attendee list
        if self.event.user_id != self.user_id:
            self.not_authorized = True
            return

        self.attendees = self.event.attendees