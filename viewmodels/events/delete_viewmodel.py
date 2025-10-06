from viewmodels.events.events_viewmodel_base import EventViewModelBase

class EventDeleteViewModel(EventViewModelBase):
    def __init__(self):
        super().__init__()
        self.load_event()

    def validate(self):
        if not self.event:
            self.error = "Event not found."
            return
        if self.event.user_id != self.user_id:
            self.error = "Not authorized to delete this event."