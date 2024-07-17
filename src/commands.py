from src.get_data import get_user


def show_user():
    pass


def list_gear():
    user = get_user()
    return user['bikes'], user['shoes']


if __name__ == '__main__':
    list_gear()
