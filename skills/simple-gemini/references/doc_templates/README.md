# 文档模板集合 (Documentation Templates)

> 为 simple-gemini 技能提供标准化文档模板，确保生成的文档符合项目规范。

## 可用模板

| 文件名 | 用途 |
|--------|------|
| `projectwiki_template.md` | PROJECTWIKI.md 标准模板（生成项目知识库文档） |
| `readme_template.md` | README.md 标准模板（生成项目说明文档） |
| `changelog_template.md` | CHANGELOG.md 标准模板（生成变更日志） |
| `architecture_template.md` | 架构设计章节模板（生成架构设计文档） |
| `api_doc_template.md` | API 文档章节模板（生成 API 文档） |
| `mermaid_examples.md` | Mermaid 图表示例集合（流程图、时序图、状态图） |

## 质量标准（生成文档时必须满足）

1. **必备章节**: PROJECTWIKI 包含 12 个标准章节
2. **可视化**: 至少包含 1 个 Mermaid 代码块
3. **链接有效**: 所有相对链接指向存在的文件
4. **一致性**: API 定义与代码实现保持一致
5. **版本规范**: CHANGELOG 遵循 Keep a Changelog + SemVer
