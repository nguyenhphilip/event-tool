import flask
import infrastructure.cookie_auth as cookie_auth
import services.user_service as user_service
from viewmodels.users.index_viewmodel import IndexViewModel
from viewmodels.users.register_viewmodel import RegisterViewModel
from viewmodels.users.login_viewmodel import LoginViewModel

blueprint = flask.Blueprint('users', __name__, template_folder='templates')


@blueprint.route("/users")
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/users/login')

    return flask.render_template('users/index.html',
                                 **vm.to_dict())


############################## REGISTER ##############################


@blueprint.route("/users/register", methods = ['GET'])
def register_get():
    vm = RegisterViewModel()
    return flask.render_template('users/register.html',
                                 **vm.to_dict())


@blueprint.route("/users/register", methods = ['POST'])
def register_post():

    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        return flask.render_template('users/register.html', 
                                     **vm.to_dict())


    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        return flask.render_template('users/register.html', 
                                     **vm.to_dict())

    resp = flask.redirect('/users')
    cookie_auth.set_auth(resp, user.id)
    return resp


############################## LOGIN ##############################

@blueprint.route("/users/login", methods = ['GET'])
def login_get():
    vm = LoginViewModel()
    return flask.render_template('users/login.html', **vm.to_dict())


@blueprint.route("/users/login", methods = ['POST'])
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return flask.render_template('users/login.html', **vm.to_dict())

    resp = flask.redirect('/users')
    cookie_auth.set_auth(resp, vm.user.id)
    return resp


@blueprint.route("/users/logout")
def logout():

    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp