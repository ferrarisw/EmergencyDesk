import os

from flask import Flask, url_for, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data.sqlite')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)

    def get_url(self):
        return url_for('get_user', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'username': self.username
        }

    def import_data(self, data):
        try:
            self.username = data['name']
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        return self


@app.route('/users/', methods=['GET'])
def get_users():
    return jsonify({'users': [user.get_url() for user in
                              User.query.all()]})


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


@app.route('/users/', methods=['POST'])
def new_user():
    user = User()
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({}), 201, {'Location': user.get_url()}


@app.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
