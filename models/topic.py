from . import ModelMixin
from . import db
from . import timestamp

class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(500))
    content = db.Column(db.Text(2500))
    created_time = db.Column(db.Text(20))

    comments = db.relationship('Comment', backref='topic')
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.node_id = form.get('node_id', -1)
        self.user_id = form.get('user_id', -1)

    def comment_num(self):
        self.comment_num = len(self.comments)

    def update(self, form):
        self.title = form.get('title', -1)
        self.content = form.get('content', -1)
        self.save()


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(2500))
    created_time = db.Column(db.Text(20))

    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.topic_id = form.get('topic_id', -1)