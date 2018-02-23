#!/usr/bin/env python
import os

from cad import create_app, db
from cad.models import User, Log

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

            log = Log(created_by='System', event_id=user.id, log_action='User Created')
            db.session.add(log)
            db.session.commit()

    app.run()
