from datetime import datetime
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from ..ORM.schemas.user_schema import User, UserModel, UserValidator
from ..ORM.database import Base


ACC_TOKEN_TS = datetime.now()


@pytest.fixture(scope='function')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope='function')
def dataset(db):
    john = UserModel(username='john', token='jtoken', acc_token_ts=ACC_TOKEN_TS)
    mary = UserModel(username='mary', token='mtoken', acc_token_ts=ACC_TOKEN_TS)
    peter = UserModel(username='peter', token='ptoken')
    db.add_all([john, mary, peter])
    db.commit()
    yield db


@pytest.fixture()
def new_user():
    return UserValidator(
        username='new user',
        token='ntoken',
        refresh_token='nrefresh_token'
    )


def test_get_not_found(dataset):
    with pytest.raises(NoResultFound):
        User.get(dataset, username='another_name')


def test_get_found(dataset):
    user = User.get(dataset, username='john')
    assert user.username == 'john'
    assert user.token == 'jtoken'


def test_get_multiple_found(dataset):
    with pytest.raises(MultipleResultsFound):
        User.get(dataset, acc_token_ts=ACC_TOKEN_TS)


def test_get_or_create_exists_user(dataset):
    user, created = User.get_or_create(dataset, username='john')
    assert created is False
    assert user.token == 'jtoken'
    assert dataset.query(UserModel).filter(UserModel.username == 'john').count() == 1


def test_get_or_create_new_user(dataset, new_user):
    user, created = User.get_or_create(dataset, _defaults=new_user.dict(), username='new user')
    assert created is True
    assert user.username == 'new user'
    assert user.token == 'ntoken'
    assert user.refresh_token == 'nrefresh_token'
    assert dataset.query(UserModel).filter(UserModel.username == 'new user').count() == 1


def test_update(dataset, new_user):
    user1 = User.get(dataset, username='john')
    user2, _ = User.get_or_create(dataset, _defaults=new_user.dict(), username=new_user.username)

    user1 = user1.update(dataset, _updates={'refresh_token': 'n123456'})
    user2 = user2.update(dataset, _updates={'username': 'new_user2'})

    db_user1 = dataset.query(UserModel).filter(UserModel.username == 'john').one()
    db_user2 = dataset.query(UserModel).filter(UserModel.username == 'new_user2').one()

    assert user1.username == 'john'
    assert user1.refresh_token == 'n123456'
    assert user2.username == 'new_user2'
    assert user2.refresh_token == 'nrefresh_token'
    assert user1.id == db_user1.id
    assert user2.id == db_user2.id


def test_save(dataset):
    user = User.get(dataset, username='john')
    user.username = 'changed_username'
    user.token = 'changed_token'
    user.save(dataset)

    user = User.get(dataset, username='changed_username')
    assert user.token == 'changed_token'


def test_save_new_user(dataset, new_user):
    user = User(**new_user.dict(), acc_token_ts=ACC_TOKEN_TS)
    user.save(dataset)

    db_user = dataset.query(UserModel).filter(UserModel.username == user.username).one()

    assert user.token == db_user.token
    assert user.refresh_token == db_user.refresh_token
