# 单元测试模式 (Unit Test Patterns)

> **用途**: 提供单元测试的标准模板和示例代码（Python pytest 和 JavaScript Jest）。

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
