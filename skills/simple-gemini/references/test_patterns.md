# 测试代码模式与最佳实践

本文档提供测试代码编写的最佳实践、常用模式和示例，供 gemini 编写测试代码时参考。

## 一、测试组织原则

### 1.1 文件组织

**命名约定**：
- Python: `test_<module>.py` 或 `<module>_test.py`
- JavaScript: `<module>.test.js` 或 `<module>.spec.js`
- 测试文件应与被测试文件结构对应

**目录结构示例**：

```
项目根目录/
├── src/
│   ├── features.py
│   ├── model_training.py
│   └── utils/
│       └── helpers.py
└── tests/
    ├── test_features.py
    ├── test_model_training.py
    └── utils/
        └── test_helpers.py
```

### 1.2 测试分类

**单元测试（Unit Tests）**：
- 测试单个函数或类
- 隔离外部依赖（使用 mock）
- 快速执行（< 1 秒）

**集成测试（Integration Tests）**：
- 测试多个组件协作
- 可能涉及数据库、文件系统
- 执行时间较长

**端到端测试（E2E Tests）**：
- 测试完整用户流程
- 涉及真实环境
- 执行最慢，数量最少

---

## 二、AAA 模式（Arrange-Act-Assert）

### 2.1 基本结构

每个测试应遵循 AAA 模式：

```python
def test_example():
    # Arrange（准备）：设置测试数据和环境
    user = User(name="Alice", age=30)

    # Act（执行）：调用被测试的功能
    result = user.is_adult()

    # Assert（断言）：验证结果
    assert result == True
```

### 2.2 清晰的分段

使用注释或空行分隔三个阶段：

```python
def test_calculate_total_price():
    # Arrange
    cart = ShoppingCart()
    cart.add_item(Item(name="Book", price=29.99))
    cart.add_item(Item(name="Pen", price=5.00))

    # Act
    total = cart.calculate_total()

    # Assert
    assert total == 34.99
```

---

## 三、测试命名规范

### 3.1 描述性命名

测试名称应清晰描述：
1. 被测试的功能
2. 测试的场景
3. 预期的结果

**模式**：`test_<功能>_<场景>_<预期结果>`

**示例**：

```python
# 好的命名
def test_calculate_discount_with_valid_coupon_returns_discounted_price():
    pass

def test_login_with_invalid_password_raises_authentication_error():
    pass

def test_get_user_by_id_when_user_not_found_returns_none():
    pass

# 不好的命名（过于简略）
def test_discount():
    pass

def test_login():
    pass

def test_get_user():
    pass
```

### 3.2 中文命名（可选）

对于中文项目，可以使用中文测试名称：

```python
def test_计算折扣_使用有效优惠券_返回折扣价格():
    pass

def test_用户登录_密码错误_抛出认证异常():
    pass
```

---

## 四、Fixture 和 Setup/Teardown

### 4.1 Pytest Fixtures（推荐）

**基本 Fixture**：

```python
import pytest

@pytest.fixture
def sample_user():
    """创建测试用户"""
    return User(name="Alice", age=30)

def test_user_is_adult(sample_user):
    assert sample_user.is_adult() == True
```

**Fixture 作用域**：

```python
@pytest.fixture(scope="function")  # 每个测试函数执行一次（默认）
def temp_file():
    file = create_temp_file()
    yield file
    file.close()

@pytest.fixture(scope="module")  # 每个模块执行一次
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="session")  # 整个测试会话执行一次
def app_config():
    return load_config()
```

### 4.2 setUp 和 tearDown（Unittest）

```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """每个测试方法前执行"""
        self.calc = Calculator()

    def tearDown(self):
        """每个测试方法后执行"""
        self.calc = None

    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
```

---

## 五、Mock 和 Patch

### 5.1 为什么使用 Mock

- 隔离外部依赖（数据库、API、文件系统）
- 加快测试速度
- 模拟难以复现的场景（网络错误、边界条件）

### 5.2 使用 unittest.mock

**Mock 函数**：

```python
from unittest.mock import Mock

def test_send_notification():
    # Arrange
    mock_email_service = Mock()
    notifier = Notifier(email_service=mock_email_service)

    # Act
    notifier.send("Hello", to="user@example.com")

    # Assert
    mock_email_service.send_email.assert_called_once_with(
        subject="Hello",
        to="user@example.com"
    )
```

**Patch 模块**：

```python
from unittest.mock import patch

@patch('mymodule.external_api_call')
def test_fetch_data(mock_api):
    # Arrange
    mock_api.return_value = {"data": "test"}

    # Act
    result = fetch_user_data(user_id=123)

    # Assert
    assert result["data"] == "test"
    mock_api.assert_called_once_with(user_id=123)
```

**Mock 文件操作**：

```python
from unittest.mock import mock_open, patch

def test_read_config():
    mock_data = "key=value"

    with patch("builtins.open", mock_open(read_data=mock_data)):
        config = read_config_file("config.txt")
        assert config["key"] == "value"
```

### 5.3 Pytest-mock

```python
def test_database_query(mocker):
    # Arrange
    mock_db = mocker.patch('mymodule.database.query')
    mock_db.return_value = [{"id": 1, "name": "Alice"}]

    # Act
    users = get_all_users()

    # Assert
    assert len(users) == 1
    assert users[0]["name"] == "Alice"
```

---

## 六、断言最佳实践

### 6.1 清晰的断言消息

```python
# 好的断言
assert len(users) == 2, f"Expected 2 users, but got {len(users)}"

# 更好的断言（使用 pytest）
import pytest

def test_user_count():
    users = get_users()
    assert len(users) == 2, \
        f"Expected 2 users, but got {len(users)}: {users}"
```

### 6.2 具体的断言

```python
# 不好：过于宽泛
assert result  # 只检查非空

# 好：具体检查
assert result == [1, 2, 3]
assert result["status"] == "success"
assert result["data"]["user_id"] == 123
```

### 6.3 异常断言

**Pytest**：

```python
import pytest

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0

def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError, match="Invalid input"):
        process_data("invalid")
```

**Unittest**：

```python
import unittest

class TestValidator(unittest.TestCase):
    def test_invalid_email_raises_error(self):
        with self.assertRaises(ValueError):
            validate_email("invalid-email")

        # 检查异常消息
        with self.assertRaisesRegex(ValueError, "Invalid email"):
            validate_email("invalid-email")
```

---

## 七、边界条件和边缘情况

### 7.1 常见边界条件

**数值边界**：

```python
def test_age_validation():
    # 正常值
    assert is_valid_age(25) == True

    # 边界值
    assert is_valid_age(0) == True
    assert is_valid_age(150) == True

    # 超出边界
    assert is_valid_age(-1) == False
    assert is_valid_age(151) == False
```

**集合边界**：

```python
def test_list_operations():
    # 空列表
    assert sum_list([]) == 0

    # 单元素
    assert sum_list([5]) == 5

    # 多元素
    assert sum_list([1, 2, 3]) == 6
```

### 7.2 特殊值

```python
def test_special_values():
    # None
    assert process_data(None) == None

    # 空字符串
    assert validate_string("") == False

    # 空白字符串
    assert validate_string("   ") == False

    # 极大值
    assert calculate(float('inf')) == float('inf')

    # NaN
    import math
    assert math.isnan(calculate(float('nan')))
```

---

## 八、参数化测试

### 8.1 Pytest 参数化

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (-2, 4),
])
def test_square(input, expected):
    assert square(input) == expected
```

**多个参数**：

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### 8.2 Unittest 参数化（使用 subTest）

```python
import unittest

class TestMath(unittest.TestCase):
    def test_square(self):
        test_cases = [
            (0, 0),
            (1, 1),
            (2, 4),
            (3, 9),
            (-2, 4),
        ]

        for input, expected in test_cases:
            with self.subTest(input=input):
                self.assertEqual(square(input), expected)
```

---

## 九、测试数据管理

### 9.1 测试数据生成

**使用 Factory**：

```python
class UserFactory:
    @staticmethod
    def create(name="Test User", age=30, email=None):
        if email is None:
            email = f"{name.lower().replace(' ', '_')}@test.com"
        return User(name=name, age=age, email=email)

def test_user_creation():
    user = UserFactory.create(name="Alice", age=25)
    assert user.name == "Alice"
    assert user.email == "alice@test.com"
```

**使用 Faker（生成随机数据）**：

```python
from faker import Faker

fake = Faker()

def test_with_random_data():
    user = User(
        name=fake.name(),
        email=fake.email(),
        address=fake.address()
    )
    assert user.is_valid()
```

### 9.2 测试数据文件

```python
import json
import pytest

@pytest.fixture
def sample_data():
    with open("tests/fixtures/sample_data.json") as f:
        return json.load(f)

def test_process_data(sample_data):
    result = process(sample_data)
    assert result["status"] == "success"
```

---

## 十、测试覆盖率

### 10.1 覆盖率要求

- **最低要求**：70% 行覆盖率
- **推荐**：80-90% 行覆盖率
- **关键模块**：100% 行覆盖率

### 10.2 运行覆盖率检查

```bash
# Pytest with coverage
pytest --cov=src --cov-report=html tests/

# 只显示未覆盖的行
pytest --cov=src --cov-report=term-missing tests/

# 设置最低覆盖率要求
pytest --cov=src --cov-fail-under=70 tests/
```

### 10.3 忽略特定代码

```python
def debug_function():  # pragma: no cover
    """调试用函数，不需要测试"""
    print("Debug info")
```

---

## 十一、完整示例

### 11.1 Python 单元测试示例

**被测试代码（src/calculator.py）**：

```python
class Calculator:
    def add(self, a, b):
        """加法"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numbers")
        return a + b

    def divide(self, a, b):
        """除法"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numbers")
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
```

**测试代码（tests/test_calculator.py）**：

```python
import pytest
from src.calculator import Calculator

class TestCalculator:
    """Calculator 类的测试套件"""

    @pytest.fixture
    def calc(self):
        """创建 Calculator 实例"""
        return Calculator()

    # ===== 加法测试 =====

    def test_add_positive_numbers(self, calc):
        """测试加法 - 正数"""
        # Arrange
        a, b = 2, 3

        # Act
        result = calc.add(a, b)

        # Assert
        assert result == 5

    def test_add_negative_numbers(self, calc):
        """测试加法 - 负数"""
        assert calc.add(-1, -1) == -2

    def test_add_zero(self, calc):
        """测试加法 - 零"""
        assert calc.add(5, 0) == 5
        assert calc.add(0, 5) == 5

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (0.1, 0.2, 0.3),
    ])
    def test_add_parametrized(self, calc, a, b, expected):
        """测试加法 - 参数化"""
        assert calc.add(a, b) == pytest.approx(expected)

    def test_add_invalid_type_raises_type_error(self, calc):
        """测试加法 - 无效类型"""
        with pytest.raises(TypeError, match="Inputs must be numbers"):
            calc.add("1", 2)

    # ===== 除法测试 =====

    def test_divide_positive_numbers(self, calc):
        """测试除法 - 正数"""
        assert calc.divide(10, 2) == 5

    def test_divide_by_zero_raises_error(self, calc):
        """测试除法 - 除以零"""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(10, 0)

    def test_divide_negative_numbers(self, calc):
        """测试除法 - 负数"""
        assert calc.divide(-10, 2) == -5
        assert calc.divide(10, -2) == -5

    def test_divide_invalid_type_raises_type_error(self, calc):
        """测试除法 - 无效类型"""
        with pytest.raises(TypeError):
            calc.divide(10, "2")
```

### 11.2 集成测试示例

**被测试代码（src/user_service.py）**：

```python
class UserService:
    def __init__(self, database, email_service):
        self.database = database
        self.email_service = email_service

    def create_user(self, name, email):
        """创建用户并发送欢迎邮件"""
        # 验证邮箱格式
        if "@" not in email:
            raise ValueError("Invalid email format")

        # 保存到数据库
        user_id = self.database.save_user(name, email)

        # 发送欢迎邮件
        self.email_service.send_welcome_email(email, name)

        return user_id
```

**测试代码（tests/test_user_service.py）**：

```python
import pytest
from unittest.mock import Mock
from src.user_service import UserService

class TestUserService:
    """UserService 集成测试"""

    @pytest.fixture
    def mock_database(self):
        """创建 mock 数据库"""
        db = Mock()
        db.save_user.return_value = 123  # 返回用户 ID
        return db

    @pytest.fixture
    def mock_email_service(self):
        """创建 mock 邮件服务"""
        return Mock()

    @pytest.fixture
    def user_service(self, mock_database, mock_email_service):
        """创建 UserService 实例"""
        return UserService(mock_database, mock_email_service)

    def test_create_user_success(self, user_service, mock_database, mock_email_service):
        """测试创建用户 - 成功"""
        # Arrange
        name = "Alice"
        email = "alice@example.com"

        # Act
        user_id = user_service.create_user(name, email)

        # Assert
        assert user_id == 123
        mock_database.save_user.assert_called_once_with(name, email)
        mock_email_service.send_welcome_email.assert_called_once_with(email, name)

    def test_create_user_invalid_email(self, user_service):
        """测试创建用户 - 无效邮箱"""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user("Alice", "invalid-email")

    def test_create_user_database_error(self, user_service, mock_database):
        """测试创建用户 - 数据库错误"""
        # Arrange
        mock_database.save_user.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            user_service.create_user("Alice", "alice@example.com")
```

---

## 十二、测试代码质量检查清单

编写测试代码后，检查：

### 基础质量
- [ ] 每个测试函数只测试一个功能点
- [ ] 测试名称清晰描述测试内容
- [ ] 遵循 AAA 模式（Arrange-Act-Assert）
- [ ] 没有重复代码（使用 fixture 或 helper 函数）

### 覆盖完整性
- [ ] 覆盖正常情况（happy path）
- [ ] 覆盖边界条件（边界值、空值、极值）
- [ ] 覆盖异常情况（错误输入、异常抛出）
- [ ] 覆盖率 ≥ 70%

### 断言质量
- [ ] 断言具体且明确
- [ ] 断言包含错误消息
- [ ] 没有冗余断言

### 独立性
- [ ] 测试之间互不依赖
- [ ] 测试顺序可以任意调整
- [ ] 每个测试都有清理（teardown）

### Mock 使用
- [ ] 外部依赖已 mock
- [ ] Mock 调用已验证
- [ ] Mock 返回值合理

### 可维护性
- [ ] 代码易读易懂
- [ ] 使用了适当的 fixture
- [ ] 测试数据清晰
- [ ] 有必要的注释

---

## 十三、常见反模式（避免）

### ❌ 测试实现细节而非行为

```python
# 不好：测试实现细节
def test_sort_uses_quicksort():
    assert sort_algorithm == "quicksort"

# 好：测试行为
def test_sort_returns_sorted_list():
    assert sort([3, 1, 2]) == [1, 2, 3]
```

### ❌ 测试过于复杂

```python
# 不好：一个测试做太多事情
def test_everything():
    user = create_user()
    login(user)
    create_post(user)
    delete_post(user)
    logout(user)
    # 太多逻辑，难以定位问题

# 好：拆分成多个测试
def test_create_user():
    user = create_user()
    assert user is not None

def test_user_can_login():
    user = create_user()
    result = login(user)
    assert result == True
```

### ❌ 测试之间有依赖

```python
# 不好：测试有顺序依赖
class TestUser:
    user = None

    def test_1_create_user(self):
        self.user = create_user("Alice")

    def test_2_update_user(self):
        # 依赖 test_1_create_user
        update_user(self.user, name="Bob")

# 好：每个测试独立
class TestUser:
    @pytest.fixture
    def user(self):
        return create_user("Alice")

    def test_create_user(self):
        user = create_user("Alice")
        assert user.name == "Alice"

    def test_update_user(self, user):
        update_user(user, name="Bob")
        assert user.name == "Bob"
```

### ❌ 没有断言

```python
# 不好：只执行不验证
def test_process_data():
    process_data({"key": "value"})
    # 没有断言，测试无意义

# 好：有明确断言
def test_process_data():
    result = process_data({"key": "value"})
    assert result["status"] == "success"
```

---

## 使用建议

1. **先写简单测试**：从正常情况开始，逐步添加边界和异常测试
2. **保持测试简单**：每个测试只验证一个行为
3. **使用 fixture**：减少重复代码，提高可维护性
4. **参数化测试**：相似测试用参数化合并
5. **Mock 外部依赖**：加快测试速度，提高可靠性
6. **定期审查**：检查测试覆盖率和测试质量
