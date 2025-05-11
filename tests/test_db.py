from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='Diogo', email='teste@gmail.com', password='teste123')

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'teste@gmail.com')
    )

    assert result.username == 'Diogo'
