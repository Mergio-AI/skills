# Hermes Skills

Hermes Agent 通用 Skills 仓库 — 所有 Agent 共享的技能文件，按领域分类组织。

## 同步机制

| 时间 | 动作 | 执行者 | 脚本 |
|------|------|--------|------|
| 每天 03:00 | 推送 Skills 变更 PR | 从 Agent | `scripts/skill-push-pr.sh` |
| 03:30 | Review + 合并 PR | 主 Agent | 手动或 CI |
| 04:00 | 全量 Agent 拉取最新 | 所有 Agent | `scripts/skill-pull.sh` |

### Cron 配置

```bash
# 从 Agent（大茄子）— 03:00 推送 PR
hermes cron create \
  --name "skill-sync-push" \
  --schedule "0 3 * * *" \
  --script scripts/skill-push-pr.sh \
  --no-agent \
  --workdir /opt/data/hermes-skills

# 所有 Agent — 04:00 拉取
hermes cron create \
  --name "skill-sync-pull" \
  --schedule "0 4 * * *" \
  --script scripts/skill-pull.sh \
  --no-agent \
  --workdir /opt/data/hermes-skills
```

`scripts/skill-push-pr.sh` 在没有变更时静默退出，不会产生空 PR。

## 当前 Skills

| Skill | 分类 | 说明 |
|-------|------|------|
| `configure-mcp` | mcp | MCP 服务配置方法论（原生 vs mcporter） |
| `postgres-schema-inspection` | devops | PostgreSQL 数据库结构检测 |
| `request-troubleshooting` | devops | API 请求异常排查（通用方法论） |
| `static-site-publishing` | devops | 静态站点发布（搭建 + 使用） |

## 添加新 Skill

1. 在对应分类目录下创建 Skill 子目录
2. 编写 `SKILL.md`（参考现有格式）
3. 可选的 `references/`、`scripts/`、`templates/` 子目录
4. 提交 → 推送 PR → 等待合并 → 所有 Agent 04:00 自动同步

## 使用方式

```bash
# 安装到本地 Hermes
git clone git@github.com:aicodewith-team/hermes-skills.git ~/.hermes/skills/hermes-skills

# 或通过 Hermes CLI
hermes skills install --repo aicodewith-team/hermes-skills
```
