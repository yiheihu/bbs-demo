from routes import *
from models.node import Node


main = Blueprint('node', __name__)

Model = Node

def nowaday_user():
    user_id = session.get('uid', -1)
    u = User.query.get(user_id)
    return u


def admin_required():
    u = nowaday_user()
    if u is None or not u.is_admin():
        abort(404)

main.before_request(admin_required)

@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('node_index.html', node_list=ms)



@main.route('/add', methods=['POST'])
def add():
    form = request.form
    Model.new(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
def delete(id):
    m = Model.query.get(id)
    m.delete()
    return redirect(url_for('.index'))


@main.route('/edit/<id>')
def edit(id):
    m = Model.query.get(id)
    return render_template('node_edit.html', node=m)


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    Model.update(id, form)
    return redirect(url_for('.index'))