# Agent Loop

## loop

True 循环直到 stop_reason != "tool_use"

## message

- system: 设定 AI 行为规则
- user: 人类输入 + tool_result（外部世界响应）
- assistant: 模型回复 + tool_use 请求
- message: user/assistant 必须相互迭代

## Pydantic

- Pydantic: Anthropic SDK 返回对象的序列化处理
- response.content里面包含Pydantic对象
  - model_dump() / model_dump_json()
  - 递归转换 to_serializable()

## thinking

- Extended Thinking: 通过 thinking 参数获取 LLM 推理过程
