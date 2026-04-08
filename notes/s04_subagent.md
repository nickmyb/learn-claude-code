# Subagents

## break big tasks down

- 大任务拆小，每个小任务干净的上下文
- harness做上下文隔离 — 保护模型的思维清晰度

1. main agent 有 task 工具
2. sub agent 有所有基础工具，但没有 task（防止递归生成）
3. sub agent 返回的只有最终摘要文本，整个消息历史被丢弃

## subagent context

- subagent
  - subagent隔离
  - system prompt
  - task

## subagent工具和权限控制

- 最小原则

## subagent has no task

```
Task 工具不包含在子代理的工具集中。
子代理必须直接完成工作，不能继续委派。
这防止了无限委派循环：没有这个约束，一个代理可能创建子代理，子代理又创建子代理，每一层都用略微不同的措辞重新委派同一任务，消耗 token 却毫无进展。
一层委派足以处理绝大多数场景。
如果任务对单个子代理来说太复杂，应该由父代理重新分解。
```