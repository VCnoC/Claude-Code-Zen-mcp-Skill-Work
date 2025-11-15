# Skills Shared - 跨技能共享资源

> 存放多个技能共同使用的模板、工具和组件。

## 📁 当前内容

| 文件 | 用途 | 使用技能 |
|------|------|---------|
| `auto_log_template.md` | 自动化决策日志统一模板（automation_mode=true 时） | codex / simple-gemini / deep-gemini / plan-down |

## 🔗 与 references/standards/ 的区别

| 维度 | skills/shared/ | references/standards/ |
|------|---------------|---------------------|
| **内容类型** | 可复用的模板、组件、工具 | 操作规范、流程标准 |
| **使用方式** | 作为模板填充、作为组件引用 | 作为规范遵守、作为流程执行 |
| **变更频率** | 较低（结构稳定） | 极低（标准固化） |

## 📝 引用格式

**在 CLAUDE.md「共享概念」中**：
```markdown
### auto_log (自动化决策日志)
- **模板**: 统一使用 `skills/shared/auto_log_template.md`
```

**在技能 SKILL.md 中**：
```markdown
auto_log 的定义与约束见 CLAUDE.md「共享概念速查」
模板文件：`skills/shared/auto_log_template.md`
```

## ➕ 添加原则

新增内容需满足以下**全部条件**：

1. **复用性**：至少 2 个技能使用
2. **稳定性**：结构不频繁变更
3. **接口明确**：有清晰的使用说明和填充规范
4. **独立性**：可单独复制到其他项目使用

**不符合条件的内容**：
- 仅 1 个技能使用 → 放该技能的 `references/` 目录
- 操作规范或流程 → 放 `references/standards/`
- 概念定义 → 放 CLAUDE.md「共享概念」
