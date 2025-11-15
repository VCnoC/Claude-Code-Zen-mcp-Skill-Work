# Mermaid 图表示例集合

> **用途**: 提供常用的 Mermaid 图表类型示例，包括流程图、时序图、状态图、ER图、类图、甘特图等。

---

## 1. 时序图（Sequence Diagram）

```mermaid
sequenceDiagram
    autonumber
    actor User as 用户
    participant App as 应用
    participant Auth as 认证服务
    participant DB as 数据库

    User->>App: 发起登录
    App->>Auth: 验证凭据
    Auth->>DB: 查询用户
    DB-->>Auth: 返回用户信息

    alt 验证成功
        Auth-->>App: 返回JWT令牌
        App-->>User: 登录成功
    else 验证失败
        Auth-->>App: 返回错误
        App-->>User: 登录失败
    end
```

---

## 2. 流程图（Flowchart）

```mermaid
flowchart TD
    Start([开始]) --> Input[/输入用户数据/]
    Input --> Validate{数据验证}

    Validate -->|无效| Error[显示错误]
    Error --> Input

    Validate -->|有效| CheckExists{用户是否存在}
    CheckExists -->|存在| Duplicate[提示用户已存在]
    Duplicate --> End([结束])

    CheckExists -->|不存在| CreateUser[创建用户]
    CreateUser --> SendEmail[发送欢迎邮件]
    SendEmail --> Success[显示成功消息]
    Success --> End
```

---

## 3. 状态图（State Diagram）

```mermaid
stateDiagram-v2
    [*] --> Idle: 初始化
    Idle --> Loading: 开始加载
    Loading --> Success: 加载成功
    Loading --> Error: 加载失败
    Success --> Idle: 重置
    Error --> Idle: 重试
    Success --> [*]: 完成
```

---

## 4. 实体关系图（ER Diagram）

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string customer_id PK
        string name
        string email UK
        date registered_at
    }
    ORDER ||--|{ LINE-ITEM : contains
    ORDER {
        string order_id PK
        string customer_id FK
        date order_date
        decimal total_amount
        string status
    }
    PRODUCT ||--o{ LINE-ITEM : "ordered in"
    PRODUCT {
        string product_id PK
        string name
        decimal price
        int stock_quantity
    }
    LINE-ITEM {
        string line_item_id PK
        string order_id FK
        string product_id FK
        int quantity
        decimal unit_price
    }
```

---

## 5. 类图（Class Diagram）

```mermaid
classDiagram
    class User {
        +String id
        +String username
        +String email
        -String password_hash
        +register()
        +login()
        +logout()
    }

    class Order {
        +String id
        +String user_id
        +DateTime created_at
        +Decimal total_amount
        +String status
        +create()
        +cancel()
        +complete()
    }

    class OrderItem {
        +String id
        +String order_id
        +String product_id
        +Integer quantity
        +Decimal price
        +add()
        +remove()
    }

    User "1" --> "*" Order : places
    Order "1" --> "*" OrderItem : contains
```

---

## 6. 甘特图（Gantt Chart）

```mermaid
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD
    section 阶段1: 需求分析
    需求收集           :a1, 2025-01-01, 5d
    需求评审           :a2, after a1, 2d
    section 阶段2: 设计
    架构设计           :b1, after a2, 3d
    UI设计             :b2, after a2, 4d
    section 阶段3: 开发
    后端开发           :c1, after b1, 10d
    前端开发           :c2, after b2, 10d
    section 阶段4: 测试
    单元测试           :d1, after c1, 3d
    集成测试           :d2, after c2, 3d
    section 阶段5: 部署
    部署上线           :e1, after d2, 2d
```

---

## 使用说明

### 选择合适的图表类型

| 图表类型 | 适用场景 | 关键词 |
|---------|----------|--------|
| 流程图 (Flowchart) | 业务流程、算法逻辑 | 条件判断、循环、分支 |
| 时序图 (Sequence) | API 交互、系统间通信 | 时间顺序、消息传递 |
| 状态图 (State) | 状态机、生命周期 | 状态转换、事件触发 |
| ER图 (ER Diagram) | 数据库设计、实体关系 | 表结构、外键关系 |
| 类图 (Class) | 面向对象设计、代码结构 | 类、继承、关联 |
| 甘特图 (Gantt) | 项目计划、时间线 | 任务安排、里程碑 |

### 质量检查清单

- [ ] 使用 Mermaid 语法（禁止 ASCII 图）
- [ ] 节点标识清晰（英文 ID + 中文说明）
- [ ] 图表可以正确渲染
- [ ] 适合文档场景（选择正确的图表类型）

---

*本文件提供常用 Mermaid 图表类型的可复用示例*
