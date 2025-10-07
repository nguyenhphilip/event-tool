from viewmodels.shared.viewmodelbase import ViewModelBase
from services import user_service, event_service
import data.db_session as db_session

class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        # if the user is logged in, load their data
        self.user = user_service.find_user_by_id(self.user_id)
        self.events = self.user["events"] if self.user else []
        self.message = None
        self.deleted_event_title = None
        self.deleted_event_slug = None

    def validate_delete(self, event_slug: str):
        """Validate and perform event deletion for this user."""
        if not self.user:
            self.error = "You must be logged in to delete an event."
            return

        session = db_session.create_session()
        event = event_service.find_event_by_slug(event_slug)

        if not event:
            self.error = "That event could not be found."
            return

        if event.user_id != self.user_id:
            self.error = "You are not authorized to delete this event."
            return

        # store before deletion
        self.deleted_event_title = event.title
        self.deleted_event_slug = event.event_slug

        # perform deletion
        session.delete(event)
        session.commit()

        # confirmation message
        self.message = f"Deleted event: {self.deleted_event_title}"

        # reload updated list
        self.user = user_service.find_user_by_id(self.user_id)
        self.events = self.user["events"]
