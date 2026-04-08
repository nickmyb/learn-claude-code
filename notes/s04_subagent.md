# Subagents

## break big tasks down

- 大任务拆小，每个小任务干净的上下文
- harness做上下文隔离 — 保护模型的思维清晰度

1. main agent 有 task 工具
2. sub agent 有所有基础工具，但没有 task（防止递归生成）
3. sub agent 返回的只有最终摘要文本，整个消息历史被丢弃