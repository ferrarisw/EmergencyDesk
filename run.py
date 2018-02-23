#!/usr/bin/env python
import os

from cad import create_app, db
from cad.models import User
from cad.utils import log_cad

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
    with app.app_context():
        db.create_all()
        # create a development user
        if User.query.get(1) is None:
            user = User(username='davide')
            user.set_password('cat')
            db.session.add(user)
            db.session.commit()

            log_cad(db, created_by='System', log_action='User Created')

    app.run()
