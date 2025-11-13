# 测试模式与最佳实践 (Test Patterns and Best Practices)

> **用途**: 为测试代码生成提供标准模板和最佳实践，确保测试覆盖率和代码质量。

---

## 目录

1. [测试覆盖率要求](#测试覆盖率要求)
2. [单元测试模式](#单元测试模式)
3. [集成测试模式](#集成测试模式)
4. [端到端测试模式](#端到端测试模式)
5. [测试命名规范](#测试命名规范)
6. [测试组织结构](#测试组织结构)
7. [Mock 和 Stub 模式](#mock-和-stub-模式)
8. [测试数据管理](#测试数据管理)
9. [性能测试模式](#性能测试模式)
10. [常见反模式](#常见反模式)

---

## 测试覆盖率要求

### 覆盖率目标 (G9 合规)

- **默认目标**: 85% 语句覆盖率
- **最低阈值**: 70% 语句覆盖率
- **推荐目标**: 90%+ 对于核心业务逻辑

### 覆盖率读取机制

```markdown
测试代码生成时，必须从上下文读取 `[COVERAGE_TARGET: X%]`：
- 由 main-router 在任务开始时设置
- simple-gemini / codex-code-reviewer 只读取不判断
- 默认值：85%（用户未指定时）
- 最低值：70%（低于此值触发警告）
```

### 覆盖率类型

1. **语句覆盖率 (Statement Coverage)**: 每一行代码是否被执行
2. **分支覆盖率 (Branch Coverage)**: 每个条件分支是否被测试
3. **函数覆盖率 (Function Coverage)**: 每个函数是否被调用
4. **路径覆盖率 (Path Coverage)**: 所有可能的执行路径

**优先级**: 语句覆盖 > 分支覆盖 > 函数覆盖 > 路径覆盖

---

## 单元测试模式

### Python 单元测试模板 (pytest)

```python
# tests/test_user_service.py
import pytest
from unittest.mock import Mock, patch
from src.services.user_service import UserService
from src.models.user import User


class TestUserService:
    """用户服务单元测试"""

    @pytest.fixture
    def user_service(self):
        """创建测试用的用户服务实例"""
        return UserService()

    @pytest.fixture
    def sample_user(self):
        """创建测试用户数据"""
        return User(
            id="usr_001",
            username="testuser",
            email="test@example.com"
        )

    def test_create_user_success(self, user_service, sample_user):
        """测试创建用户 - 成功场景"""
        # Arrange (准备)
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123"
        }

        # Act (执行)
        result = user_service.create_user(user_data)

        # Assert (断言)
        assert result is not None
        assert result.username == user_data["username"]
        assert result.email == user_data["email"]
        assert result.id is not None

    def test_create_user_duplicate_email(self, user_service):
        """测试创建用户 - 邮箱重复"""
        # Arrange
        user_data = {
            "username": "testuser",
            "email": "existing@example.com",
            "password": "SecurePass123"
        }

        # Mock 数据库返回已存在的用户
        with patch.object(user_service, 'db') as mock_db:
            mock_db.find_by_email.return_value = Mock()

            # Act & Assert
            with pytest.raises(ValueError, match="Email already exists"):
                user_service.create_user(user_data)

    def test_create_user_invalid_email(self, user_service):
        """测试创建用户 - 无效邮箱格式"""
        # Arrange
        user_data = {
            "username": "testuser",
            "email": "invalid-email",  # 无效格式
            "password": "SecurePass123"
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user(user_data)

    @pytest.mark.parametrize("username,email,expected", [
        ("user1", "user1@test.com", True),
        ("user2", "user2@test.com", True),
        ("", "empty@test.com", False),  # 空用户名
        ("user3", "invalid", False),    # 无效邮箱
    ])
    def test_create_user_parametrized(self, user_service, username, email, expected):
        """参数化测试 - 多种输入场景"""
        user_data = {
            "username": username,
            "email": email,
            "password": "Pass123"
        }

        if expected:
            result = user_service.create_user(user_data)
            assert result is not None
        else:
            with pytest.raises(ValueError):
                user_service.create_user(user_data)
```

### JavaScript 单元测试模板 (Jest)

```javascript
// tests/userService.test.js
import { UserService } from '../src/services/UserService';
import { User } from '../src/models/User';

describe('UserService', () => {
  let userService;

  beforeEach(() => {
    // 每个测试前重置服务实例
    userService = new UserService();
  });

  afterEach(() => {
    // 清理资源
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    it('should create user successfully', async () => {
      // Arrange
      const userData = {
        username: 'testuser',
        email: 'test@example.com',
        password: 'SecurePass123'
      };

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toBeDefined();
      expect(result.username).toBe(userData.username);
      expect(result.email).toBe(userData.email);
      expect(result.id).toBeTruthy();
    });

    it('should throw error when email already exists', async () => {
      // Arrange
      const userData = {
        username: 'testuser',
        email: 'existing@example.com',
        password: 'SecurePass123'
      };

      // Mock database to return existing user
      jest.spyOn(userService.db, 'findByEmail').mockResolvedValue({ id: '123' });

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Email already exists');
    });

    it('should throw error for invalid email format', async () => {
      // Arrange
      const userData = {
        username: 'testuser',
        email: 'invalid-email',
        password: 'SecurePass123'
      };

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Invalid email format');
    });
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      // Arrange
      const userId = 'usr_001';
      const mockUser = new User({
        id: userId,
        username: 'testuser',
        email: 'test@example.com'
      });

      jest.spyOn(userService.db, 'findById').mockResolvedValue(mockUser);

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toEqual(mockUser);
    });

    it('should return null when user not found', async () => {
      // Arrange
      const userId = 'nonexistent';
      jest.spyOn(userService.db, 'findById').mockResolvedValue(null);

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toBeNull();
    });
  });
});
```

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

---

## 端到端测试模式

### E2E 测试模板 (Playwright / Cypress)

```javascript
// tests/e2e/userFlow.spec.js
import { test, expect } from '@playwright/test';

test.describe('User Registration and Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    // 每个测试前访问首页
    await page.goto('http://localhost:3000');
  });

  test('should complete full user registration flow', async ({ page }) => {
    // Step 1: 导航到注册页面
    await page.click('text=Sign Up');
    await expect(page).toHaveURL(/.*\/register/);

    // Step 2: 填写注册表单
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123');
    await page.fill('input[name="confirmPassword"]', 'SecurePass123');

    // Step 3: 提交表单
    await page.click('button[type="submit"]');

    // Step 4: 验证注册成功
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('text=Welcome, testuser')).toBeVisible();
  });

  test('should show error for invalid email', async ({ page }) => {
    // Step 1: 导航到注册页面
    await page.click('text=Sign Up');

    // Step 2: 填写无效邮箱
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'Pass123');

    // Step 3: 提交表单
    await page.click('button[type="submit"]');

    // Step 4: 验证错误提示
    await expect(page.locator('text=Invalid email format')).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    // Prerequisite: 假设用户已注册
    // （在真实 E2E 测试中，可能需要先注册或使用测试数据库）

    // Step 1: 导航到登录页面
    await page.click('text=Login');

    // Step 2: 填写登录表单
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123');

    // Step 3: 提交表单
    await page.click('button[type="submit"]');

    // Step 4: 验证登录成功
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('text=Welcome back')).toBeVisible();
  });

  test('should persist user session after page refresh', async ({ page }) => {
    // Step 1: 登录
    await page.click('text=Login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123');
    await page.click('button[type="submit"]');

    // Step 2: 刷新页面
    await page.reload();

    // Step 3: 验证会话保持
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });
});
```

---

## 测试命名规范

### 命名模式

```
test_<function>_<scenario>_<expected_result>
```

### 示例

**✅ 好的命名**:
```python
def test_create_user_with_valid_data_returns_user_object():
    pass

def test_create_user_with_duplicate_email_raises_value_error():
    pass

def test_get_user_by_id_with_nonexistent_id_returns_none():
    pass
```

**❌ 不好的命名**:
```python
def test_user():  # 太模糊
    pass

def test_create():  # 缺少上下文
    pass

def test_1():  # 完全无意义
    pass
```

### JavaScript / TypeScript 命名

```javascript
// ✅ 好的命名
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user successfully with valid data', () => {});
    it('should throw error when email already exists', () => {});
    it('should throw error for invalid email format', () => {});
  });
});

// ❌ 不好的命名
describe('Tests', () => {
  it('works', () => {});  // 太模糊
  it('test1', () => {});  // 无意义
});
```

---

## 测试组织结构

### Python 项目结构

```
project/
├── src/
│   ├── services/
│   │   └── user_service.py
│   ├── models/
│   │   └── user.py
│   └── api/
│       └── user_api.py
└── tests/
    ├── unit/
    │   ├── services/
    │   │   └── test_user_service.py
    │   └── models/
    │       └── test_user.py
    ├── integration/
    │   └── test_user_api.py
    ├── e2e/
    │   └── test_user_flow.py
    ├── fixtures/
    │   └── user_fixtures.py
    └── conftest.py
```

### JavaScript / TypeScript 项目结构

```
project/
├── src/
│   ├── services/
│   │   └── UserService.ts
│   ├── models/
│   │   └── User.ts
│   └── api/
│       └── userApi.ts
└── tests/
    ├── unit/
    │   ├── services/
    │   │   └── UserService.test.ts
    │   └── models/
    │       └── User.test.ts
    ├── integration/
    │   └── userApi.test.ts
    ├── e2e/
    │   └── userFlow.spec.ts
    └── fixtures/
        └── userFixtures.ts
```

---

## Mock 和 Stub 模式

### Python Mock 示例

```python
from unittest.mock import Mock, patch, MagicMock

# 1. Mock 对象
def test_with_mock_object():
    # 创建 Mock 对象
    mock_db = Mock()
    mock_db.find_by_id.return_value = {"id": "123", "name": "Test"}

    # 使用 Mock
    service = UserService(db=mock_db)
    result = service.get_user("123")

    # 验证调用
    mock_db.find_by_id.assert_called_once_with("123")
    assert result["name"] == "Test"

# 2. Patch 装饰器
@patch('src.services.user_service.Database')
def test_with_patch_decorator(mock_database):
    mock_database.return_value.find_by_id.return_value = {"id": "123"}

    service = UserService()
    result = service.get_user("123")

    assert result["id"] == "123"

# 3. Patch 上下文管理器
def test_with_patch_context():
    with patch('src.services.user_service.Database') as mock_db:
        mock_db.return_value.find_by_id.return_value = {"id": "123"}

        service = UserService()
        result = service.get_user("123")

        assert result["id"] == "123"

# 4. Mock 方法返回值
def test_mock_side_effect():
    mock_api = Mock()
    # 模拟多次调用返回不同值
    mock_api.get_data.side_effect = ["data1", "data2", "data3"]

    assert mock_api.get_data() == "data1"
    assert mock_api.get_data() == "data2"
    assert mock_api.get_data() == "data3"

# 5. Mock 异常
def test_mock_exception():
    mock_api = Mock()
    mock_api.get_data.side_effect = ConnectionError("Network error")

    with pytest.raises(ConnectionError):
        mock_api.get_data()
```

### JavaScript Mock 示例

```javascript
// 1. Jest Mock 函数
test('should call callback with data', () => {
  const mockCallback = jest.fn();
  const data = { id: '123', name: 'Test' };

  processData(data, mockCallback);

  expect(mockCallback).toHaveBeenCalledWith(data);
  expect(mockCallback).toHaveBeenCalledTimes(1);
});

// 2. Mock 模块
jest.mock('../src/services/Database', () => {
  return {
    Database: jest.fn().mockImplementation(() => {
      return {
        findById: jest.fn().mockResolvedValue({ id: '123' })
      };
    })
  };
});

// 3. Spy 函数
test('should spy on method', () => {
  const user = new User();
  const spy = jest.spyOn(user, 'save');

  user.update({ name: 'New Name' });

  expect(spy).toHaveBeenCalled();
  spy.mockRestore();
});

// 4. Mock 实现
test('should mock implementation', () => {
  const mockFn = jest.fn().mockImplementation((x) => x * 2);

  expect(mockFn(2)).toBe(4);
  expect(mockFn(3)).toBe(6);
});

// 5. Mock 返回值
test('should mock return values', () => {
  const mockFn = jest.fn()
    .mockReturnValueOnce('first')
    .mockReturnValueOnce('second')
    .mockReturnValue('default');

  expect(mockFn()).toBe('first');
  expect(mockFn()).toBe('second');
  expect(mockFn()).toBe('default');
  expect(mockFn()).toBe('default');
});
```

---

## 测试数据管理

### Fixture 模式

**Python (pytest)**:
```python
# tests/conftest.py
import pytest
from src.models.user import User

@pytest.fixture
def sample_user():
    """创建测试用户"""
    return User(
        id="usr_001",
        username="testuser",
        email="test@example.com"
    )

@pytest.fixture
def user_list():
    """创建用户列表"""
    return [
        User(id=f"usr_{i:03d}", username=f"user{i}", email=f"user{i}@test.com")
        for i in range(1, 6)
    ]

@pytest.fixture(scope="session")
def database():
    """会话级别的数据库 fixture"""
    db = Database()
    db.connect()
    yield db
    db.disconnect()
```

### Factory 模式

```python
# tests/factories.py
from datetime import datetime

class UserFactory:
    """用户工厂"""

    @staticmethod
    def create(overrides=None):
        """创建用户对象"""
        defaults = {
            "id": "usr_001",
            "username": "testuser",
            "email": "test@example.com",
            "created_at": datetime.now()
        }

        if overrides:
            defaults.update(overrides)

        return User(**defaults)

    @staticmethod
    def create_batch(count, **kwargs):
        """批量创建用户"""
        return [
            UserFactory.create({
                **kwargs,
                "id": f"usr_{i:03d}",
                "username": f"user{i}",
                "email": f"user{i}@test.com"
            })
            for i in range(1, count + 1)
        ]

# 使用示例
def test_with_factory():
    user = UserFactory.create({"username": "custom_user"})
    users = UserFactory.create_batch(5)
```

---

## 性能测试模式

### 基准测试 (Benchmark)

```python
import pytest
import time

@pytest.mark.benchmark
def test_user_creation_performance(benchmark):
    """基准测试：用户创建性能"""

    def create_user():
        return UserService().create_user({
            "username": "testuser",
            "email": "test@example.com",
            "password": "Pass123"
        })

    result = benchmark(create_user)
    assert result is not None

    # 验证性能指标
    assert benchmark.stats['mean'] < 0.1  # 平均时间小于 100ms
```

### 负载测试 (Load Test)

```python
import concurrent.futures

def test_concurrent_user_creation():
    """负载测试：并发创建用户"""
    service = UserService()
    user_count = 100

    def create_user(index):
        return service.create_user({
            "username": f"user{index}",
            "email": f"user{index}@test.com",
            "password": "Pass123"
        })

    # 并发创建用户
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_user, i) for i in range(user_count)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(results) == user_count
    assert all(r is not None for r in results)
```

---

## 常见反模式

### ❌ 反模式 1: 测试依赖顺序

```python
# ❌ 不好：测试依赖执行顺序
class TestBadOrder:
    def test_01_create_user(self):
        self.user_id = create_user()

    def test_02_update_user(self):
        update_user(self.user_id)  # 依赖上一个测试

# ✅ 好：每个测试独立
class TestGoodOrder:
    @pytest.fixture
    def user_id(self):
        return create_user()

    def test_create_user(self):
        user_id = create_user()
        assert user_id is not None

    def test_update_user(self, user_id):
        result = update_user(user_id)
        assert result is True
```

### ❌ 反模式 2: 过度 Mock

```python
# ❌ 不好：Mock 了所有依赖
def test_too_much_mocking():
    mock_db = Mock()
    mock_cache = Mock()
    mock_logger = Mock()
    mock_validator = Mock()
    mock_emailer = Mock()
    # ... 过度 Mock，测试变得毫无意义

# ✅ 好：只 Mock 外部依赖
def test_appropriate_mocking():
    # 只 Mock 真正的外部依赖（数据库、API 等）
    with patch('src.services.external_api.ExternalAPI') as mock_api:
        mock_api.return_value.get_data.return_value = {"key": "value"}
        result = service.process_data()
        assert result is not None
```

### ❌ 反模式 3: 测试实现细节

```python
# ❌ 不好：测试私有方法
def test_private_method():
    service = UserService()
    result = service._validate_email("test@example.com")  # 测试私有方法
    assert result is True

# ✅ 好：测试公共接口
def test_public_interface():
    service = UserService()
    user = service.create_user({
        "email": "test@example.com",
        "username": "testuser",
        "password": "Pass123"
    })
    assert user.email == "test@example.com"  # 通过公共方法验证
```

### ❌ 反模式 4: 忽略边界条件

```python
# ❌ 不好：只测试正常路径
def test_only_happy_path():
    result = divide(10, 2)
    assert result == 5

# ✅ 好：测试边界条件
def test_with_boundary_conditions():
    assert divide(10, 2) == 5  # 正常情况
    assert divide(0, 5) == 0   # 零除数
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)  # 除零错误
    assert divide(-10, 2) == -5  # 负数
```

---

## 测试最佳实践总结

### AAA 模式（Arrange-Act-Assert）

```python
def test_with_aaa_pattern():
    # Arrange（准备）：设置测试数据和前置条件
    user_data = {"username": "test", "email": "test@example.com"}
    service = UserService()

    # Act（执行）：调用被测试的方法
    result = service.create_user(user_data)

    # Assert（断言）：验证结果
    assert result is not None
    assert result.username == user_data["username"]
```

### FIRST 原则

- **Fast（快速）**: 测试应该快速执行
- **Independent（独立）**: 测试之间不应相互依赖
- **Repeatable（可重复）**: 测试结果应该一致
- **Self-Validating（自验证）**: 测试应该有明确的通过/失败结果
- **Timely（及时）**: 测试应该与代码同步编写

### 测试金字塔

```
        /\
       /  \        E2E Tests (10%)
      /____\       - 少量关键流程测试
     /      \
    /        \     Integration Tests (20%)
   /__________\    - 模块间交互测试
  /            \
 /              \  Unit Tests (70%)
/________________\ - 大量单元测试
```

---

## 使用指南

### simple-gemini 使用此模板

生成测试代码时，请参考 `references/test_patterns.md`：

1. 选择合适的测试类型（单元/集成/E2E）
2. 遵循 AAA 模式组织测试代码
3. 确保测试覆盖率达到目标值（从上下文读取 `[COVERAGE_TARGET: X%]`）
4. 包含正常路径和边界条件测试
5. 使用清晰的测试命名

### 覆盖率验证（codex-code-reviewer）

验证测试代码时，确保：

- 实际覆盖率 ≥ coverage_target（从上下文读取）
- 包含边界条件和异常处理测试
- 测试命名清晰、有意义
- 避免常见反模式（过度 Mock、测试私有方法等）

---

## 质量检查清单

生成测试代码时，确保通过以下检查：

- [ ] 遵循 AAA 模式（Arrange-Act-Assert）
- [ ] 测试命名清晰（`test_<function>_<scenario>_<expected>`）
- [ ] 覆盖正常路径和边界条件
- [ ] 适当使用 Mock/Stub（不过度 Mock）
- [ ] 测试独立，不依赖执行顺序
- [ ] 包含异常处理测试
- [ ] 测试覆盖率达到目标值（≥ coverage_target）
- [ ] 避免测试实现细节（测试公共接口）
