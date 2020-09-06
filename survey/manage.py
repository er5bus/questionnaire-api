from src import create_app, models
import os
import click


application = create_app(os.getenv('FLASK_CONFIG', 'default'))

import handle_errors


@application.cli.command("create_admin")
@click.argument('username')
@click.argument('password')
def create_admin(username, password):
    root = models.BaseUser.query.filter_by(username=username).one_or_none()
    if not root:
        root = models.BaseUser()
        root.username = username
        root.password = password
        root.role = models.Role.ADMIN
        root.save()


@application.cli.command("test")
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    application.run(debug=True)
