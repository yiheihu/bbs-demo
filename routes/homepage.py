from routes import *
from models.node import Node
from . import current_user


main = Blueprint('homepage', __name__)

Model = Node

@main.route('/show/<int:id>')
@current_user
def show(u, id):
    m_list = Model.query.all()
    m = Model.query.get(id)
    m.get_comment_num()
    return render_template('node_show.html', node=m, user=u, n_list=m_list )
