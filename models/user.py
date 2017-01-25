from . import ModelMixin
from . import db
from . import timestamp
from admin import admin_id, admin_password


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(20))
    password = db.Column(db.Text(20))
    qq = db.Column(db.Text(20))
    email = db.Column(db.Text(20))
    signature = db.Column(db.Text(100))
    created_time = db.Column(db.Text(20))
    avatar = db.Column(db.Text(500))

    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')




    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')
        self.signature = form.get('signature', '')
        self.qq = form.get('qq', '')
        self.created_time = timestamp()
        self.avatar = form.get('avatar', '0001.jpeg')


    def update(self, form):
        print('user.update, ', form)
        self.password = form.get('password', self.password)


    def salted_password(self,password):
        import hashlib
        salt = 'dfgeryu564'
        def sha1hex(str):
            ascii_str = str.encode('ascii')
            return hashlib.sha1(ascii_str).hexdigest()
        hash1 = sha1hex(password)
        hash2 = sha1hex(hash1 + salt)
        return hash2

    # 验证注册用户的合法性的
    def valid(self):
        valid_username = User.query.filter_by(username=self.username).first() == None
        print('self.password', self.password)
        valid_username_len = len(self.username) >= 6
        valid_password_len = len(self.password) >= 6
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        if not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        if not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        self.password = self.salted_password(self.password)
        print('pwd', self.password)
        return status, msgs




    def valid_login(self, u):
        if u is not None:
            username_equals = u.username == self.username
            password_equals = u.password == self.salted_password(self.password)
            return username_equals and password_equals
        else:
            return False

    def is_admin(self):
        return self.username == 'admin_1' and self.id == admin_id and self.password == admin_password



