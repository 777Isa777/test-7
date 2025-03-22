import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_user_with_existing_username(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'anotheruser@example.com', 'password456')
    assert result == False
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username='testuser';")
    count = cursor.fetchone()[0]
    assert count == 1

def test_successful_authentication(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'password123')
    assert result == True

def test_successful_authentication(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'password123')
    assert result == True

def test_authentication_non_existing_user(setup_database, connection):
    result = authenticate_user('nonexistentuser', 'somepassword')
    assert result == False

def test_authentication_wrong_password(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'wrongpassword')
    assert result == False

def test_display_users(setup_database, connection):
    add_user('testuser1', 'testuser1@example.com', 'password123')
    add_user('testuser2', 'testuser2@example.com', 'password456')
    
    users = display_users()
    assert len(users) == 2
    assert any(user['username'] == 'testuser1' for user in users)
    assert any(user['username'] == 'testuser2' for user in users)

