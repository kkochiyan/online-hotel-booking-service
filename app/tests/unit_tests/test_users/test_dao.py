import pytest

from app.users.dao import UsersDAO

@pytest.mark.parametrize(
    "user_id, email, exists",
    [
        (1, "test@test.com", True),
        (2, "artem@example.com", True),
        (3, ".....", False),
    ]
)
async def test_find_one_or_none(user_id, email, exists):
    user = await UsersDAO.find_one_or_none(id=user_id)

    if exists:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user