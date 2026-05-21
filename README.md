# Hermes Skills

Hermes Agent 通用 Skills 仓库 — 所有 Agent 共享的技能文件，按领域分类组织。

## 同步机制

| 时间 | 动作 | 执行者 |
|------|------|--------|
| 每天 03:00 | 自动推送 Skills 变更 PR | 主 Agent（大白菜 / 大茄子） |
| 03:30 | PR 自动合并 | CI |
| 04:00 | 全量 Agent 拉取最新 Skills | 所有 Agent |

## 目录结构

```
hermes-skills/
├── autonomous-ai-agents/    # AI Agent 工具链
├── creative/                # 创意与设计
├── data-science/            # 数据科学
├── devops/                  # DevOps 通用
├── email/                   # 邮件
├── gaming/                  # 游戏
├── github/                  # GitHub 工作流
├── mcp/                     # MCP 协议
├── media/                   # 媒体处理
├── mlops/                   # ML 工程
├── note-taking/             # 笔记
├── productivity/            # 生产力工具
├── red-teaming/             # 红队测试
├── research/                # 学术研究
├── smart-home/              # 智能家居
├── social-media/            # 社交媒体
├── software-development/    # 软件开发方法论
└── README.md
```

每个目录下是独立的 Skill 子目录，内含 `SKILL.md` 及相关资源。

## 使用方式

1. Agent 启动时自动加载 Skills 索引
2. 通过 Hermes Skill 管理器安装：`hermes skills install <name>`
3. 或直接 clone 到 `~/.hermes/skills/` 目录
