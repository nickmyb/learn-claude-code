# Agent Teams

## 没有解决多个agent之间的合作

1. subagent: 隔离context的LLM调用后返回summary
2. background tasks: 子进程run shell command
3. agent teams: main agent可以spawn, agents之间可以互相send, 但任务的执行结果并不会返回调用者(后续需要解决的问题)

## MessageBus

1. 向指定jsonl追加JSON content
2. 读取指定jsonl中所有JSON内容并清空
3. 通过send广播消息

## TeammateManager

1. 只有main agent有spawn
2. 记录所有的agent
3. spawn subagent
4. 当前版本agent之间只能收发消息,但对于任务的结果的回传是不强制的
  - 会出现agent处理完了任务,但没有通过message回传到分配任务的agent中,没有send message到from

```
def _teammate_loop(self, name, role, prompt):
    messages = [...]
    exit_reason = "completed"
    final_text = ""
    for i in range(50):
        # ... 现有逻辑 ...
        if response.stop_reason != "tool_use":
            final_text = extract_text(response)
            break
    else:
        exit_reason = "turn_limit_exceeded"
    
    # 不管怎么出来的，至少给 lead 留个字条
    BUS.send(name, "lead", json.dumps({
        "type": "teammate_exit",
        "reason": exit_reason,
        "last_message": final_text[:500],
        "turns_used": i + 1,
    }))
    self._find_member(name)["status"] = "idle"
```
