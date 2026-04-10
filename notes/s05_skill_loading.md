# Skills

## 按需加载

- Load knowledge when you need it, not upfront
  - inject via tool_result, not the system prompt.
- Layer 1: skill names in system prompt (cheap). Layer 2: full body via tool_result (on demand).
  - Layer 1: `Compact Summaries`
    - All skills are summarized in the system prompt. Compact, always present.
  - Layer 2: `Full Injection`
    - The full skill instructions are injected as a tool_result, not into the system prompt.

## skill定义

- Each skill is a `directory` containing a `SKILL.md` with `YAML` frontmatter.

## The Philosophy of Agent Harness Engineering

- agent: 一个学会了如何行动的模型
  - agent就是LLM
  - Agency is learned, not programmed.(GOFAI是错误的历史)
  - **The model already knows how to be an agent. Your job is to build it a world worth acting in.**

## The Harness: What We Actually Build

- model is the agent
- code is the **harness** -- the environment that gives the agent the ability to perceive and act in a specific domain.

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions
```

### tools

- 原子化、可组合、描述清晰
- 从 3-5 个工具开始。只有当模型因为缺少工具而持续失败时，才增加新工具。

### knowledge

- = SKILL

### context

- 有限的context
- subagent减少噪音
- compact history上下文
- task分解任务

### permissions

- 权限
- 沙箱

### Task-Process Data

- harness 收集的训练数据可以训练更好的 agent

## 核心就是loop

- 循环以外都是harness engineering

```
LOOP:
  Model sees: conversation history + available tools
  Model decides: act or respond
  If act: tool executed, result added to context, loop continues
  If respond: answer returned, loop ends
```

## harness engineering原则

1. 信任模型
2. todo list + only one task in progress: 聚焦
3. progressive complexity - 需要时才增加
4. 转变做agent的思维

## the vehicle metaphor

- 同一个模型（同一个司机）可以驾驶不同的载具去不同的领域工作
  - 给它装上"代码 IDE"它就是 Claude Code
  - 给它装上"农场传感器"它就是农业 agent
- 这就是为什么学 harness 工程是有普遍价值的：你学的不是怎么造车，而是怎么造驾驶舱，而驾驶舱的设计原则是跨领域通用的。

## 什么时候微调

- 模型在这个领域的基础能力确实不够(没见过或者见得少)
- 加载SKILL的上下文大小有限制
- 已经有海量高质量的 trajectory 数据
  - 先有 harness 和 SKILL 跑起来，才有 trajectory 数据，最后是微调
- 需要改变模型的默认行为倾向(风格)
  - 风格问题 基本都能通过 system prompt + SKILL 解决

## agent-builder

- 现有版本只能生成最基础的agent,需要的功能要人为补充,提供了一个脚手架
- harness engineer应该是人而不是AI
- 可以去优化agent-builder,但不应该大规模修改,loop就是一切的起点

## 总结

- 专用 harness + 通用模型
- 思考前面的比喻
- 训练模型你是怎么一步步解决问题的而不是给他限制解决步骤
- harness engineer = backend engineer + pm
- The model is the agent. The code is the harness. Know which one you're building.
