# Mergio Skills

Mergio Agent 官方公开 Skills 库 — 按领域分类的即用型 Agent 技能。

## 使用方式

```bash
# 通过 npx skills 安装（社区标准）
npx skills add Mergio-AI/skills --skill postgres-schema-inspection

# 或直接从 Mergio Dashboard 一键安装
```

## 当前 Skills

| Skill | 分类 | 说明 |
|-------|------|------|
| `postgres-schema-inspection` | devops | PostgreSQL 数据库结构检测（读权限用户兼容） |
| `request-troubleshooting` | devops | API 请求异常排查通用方法论 |
| `static-site-publishing` | devops | 静态站点发布完整流程 |
| `configure-mcp` | mcp | MCP 服务配置：原生 vs mcporter 双路径 |

## Skill 结构

```
category/
  skill-name/
    SKILL.md          ← 主指令（YAML frontmatter + markdown）
    references/       ← API 文档、错误码对照表
    scripts/          ← setup.sh、validate.py
    templates/        ← 配置模板
```

## 提交 Skill

欢迎提交 PR。请确保：

1. YAML frontmatter 完整（name, description, version, tags）
2. 有 Overview + Prerequisites + Pitfalls 段
3. 无硬编码密钥/密码
4. 代码示例可运行

详见 [Skills 编写规范](https://hermes-daqiezi.mergio.dev/skills-authoring-best-practices.html)。
