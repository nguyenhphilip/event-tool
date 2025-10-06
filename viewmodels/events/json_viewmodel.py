from viewmodels.shared.viewmodelbase import ViewModelBase
from services import event_service

class EventsJsonViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.events = event_service.get_all_events()
        self.event_list = []

        for e in self.events:
            self.event_list.append({
                "title": e.title,
                "start": e.event_datetime.isoformat(),
                "description": e.description,
                "url": f"/events/{e.event_slug}"
            })