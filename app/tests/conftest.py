import pytest
from app import create_app
from app import db
#create a new database session after a request as described below.
from flask.signals import request_finished
from app.models.planet import Planet

# Create test versions of our flask app and database
@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    #will be invoked after any request is completed
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        # sets up database
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    # depends on app that references another fixture
    # holds the reference to the test interface
    return app.test_client()

@pytest.fixture
def two_saved_planets(app):
    # Arrange
    blorp = Planet 
    {
            "id": 2,
            "name": 'Blorp',
            "color": 'Purple',
            "description": "Stinky"
        }
    florpus = Planet
    {
            "id": 3,
            "name": 'Florpus',
            "color": 'Red',
            "description": "Shy"
        }
    db.session.add_all([blorp, florpus])
    # Alternatively, we could do
    # db.session.add(winston)
    # db.session.add(winter)
    db.session.commit()

 