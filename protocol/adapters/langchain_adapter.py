from protocol.schemas.message import BaseMessage


class LangChainAdapter:

    def to_protocol(self, tool_call: dict) -> BaseMessage:
        return BaseMessage(
            sender="langchain_agent",
            receiver=tool_call.get("target", "unknown"),
            type="REQUEST",
            action=tool_call["name"],
            payload=tool_call["args"]
        )

    def from_protocol(self, message: BaseMessage):
        return message.payload