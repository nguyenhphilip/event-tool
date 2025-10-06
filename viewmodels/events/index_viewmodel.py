from viewmodels.events.events_viewmodel_base import EventViewModelBase
from services import event_service

class EventListViewModel(EventViewModelBase):
    def __init__(self):
        super().__init__()
        self.events = event_service.get_all_events()