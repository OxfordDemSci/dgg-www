import pytest
from app import create_app
from sqlalchemy import text

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app('testing')
    os.environ["ENV"] = "test"
    with app.app_context():
        yield app


def delete_all_tables(db):
    query = text("""DO $$ 
    DECLARE 
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema() AND tablename != 'spatial_ref_sys') LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
        EXECUTE 'DROP TYPE IF EXISTS userroleenum CASCADE';
    END $$;""")
    with db.engine.begin() as connection:
        connection.execute(query)


@pytest.fixture(scope='session')
def db(app):
    import logging
    logging.getLogger('alembic').setLevel(logging.CRITICAL)
    alembic_cfg = Config(ALEMBIC)
    alembic_cfg.set_main_option("sqlalchemy.url", app.config["TEST_DATABASE_URI"])
    with app.app_context():
        _db.create_all()
        delete_all_tables(_db)
        upgrade(alembic_cfg, "head")
    with _db.session.begin_nested():
        print("INSERTING TEST DATA")
        insert_test_data(_db.session)
        from app import bcrypt
        from app.models import User
        from app.datatypes import UserRoleEnum
        username = "test_user"
        password = "test_password"
        #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        add_users_to_db(username, password, UserRoleEnum.WRITE, app, _db)
    yield _db
    delete_all_tables(_db)
    _db.drop_all()
    _db.engine.dispose()


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def test_client(app):
    with app.test_client() as test_client:
        yield test_client