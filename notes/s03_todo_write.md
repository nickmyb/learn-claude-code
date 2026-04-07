# TodoWrite

## 1 task In-Progress

- 任务的上下文切换会导致过程的不可控,单任务让可靠性产生巨大提高

## TodoWrite(Not TodoUpdate)

- LLM 擅长生成结构化状态数据
- LLM 不擅长数据的变更操作
- 让模型决定高层意图（做什么）
- 不让模型操心低层实现（怎么做到）

```
# 工具定义：多个操作
tools = [
    {"name": "todo_add", "input_schema": {"text": str}},
    {"name": "todo_remove", "input_schema": {"id": str}},
    {"name": "todo_update_status", "input_schema": {"id": str, "status": str}},
    {"name": "todo_update_text", "input_schema": {"id": str, "text": str}},
]

# LLM 的思考负担：
"""
当前状态：
  [x] #1: 读取文件
  [>] #2: 分析代码  
  [ ] #3: 写测试

我完成了分析代码，要开始写测试了。
我需要：
  1. 调用 todo_update_status(id="2", status="completed")  
  2. 调用 todo_update_status(id="3", status="in_progress")
  
等等，顺序对吗？要是我先把 3 设成 in_progress，
会不会违反"只能有一个 in_progress"的规则？
应该先完成 2，再开始 3...
"""

# LLM 可能犯的错：
# - 忘记更新某个任务
# - 操作顺序错误导致违反约束
# - 搞混 id
# - 选错工具（用了 update_text 而不是 update_status）
```

```
# 工具定义：一个工具，全量状态
tools = [
    {
        "name": "todo_update",
        "input_schema": {
            "items": [{"id": str, "text": str, "status": str}, ...]
        }
    }
]

# LLM 的思考负担：
"""
当前状态：
  [x] #1: 读取文件
  [>] #2: 分析代码  
  [ ] #3: 写测试

我完成了分析代码，要开始写测试了。
新状态应该是：
  #1: 读取文件 - completed（不变）
  #2: 分析代码 - completed（改）
  #3: 写测试 - in_progress（改）
  
直接输出这个列表。
"""

# LLM 的输出：
tool_use(name="todo_update", input={
    "items": [
        {"id": "1", "text": "读取文件", "status": "completed"},
        {"id": "2", "text": "分析代码", "status": "completed"},
        {"id": "3", "text": "写测试", "status": "in_progress"},
    ]
})

# 框架负责验证：
# - 只有一个 in_progress？✅
# - 不超过 20 个？✅
# - 状态值合法？✅
```

```
┌─────────────────────────────────────────────────────────────────┐
│  操作式："我要做什么变更"                                        │
│                                                                 │
│  LLM 需要：                                                     │
│    1. 理解当前状态                                               │
│    2. 计算差异（什么变了）                                       │
│    3. 转换成操作序列（add? remove? update?）                     │
│    4. 确保操作顺序正确                                           │
│    5. 确保不违反约束                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  状态式："最终应该是什么"                                        │
│                                                                 │
│  LLM 只需要：                                                   │
│    1. 输出期望的最终状态                                         │
│                                                                 │
│  框架负责：                                                      │
│    - 验证约束                                                    │
│    - 计算差异（如果需要）                                        │
│    - 执行变更                                                    │
└─────────────────────────────────────────────────────────────────┘
```

## tool的设计很关键

- 一般状态式更容易处理 全量更新

```
┌─────────────────────────────────────────────────────────────────┐
│  1. 默认用状态式                                                 │
│     除非有明确理由用操作式                                       │
├─────────────────────────────────────────────────────────────────┤
│  2. 数据量是关键分界线                                           │
│     < 10KB  → 状态式                                            │
│     > 100KB → 操作式                                            │
├─────────────────────────────────────────────────────────────────┤
│  3. 有约束 → 状态式                                              │
│     框架一次性验证比 LLM 多步操作更可靠                          │
├─────────────────────────────────────────────────────────────────┤
│  4. 有成熟 DSL → 操作式                                          │
│     SQL、Git、正则替换 等 LLM 已经很熟悉                         │
├─────────────────────────────────────────────────────────────────┤
│  5. 不确定时，问自己：                                           │
│     "如果 LLM 犯错，状态式和操作式哪个更容易恢复？"               │
│     通常状态式更容易：直接传正确状态就行                          │
└─────────────────────────────────────────────────────────────────┘
```

### 工具设计 Checklist

#### 倾向状态式
- [ ] 数据量小（<100 项，<10KB）
- [ ] 有复杂约束（同时只能一个 in_progress）
- [ ] 操作之间有依赖或顺序要求
- [ ] 状态是用户可见的（UI 展示）
- [ ] 需要原子性（要么全成功，要么全失败）

#### 倾向操作式
- [ ] 数据量大（无法全量传递）
- [ ] 操作有成熟的 DSL（SQL、Git 命令）
- [ ] 操作是幂等的（执行多次结果相同）
- [ ] 需要追踪操作历史（审计日志）
- [ ] 底层系统本身是操作式 API

#### 混合式策略
- [ ] 读操作用查询式
- [ ] 小范围写操作用状态式
- [ ] 大范围写操作用操作式 + 确认机制

## Prompt Engineering Tag语义

### 举例

```
# 场景：LLM 正在连续调用 bash 调试一个问题

# 用 <command>：
"""
LLM 收到：<command>Update your todos.</command>
LLM 反应：好的，我必须先更新 todo...
         （放弃当前调试，去更新 todo）
         （然后忘记之前调试到哪了）
"""

# 用 <reminder>：
"""
LLM 收到：<reminder>Update your todos.</reminder>
LLM 反应：收到提醒，但我现在在调试关键问题，
         我再执行一两个命令确认结果，
         然后更新 todo 记录进度。
"""
```

### 常用Tag

```
# Prompt Engineering 中常见的 tag 选择

# 强制/系统级
<system>        # 系统指令，最高优先级
<instruction>   # 明确指令
<rule>          # 必须遵守的规则
<constraint>    # 约束条件

# 建议/提示级
<reminder>      # 温和提醒
<hint>          # 提示
<suggestion>    # 建议
<nudge>         # 轻推

# 信息/上下文级
<context>       # 背景信息
<note>          # 备注
<info>          # 一般信息
<observation>   # 观察到的情况

# 特殊用途
<thinking>      # 思考过程
<scratchpad>    # 草稿区
<error>         # 错误信息
<warning>       # 警告

# 结构类（组织 prompt）
<system>         # 系统级设置
<instructions>   # 指令
<context>        # 背景/上下文
<input>          # 用户输入
<output>         # 期望输出格式
<examples>       # 示例集合
<constraints>    # 约束条件

# 文档类
<document>       # 文档
<source>         # 来源
<data>           # 数据

# 思考类
<thinking>       # 思考过程（Claude 原生支持）
<scratchpad>     # 草稿区
<reasoning>      # 推理过程

# 通信类（Agent 场景）
<reminder>       # 温和提醒
<warning>        # 警告
<error>          # 错误
<hint>           # 提示

# 格式控制
<format>         # 格式说明
<json>           # JSON 输出
<code>           # 代码块
```

### 不同的Tag设计

```
# Anthropic 推荐的 tag 用法
<instructions>你的指令</instructions>
<context>背景信息</context>
<example>示例</example>
<document>文档内容</document>
<formatting>格式要求</formatting>


# OpenAI 更倾向于 markdown 风格
### Instructions
你的指令

### Context
背景信息

---
或者用 """ 和 ``` 包裹内容
"""
```

### 最佳实践

```
# 1. 保持一致性 - 整个项目用同一套 tag
# ❌ 混用
<instructions>...</instructions>
<task>...</task>  # 同一含义用不同 tag

# ✅ 一致
<instructions>...</instructions>
<instructions>...</instructions>

# 2. 语义清晰 - tag 名称自解释
# ❌ 模糊
<data1>...</data1>
<stuff>...</stuff>

# ✅ 清晰
<user_query>...</user_query>
<search_results>...</search_results>

# 3. 在 System Prompt 中定义你的 tags（可选但推荐）
SYSTEM = """
本对话中可能包含以下标记：
- <reminder>: 温和提醒，建议在合适时机处理
- <urgent>: 紧急事项，需立即处理
- <context>: 额外上下文信息，供参考
"""

# 4. 嵌套时保持层次清晰
<documents>
  <document index="1">
    <source>来源</source>
    <content>内容</content>
  </document>
</documents>
```

## Plan VS Act

- 重要
  - 区分于老的ReAct/Langchain/AutoGPT
  - TODO 系统让你"看到"模型的规划，但不能完全控制执行粒度。模型的自主判断有时会绕过你预期的步骤。

1. System prompt 没有强制分步执行对应一次文件操作,没有约束必须一个任务对应一次文件操作
2. 对模型来说合并更高效：三个改动本质上是对同一个文件的修改，分三次写入反而低效

```
1. read_file → TODO #1 completed
2. 尝试将 #2 #3 #4 同时设为 in_progress → 报错
3. 只将 #2 设为 in_progress
4. write_file → 一次性写入所有改动（type hints + docstrings + main guard）
5. bash 验证
6. 一次性将 #2 #3 #4 都标记为 completed
```

```
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use the todo tool to plan multi-step tasks. 
Mark in_progress before starting each task, completed when done.
IMPORTANT: Complete tasks one at a time. Each task should correspond to 
a separate tool call. Do not combine multiple pending tasks into one action.
Prefer tools over prose."""
```

## 资源

- [prompt-engineering/use-xml-tags](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)