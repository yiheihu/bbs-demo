from . import ModelMixin
from . import db
from . import timestamp


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(20))
    topics = db.relationship('Topic', backref='node', foreign_keys='Topic.node_id')

    def __init__(self, form):
        self.name = form.get('name', '')

    def _update(self, form):
        self.name = form.get('name', '')

