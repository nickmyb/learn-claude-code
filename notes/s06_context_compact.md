# Context Compact

## 三层压缩策略

- Stage 1: Micro -- shrink old tool_results automatic
- Stage 2: Auto -- summarize entire conversation at threshold
- Stage 3: /compact -- user-triggered, deepest compression

## 简易版本存在的几个问题

1. 磁盘存储的是micro_compact后的内容,不是原始内容
2. auto_compact后会丢失最新的用户消息