# (Test Best Practices)

> ****: Mock

---


##

###

```
test_<function>_<scenario>_<expected_result>
```

###

** **:
```python
def test_create_user_with_valid_data_returns_user_object():
    pass

def test_create_user_with_duplicate_email_raises_value_error():
    pass

def test_get_user_by_id_with_nonexistent_id_returns_none():
    pass
```

** **:
```python
def test_user():  #
    pass

def test_create():  #
    pass

def test_1():  #
    pass
```

### JavaScript / TypeScript

```javascript
//
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user successfully with valid data', () => {});
    it('should throw error when email already exists', () => {});
    it('should throw error for invalid email format', () => {});
  });
});

//
describe('Tests', () => {
  it('works', () => {});  //
  it('test1', () => {});  //
});
```

---

##

### Python

```
project/
 src/
    services/
       user_service.py
    models/
       user.py
    api/
        user_api.py
 tests/
     unit/
        services/
           test_user_service.py
        models/
            test_user.py
     integration/
        test_user_api.py
     e2e/
        test_user_flow.py
     fixtures/
        user_fixtures.py
     conftest.py
```

### JavaScript / TypeScript

```
project/
 src/
    services/
       UserService.ts
    models/
       User.ts
    api/
        userApi.ts
 tests/
     unit/
        services/
           UserService.test.ts
        models/
            User.test.ts
     integration/
        userApi.test.ts
     e2e/
        userFlow.spec.ts
     fixtures/
         userFixtures.ts
```

---

## Mock Stub

### Python Mock

```python
from unittest.mock import Mock, patch, MagicMock

# 1. Mock
def test_with_mock_object():
    #  Mock
    mock_db = Mock()
    mock_db.find_by_id.return_value = {"id": "123", "name": "Test"}

    #  Mock
    service = UserService(db=mock_db)
    result = service.get_user("123")

    #
    mock_db.find_by_id.assert_called_once_with("123")
    assert result["name"] == "Test"

# 2. Patch
@patch('src.services.user_service.Database')
def test_with_patch_decorator(mock_database):
    mock_database.return_value.find_by_id.return_value = {"id": "123"}

    service = UserService()
    result = service.get_user("123")

    assert result["id"] == "123"

# 3. Patch
def test_with_patch_context():
    with patch('src.services.user_service.Database') as mock_db:
        mock_db.return_value.find_by_id.return_value = {"id": "123"}

        service = UserService()
        result = service.get_user("123")

        assert result["id"] == "123"

# 4. Mock
def test_mock_side_effect():
    mock_api = Mock()
    #
    mock_api.get_data.side_effect = ["data1", "data2", "data3"]

    assert mock_api.get_data() == "data1"
    assert mock_api.get_data() == "data2"
    assert mock_api.get_data() == "data3"

# 5. Mock
def test_mock_exception():
    mock_api = Mock()
    mock_api.get_data.side_effect = ConnectionError("Network error")

    with pytest.raises(ConnectionError):
        mock_api.get_data()
```

### JavaScript Mock

```javascript
// 1. Jest Mock
test('should call callback with data', () => {
  const mockCallback = jest.fn();
  const data = { id: '123', name: 'Test' };

  processData(data, mockCallback);

  expect(mockCallback).toHaveBeenCalledWith(data);
  expect(mockCallback).toHaveBeenCalledTimes(1);
});

// 2. Mock
jest.mock('../src/services/Database', () => {
  return {
    Database: jest.fn().mockImplementation(() => {
      return {
        findById: jest.fn().mockResolvedValue({ id: '123' })
      };
    })
  };
});

// 3. Spy
test('should spy on method', () => {
  const user = new User();
  const spy = jest.spyOn(user, 'save');

  user.update({ name: 'New Name' });

  expect(spy).toHaveBeenCalled();
  spy.mockRestore();
});

// 4. Mock
test('should mock implementation', () => {
  const mockFn = jest.fn().mockImplementation((x) => x * 2);

  expect(mockFn(2)).toBe(4);
  expect(mockFn(3)).toBe(6);
});

// 5. Mock
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

##

### Fixture

**Python (pytest)**:
```python
# tests/conftest.py
import pytest
from src.models.user import User

@pytest.fixture
def sample_user():
    """"""
    return User(
        id="usr_001",
        username="testuser",
        email="test@example.com"
    )

@pytest.fixture
def user_list():
    """"""
    return [
        User(id=f"usr_{i:03d}", username=f"user{i}", email=f"user{i}@test.com")
        for i in range(1, 6)
    ]

@pytest.fixture(scope="session")
def database():
    """ fixture"""
    db = Database()
    db.connect()
    yield db
    db.disconnect()
```

### Factory

```python
# tests/factories.py
from datetime import datetime

class UserFactory:
    """"""

    @staticmethod
    def create(overrides=None):
        """"""
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
        """"""
        return [
            UserFactory.create({
                **kwargs,
                "id": f"usr_{i:03d}",
                "username": f"user{i}",
                "email": f"user{i}@test.com"
            })
            for i in range(1, count + 1)
        ]

#
def test_with_factory():
    user = UserFactory.create({"username": "custom_user"})
    users = UserFactory.create_batch(5)
```

---

##

### (Benchmark)

```python
import pytest
import time

@pytest.mark.benchmark
def test_user_creation_performance(benchmark):
    """"""

    def create_user():
        return UserService().create_user({
            "username": "testuser",
            "email": "test@example.com",
            "password": "Pass123"
        })

    result = benchmark(create_user)
    assert result is not None

    #
    assert benchmark.stats['mean'] < 0.1  #  100ms
```

### (Load Test)

```python
import concurrent.futures

def test_concurrent_user_creation():
    """"""
    service = UserService()
    user_count = 100

    def create_user(index):
        return service.create_user({
            "username": f"user{index}",
            "email": f"user{index}@test.com",
            "password": "Pass123"
        })

    #
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_user, i) for i in range(user_count)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(results) == user_count
    assert all(r is not None for r in results)
```

---

##

### 1:

```python
#
class TestBadOrder:
    def test_01_create_user(self):
        self.user_id = create_user()

    def test_02_update_user(self):
        update_user(self.user_id)  #

#
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

### 2: Mock

```python
#  Mock
def test_too_much_mocking():
    mock_db = Mock()
    mock_cache = Mock()
    mock_logger = Mock()
    mock_validator = Mock()
    mock_emailer = Mock()
    # ...  Mock

#   Mock
def test_appropriate_mocking():
    #  Mock API
    with patch('src.services.external_api.ExternalAPI') as mock_api:
        mock_api.return_value.get_data.return_value = {"key": "value"}
        result = service.process_data()
        assert result is not None
```

### 3:

```python
#
def test_private_method():
    service = UserService()
    result = service._validate_email("test@example.com")  #
    assert result is True

#
def test_public_interface():
    service = UserService()
    user = service.create_user({
        "email": "test@example.com",
        "username": "testuser",
        "password": "Pass123"
    })
    assert user.email == "test@example.com"  #
```

### 4:

```python
#
def test_only_happy_path():
    result = divide(10, 2)
    assert result == 5

#
def test_with_boundary_conditions():
    assert divide(10, 2) == 5  #
    assert divide(0, 5) == 0   #
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)  #
    assert divide(-10, 2) == -5  #
```

---

##

### AAA Arrange-Act-Assert

```python
def test_with_aaa_pattern():
    # Arrange
    user_data = {"username": "test", "email": "test@example.com"}
    service = UserService()

    # Act
    result = service.create_user(user_data)

    # Assert
    assert result is not None
    assert result.username == user_data["username"]
```

### FIRST

- **Fast**:
- **Independent**:
- **Repeatable**:
- **Self-Validating**: /
- **Timely**:

###

```
        /\
       /  \        E2E Tests (10%)
      /____\       -
     /      \
    /        \     Integration Tests (20%)
   /__________\    -
  /            \
 /              \  Unit Tests (70%)
/________________\ -
```

---

##

### simple-gemini

 `references/test_patterns.md`

1. //E2E
2. AAA
3. `[COVERAGE_TARGET: X%]`
4.
5.

### codex-code-reviewer



- ≥ coverage_target
-
-
- Mock

---

##



- [ ] AAA Arrange-Act-Assert
- [ ] `test_<function>_<scenario>_<expected>`
- [ ]
- [ ] Mock/Stub Mock
- [ ]
- [ ]
- [ ] ≥ coverage_target
- [ ]
