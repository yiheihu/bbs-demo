from routes import *
from models.user import User
from . import current_user, valid_id
import uuid


main = Blueprint('user', __name__)

Model = User




@main.route('/index/login')
def login_index():
    return render_template('login.html')


@main.route('/index/register')
def register_index():
    return render_template('register.html')


@main.route('/login',  methods=['POST'])
def login():
    form = request.form
    m = Model(form)
    u = Model.query.filter_by(username=m.username).first()
    if m.valid_login(u):
        session.permanent = True
        session['uid'] = u.id
        return redirect(url_for('homepage.show', id=1))
    else:
        return redirect(url_for('.login_index'))



@main.route('/register',  methods=['POST'])
def register():
    form = request.form
    m = Model(form)
    status, msgs = m.valid()
    if status:
        m.save()
        session.permanent = True
        session['uid'] = m.id
        return redirect(url_for('homepage.show', id=1))
    else:
        resoult = '<br>'.join(msgs)
        return resoult


@main.route('/settings')
@current_user
def settings(u):
    return render_template('settings.html', user=u)


@main.route('/settings/avatar', methods=['post'])
@current_user
def avatar(u):
    file = request.files.get('avatar') #获取文件对象
    uploads_dir = 'static/img/avatar/'
    filename = avatar_name(file.filename) # file.filename获取文件名
    path = uploads_dir + filename
    file.save(path)
    old_path = uploads_dir + u.avatar
    if old_path != 'static/img/avatar/0001.jpeg':
        os.remove(old_path)
    u.avatar = filename
    u.save()
    return render_template('settings.html', user=u)
#用Flask处理文件上传，上传的文件储存在内存或者文件系统中的一个临时位置，你可以通过request 对象的 files 属性来访问这些文件，每个上传的文件都储存在那个字典里。
#它还有一个 save() 方法允许你把文件存储在服务器的文件系统上。
def avatar_name(old_filename):
    valid_filetypes = ('png', 'jpg', 'jpeg', 'gif', 'apng')
    a = str(uuid.uuid4())
    b = old_filename.split('.')[-1]
    if b not in valid_filetypes:
        return abort(404)
    else:
        filename = a + "." + b
        return filename



@main.route('/member/<username>')
def member(username):
    if username != '游客':
        m = Model.query.filter_by(username=username).first()
        m.get_comment_num()
        return render_template('member.html', user=m)
    else:
        abort(401)




