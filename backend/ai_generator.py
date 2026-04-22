import json
from typing import Any, Dict, List, Optional

from zai import ZhipuAiClient


class AIGenerator:
    """Handles Zhipu/Z.ai GLM responses for course-material questions."""

    SYSTEM_PROMPT = """You are an AI assistant specialized in course materials and educational content with access to a comprehensive search tool for course information.

Search Tool Usage:
- Use the search tool only for questions about specific course content or detailed educational materials.
- Use at most one search per query.
- Synthesize search results into accurate, fact-based responses.
- If search yields no results, state this clearly without offering alternatives.

Response Protocol:
- General knowledge questions: answer using existing knowledge without searching.
- Course-specific questions: search first, then answer.
- No meta-commentary: provide direct answers only; do not describe your search process.

All responses must be brief, educational, clear, and example-supported when examples help.
Provide only the direct answer to what was asked.
"""

    def __init__(self, api_key: str, model: str):
        self.client = ZhipuAiClient(api_key=api_key) if api_key else None
        self.model = model
        self.base_params = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 800,
        }

    def generate_response(
        self,
        query: str,
        conversation_history: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_manager=None,
    ) -> str:
        """Generate a response, optionally allowing one GLM function call."""

        if not self.client:
            raise ValueError("ZAI_API_KEY is not configured")

        system_content = (
            f"{self.SYSTEM_PROMPT}\n\nPrevious conversation:\n{conversation_history}"
            if conversation_history
            else self.SYSTEM_PROMPT
        )
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": query},
        ]

        request_params = {**self.base_params, "messages": messages}
        if tools:
            request_params["tools"] = tools
            request_params["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**request_params)
        message = response.choices[0].message
        tool_calls = self._get_tool_calls(message)

        if tool_calls and tool_manager:
            return self._handle_tool_execution(messages, message, tool_calls, tool_manager)

        return self._get_attr(message, "content", "") or ""

    def _handle_tool_execution(
        self,
        messages: List[Dict[str, Any]],
        assistant_message: Any,
        tool_calls: List[Any],
        tool_manager,
    ) -> str:
        """Execute requested function calls and ask GLM for a final answer."""

        messages = [*messages, self._message_to_dict(assistant_message)]

        for tool_call in tool_calls:
            function = self._get_attr(tool_call, "function")
            name = self._get_attr(function, "name")
            arguments = self._parse_arguments(self._get_attr(function, "arguments", "{}"))
            tool_result = tool_manager.execute_tool(name, **arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": self._get_attr(tool_call, "id"),
                    "name": name,
                    "content": tool_result,
                }
            )

        final_response = self.client.chat.completions.create(
            **self.base_params,
            messages=messages,
        )
        return self._get_attr(final_response.choices[0].message, "content", "") or ""

    def _get_tool_calls(self, message: Any) -> List[Any]:
        return list(self._get_attr(message, "tool_calls", []) or [])

    def _message_to_dict(self, message: Any) -> Dict[str, Any]:
        if isinstance(message, dict):
            return message

        result = {
            "role": self._get_attr(message, "role", "assistant"),
            "content": self._get_attr(message, "content", "") or "",
        }
        tool_calls = self._get_tool_calls(message)
        if tool_calls:
            result["tool_calls"] = [self._tool_call_to_dict(tool_call) for tool_call in tool_calls]
        return result

    def _tool_call_to_dict(self, tool_call: Any) -> Dict[str, Any]:
        function = self._get_attr(tool_call, "function")
        return {
            "id": self._get_attr(tool_call, "id"),
            "type": self._get_attr(tool_call, "type", "function"),
            "function": {
                "name": self._get_attr(function, "name"),
                "arguments": self._get_attr(function, "arguments", "{}"),
            },
        }

    def _parse_arguments(self, raw_arguments: str) -> Dict[str, Any]:
        try:
            return json.loads(raw_arguments or "{}")
        except json.JSONDecodeError:
            return {}

    def _get_attr(self, value: Any, attr: str, default: Any = None) -> Any:
        if isinstance(value, dict):
            return value.get(attr, default)
        return getattr(value, attr, default)
