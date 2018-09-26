#!/usr/bin/env python
import os

from cad import create_app, db
from cad.models import User, Unit
from cad.utils import log_cad


def init_db():
    unit1 = Unit(created_by=1,
                 call_sign='FORMIGINE 37',
                 profile='BLDS',
                 type='AMBULANZA',
                 current_address="via Sant'Onofrio 3, Formigine",
                 active=True)

    unit2 = Unit(created_by=1,
                 call_sign='MODENA 10',
                 profile='ALS',
                 type='AMBULANZA',
                 current_address="via Emilia Est 590, Modena",
                 active=True)

    unit3 = Unit(created_by=1,
                 call_sign='MODENA 1',
                 profile='ILS',
                 type='AMBULANZA',
                 current_address="via Emilia Est 590, Modena",
                 active=True)

    db.session.add(unit1)
    db.session.add(unit2)
    db.session.add(unit3)
    db.session.commit()


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

            init_db()

            log_cad(db,
                    log_action='First User Created')

    app.run()
