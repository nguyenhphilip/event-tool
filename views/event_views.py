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
from viewmodels.events.delete_viewmodel import EventDeleteViewModel
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


# @blueprint.route("/events/<event_slug>/register", methods=["POST"])
# def register_for_event(event_slug: str):
#     r = flask.request
#     name = r.form.get("name", "").strip()

#     if not name:
#         return flask.render_template("events/details.html",
#                                      error="Name is required.",
#                                      event=event_service.find_event_by_slug(event_slug))

#     event = event_service.find_event_by_slug(event_slug)
#     if not event:
#         flask.abort(404)

#     event_service.add_attendee(event.id, name)

#     return flask.redirect(f"/events/{event_slug}/thankyou")


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

    user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request)
    if not user_id:
        return flask.redirect('/users/login')

    event_service.create_event(vm.eventname, vm.location, vm.parsed_datetime, vm.description, user_id)
    return flask.redirect('/events')


# =========================
# Attendee Unregistration
# =========================

import flask
from data.event import Event
from data.attendee import Attendee
import data.db_session as db_session
import infrastructure.cookie_auth as cookie_auth

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

@blueprint.route("/events/<event_slug>/delete", methods=["POST"])
def delete_event(event_slug):
    vm = EventDeleteViewModel()
    vm.validate()
    if vm.error:
        return flask.render_template("events/not_authorized.html", **vm.to_dict()), 403
    session = vm.session
    session.delete(vm.event)
    session.commit()
    return flask.redirect(flask.url_for("events.delete_success", event_slug=event_slug))


@blueprint.route("/events/<event_slug>/delete/success")
def delete_success(event_slug):
    return flask.render_template("events/delete_success.html")
