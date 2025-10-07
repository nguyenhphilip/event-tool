from datetime import datetime
from viewmodels.shared.viewmodelbase import ViewModelBase
from services import event_service

class EventListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        all_events = event_service.get_all_events()
        self.now = datetime.now()

        # Split into upcoming and past events
        self.upcoming_events = [e for e in all_events if e.event_datetime >= self.now]
        self.past_events = [e for e in all_events if e.event_datetime < self.now]