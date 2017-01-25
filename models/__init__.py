from flask_sqlalchemy import SQLAlchemy
import time


db = SQLAlchemy()


def timestamp():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()

    @classmethod
    def update(cls, id, form):
        m = cls.query.get(id)
        m._update(form)
        m.save()


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



    def get_comment_num(self):
        for t in self.topics:
            t.comment_num()

if __name__ =='__main__':
    t = timestamp()
    print(t)
