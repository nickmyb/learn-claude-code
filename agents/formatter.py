import json


def to_serializable(obj):
    """递归将 Anthropic SDK 对象转为可序列化的 dict"""
    if hasattr(obj, 'model_dump'):  # Pydantic 对象
        return obj.model_dump()
    elif isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    return obj


def print_messages(messages):
    """美化打印 messages"""
    serializable = to_serializable(messages)
    print(json.dumps(serializable, indent=2, ensure_ascii=False))


from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
import json

console = Console()


def print_messages_rich(messages):
    """Rich库 美化打印 messages"""
    serializable = to_serializable(messages)  # 用上面的函数

    for i, msg in enumerate(serializable):
        role = msg['role']
        content = msg['content']

        # 根据 role 选择颜色
        color = {"user": "blue", "assistant": "green"}.get(role, "white")

        # 格式化 content
        if isinstance(content, list):
            content_str = json.dumps(content, indent=2, ensure_ascii=False)
        else:
            content_str = str(content)

        console.print(Panel(
            Syntax(content_str, "json", theme="monokai", word_wrap=True),
            title=f"[{color}]{role}[/{color}]",
            border_style=color
        ))


def debug_messages(messages):
    """简洁的调试输出"""
    for i, msg in enumerate(messages):
        role = msg['role']
        content = msg['content']

        print(f"\n{'=' * 60}")
        print(f"[{i}] {role.upper()}")
        print('=' * 60)

        if isinstance(content, str):
            print(content[:200] + "..." if len(content) > 200 else content)
        elif isinstance(content, list):
            for block in content:
                if hasattr(block, 'type'):
                    if block.type == 'tool_use':
                        print(f"  📤 TOOL_USE: {block.name}")
                        print(f"     input: {block.input}")
                    elif block.type == 'text':
                        text = block.text[:150] + "..." if len(block.text) > 150 else block.text
                        print(f"  💬 TEXT: {text}")
                elif isinstance(block, dict):
                    if block.get('type') == 'tool_result':
                        print(f"  📥 TOOL_RESULT: {block.get('content', '')[:100]}...")


def debug_response_messages(response, messages):
    print()
    print()

    print("response start" + "*"*50)
    print(response)
    print("response end" + "*"*50)

    print()
    print()

    print("="*50)
    print_messages(messages)
    print("="*50)

    print()
    print()
