# 集成测试模式 (Integration Test Patterns)

> **用途**: 提供 API 集成测试的标准模板和示例代码（Python + Flask）。

---

## 集成测试模式

### API 集成测试模板 (Python + Flask)

```python
# tests/integration/test_user_api.py
import pytest
from flask import Flask
from src.app import create_app
from src.database import db


class TestUserAPI:
    """用户 API 集成测试"""

    @pytest.fixture
    def app(self):
        """创建测试应用"""
        app = create_app('testing')
        with app.app_context():
            db.create_all()
            yield app
            db.session.remove()
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        """创建测试客户端"""
        return app.test_client()

    def test_register_user_success(self, client):
        """测试用户注册 API - 成功"""
        # Arrange
        user_data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "SecurePass123"
        }

        # Act
        response = client.post('/api/v1/users/register', json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == user_data['username']
        assert data['email'] == user_data['email']
        assert 'id' in data
        assert 'password' not in data  # 确保密码不返回

    def test_register_user_duplicate_email(self, client):
        """测试用户注册 API - 邮箱重复"""
        # Arrange
        user_data = {
            "username": "user1",
            "email": "duplicate@test.com",
            "password": "Pass123"
        }

        # 先创建一个用户
        client.post('/api/v1/users/register', json=user_data)

        # 尝试用相同邮箱再次注册
        response = client.post('/api/v1/users/register', json=user_data)

        # Assert
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower()

    def test_login_success(self, client):
        """测试用户登录 API - 成功"""
        # Arrange - 先注册用户
        register_data = {
            "username": "loginuser",
            "email": "login@test.com",
            "password": "SecurePass123"
        }
        client.post('/api/v1/users/register', json=register_data)

        # Act - 登录
        login_data = {
            "email": "login@test.com",
            "password": "SecurePass123"
        }
        response = client.post('/api/v1/auth/login', json=login_data)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == login_data['email']

    def test_get_user_with_auth(self, client):
        """测试获取用户信息 - 需要认证"""
        # Arrange - 注册并登录获取 token
        register_data = {
            "username": "authuser",
            "email": "auth@test.com",
            "password": "Pass123"
        }
        client.post('/api/v1/users/register', json=register_data)

        login_response = client.post('/api/v1/auth/login', json={
            "email": "auth@test.com",
            "password": "Pass123"
        })
        token = login_response.get_json()['access_token']

        # Act - 使用 token 获取用户信息
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/v1/users/me', headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'auth@test.com'

    def test_get_user_without_auth(self, client):
        """测试获取用户信息 - 未认证"""
        # Act
        response = client.get('/api/v1/users/me')

        # Assert
        assert response.status_code == 401
```
