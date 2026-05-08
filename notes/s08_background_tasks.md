# Background Tasks

## Producer-Consumer模式的选择

## 对于LLM的信任

```
- git log --all --oneline -- docs/en/s08-background-tasks.md

  fix: remove hardcoded assistant acks after system message injection
  s08/s09/s10/s11/s_full inject background-results and inbox as user
  messages before LLM calls. The paired hardcoded assistant "Noted..."
  responses were unnecessary — consecutive user messages work fine and
  the fake acks added noise with no functional value.

  Affected: agents/s08, s09, s10, s11, s_full + docs (zh/en/ja s08, s09)
```

- [remove hardcoded assistant acks](https://github.com/shareAI-lab/learn-claude-code/commit/950378a)

## TODO

1. 测试hardcoded assistant acks对于Harness的影响
