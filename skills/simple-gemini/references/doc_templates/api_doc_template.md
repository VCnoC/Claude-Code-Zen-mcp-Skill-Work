# API 文档章节模板

> **用途**: 提供标准的 API 文档模板，包含完整的端点定义、请求/响应示例和错误码。

---

## RESTful API 示例

### 端点: 创建用户

**请求**:
```http
POST /api/v1/users
Content-Type: application/json
Authorization: Bearer <token>

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "profile": {
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**响应** (201 Created):
```json
{
  "id": "usr_1234567890",
  "username": "john_doe",
  "email": "john@example.com",
  "profile": {
    "first_name": "John",
    "last_name": "Doe"
  },
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

**错误响应**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "provided": "invalid-email"
    }
  }
}
```

**状态码**:
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `409` - 用户已存在
- `500` - 服务器错误

---

## 使用说明

### 何时使用此模板

- 编写项目的 API 文档章节
- 补充既有项目缺失的 API 说明
- 标准化 API 文档格式

### 自定义要点

1. **端点描述**: 包含 HTTP 方法、路径、描述
2. **请求示例**: 包含完整的请求头和请求体
3. **响应示例**: 包含成功和错误响应
4. **状态码**: 列出所有可能的 HTTP 状态码及其含义

---

*本模板提供标准 API 文档格式，确保与实际代码实现保持一致*
