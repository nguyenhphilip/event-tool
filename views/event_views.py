import flask
import infrastructure.cookie_auth as cookie_auth
import services.event_service as event_service
import data.db_session as db_session
from data.event import Event
from data.attendee import Attendee
from viewmodels.events.index_viewmodel import EventListViewModel
from viewmodels.events.details_viewmodel import EventDetailsViewModel
from viewmodels.events.create_viewmodel import EventCreateViewModel
from viewmodels.events.register_viewmodel import EventRegisterViewModel
from viewmodels.events.unregister_viewmodel import EventUnregisterViewModel
from viewmodels.events.json_viewmodel import EventsJsonViewModel
from viewmodels.events.attendees_viewmodel import EventAttendeesViewModel



blueprint = flask.Blueprint('events', __name__, template_folder='templates')


@blueprint.route("/events/json")
def events_json():
    vm = EventsJsonViewModel()
    return flask.jsonify(vm.event_list)


@blueprint.route('/events')
def event_list():
    vm = EventListViewModel()
    return flask.render_template('events/index.html', 
                                 **vm.to_dict())


@blueprint.route("/events/<event_slug>")
def event_details(event_slug: str):

    vm = EventDetailsViewModel(event_slug)
    if not vm.event:
        flask.abort(404)

    return flask.render_template(
        'events/details.html',
        **vm.to_dict()
    )


@blueprint.route("/events/<event_slug>/attendees")
def event_attendees(event_slug: str):
    vm = EventAttendeesViewModel(event_slug)
    if not vm.event:
        flask.abort(404)

    if vm.not_authorized:
        return flask.render_template("events/not_authorized.html", **vm.to_dict()), 403

    return flask.render_template("events/attendees.html", **vm.to_dict())


@blueprint.route("/events/<event_slug>/thankyou")
def register_confirmed(event_slug: str):
    event = event_service.find_event_by_slug(event_slug)
    return flask.render_template('events/thankyou.html', 
                                 event = event,
                                 user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request))


@blueprint.route("/events/create", methods = ['GET'])
def event_get():
    vm = EventCreateViewModel()
    return flask.render_template('events/create.html',
                                 **vm.to_dict())


@blueprint.route("/events/create", methods = ['POST'])
def event_create():
    vm = EventCreateViewModel()
    vm.validate()
    
    if vm.error:
        return flask.render_template('events/create.html', **vm.to_dict())

    user_id = vm.user_id

    if not user_id:
        return flask.redirect('/users/login')
    
    # Create the first event
    event_service.create_event(
        vm.eventname, vm.location, vm.parsed_datetime, vm.description, user_id
    )
    
    # Handle recurrence
    if vm.is_recurring and vm.num_weeks > 1:
        from datetime import timedelta
        for week in range(1, vm.num_weeks):
            next_date = vm.parsed_datetime + timedelta(weeks=week)
            event_service.create_event(
                vm.eventname, vm.location, next_date, vm.description, user_id
            )

    return flask.redirect('/events')


# =========================
# Attendee Unregistration
# =========================


@blueprint.route("/events/<event_slug>/register", methods=["POST"])
def register_attendee(event_slug):

    vm = EventRegisterViewModel()
    vm.validate()
    if vm.error:
        return flask.render_template("events/details.html", **vm.to_dict())

    attendee = Attendee(name=vm.name, email=vm.email, event_id=vm.event.id)
    session = vm.session
    session.add(attendee)
    session.commit()
    return flask.redirect(flask.url_for("events.register_confirmed", event_slug=vm.event.event_slug))


@blueprint.route("/events/<event_slug>/unregister/success")
def unregister_success(event_slug):
    session = db_session.create_session()
    event = session.query(Event).filter(Event.event_slug == event_slug).first()
    email = flask.request.args.get("email")
    return flask.render_template("events/unregister_success.html", event_slug=event_slug, email=email, event_name = event.title)


@blueprint.route("/events/<event_slug>/unregister", methods=["POST"])
def unregister_attendee(event_slug):
    vm = EventUnregisterViewModel()
    vm.validate()
    if vm.error:
        return flask.render_template("events/unregister_confirm.html", **vm.to_dict())
    session = vm.session
    session.delete(vm.attendee)
    session.commit()
    return flask.redirect(flask.url_for("events.unregister_success", event_slug=vm.event.event_slug, email=vm.email))


# =========================
# Host Event Deletion
# =========================

