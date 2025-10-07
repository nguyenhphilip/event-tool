from viewmodels.shared.viewmodelbase import ViewModelBase
from services import event_service
import data.db_session as db_session
from data.event import Event
from data.attendee import Attendee

class EventViewModelBase(ViewModelBase):
    def __init__(self, event_slug=None):
        super().__init__()
        self.event_slug = event_slug or self.request.view_args.get("event_slug")
        self.session = db_session.create_session()
        self.event = None

    def load_event(self):
        if self.event_slug:
            self.event = event_service.find_event_by_slug(self.event_slug)