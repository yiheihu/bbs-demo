from routes import *
from models.topic import Topic , Comment
from models.user import User

from . import current_user, valid_id



main = Blueprint('topic', __name__)

Model = Topic





@main.route('/')
def base():
    return render_template('topic_show.html')


@main.route('/new')
@current_user
def new(u):
    if u.username == '游客':
        abort(401)
    else:
        return render_template('topic_new.html', user=u)


@main.route('/add', methods=['POST'])
@current_user
def add(u):
    form = request.form
    print('add topic form', form)
    m = Model(form)
    # m.node_id = int(form.get('node_id', -1))
    print('m', m)
    print('m.node_id',m.node_id)
    print('m.content', m.content)
    m.user = u
    print('mm', m)
    m.save()
    print('mmm', m)
    id = m.id
    return redirect(url_for('.show', id=id))


@main.route('/show/<int:id>')
@current_user
def show(u, id):
    m = Model.query.get(id)
    m.comments = Comment.query.filter_by(topic_id=id).order_by(Comment.id.desc()).all()
    m.comment_num()
    return render_template('topic_show.html', topic=m, user=u)


@main.route('/edit/<int:id>')
@valid_id
def edit(id):
    m = Model.query.get(id)
    return render_template('topic_edit.html', topic=m)


@main.route('/update', methods=['POST'])
def update():
    form = request.form
    id = int(form.get('id', -1))
    m = Model.query.get(id)
    m.update(form)
    return redirect(url_for('.show', id=id))


@main.route('/comment/add', methods=['POST'])
@current_user
def addComment(u):
    form = request.form
    print('form', form)
    c = Comment(form)
    c.topic_id = int(form.get('topic_id', -1))
    c.user = u
    c.save()
    print(' c.content', c.content)
    id = c.topic_id
    return redirect(url_for('.show', id=id))






