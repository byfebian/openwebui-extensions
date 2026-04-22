"""
title: OpenRouter Reasoning Toggle
author: byfebian
version: 1.0.0
license: MIT
description: Toggle AI model thinking/reasoning for OpenRouter models with configurable effort levels
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Filter:
    # Configuration options for the filter (admin-configurable)
    class Valves(BaseModel):
        default_effort: str = Field(
            default="medium",
            description="Default reasoning effort level when toggle is ON",
            json_schema_extra={
                "enum": ["xhigh", "high", "medium", "low", "minimal", "none"]
            },
        )
        default_max_tokens: Optional[int] = Field(
            default=None,
            description="Maximum tokens for reasoning (leave empty to use effort-based allocation)",
        )
        exclude_reasoning: bool = Field(
            default=False,
            description="Exclude reasoning tokens from response (model thinks but doesn't show reasoning)",
        )
        debug_mode: bool = Field(
            default=False, description="Enable debug logging to console"
        )
        show_status: bool = Field(default=True, description="Show thinking status notification in chat")

    def __init__(self):
        self.valves = self.Valves()
        # This creates a toggle switch in the OpenWebUI chat interface
        self.toggle = True
        # Optional: Add an icon for the toggle (use a URL or data URI)
        # self.icon = "https://example.com/brain-icon.svg"

    def _log(self, message: str):
        """Helper for debug logging"""
        if self.valves.debug_mode:
            print(f"[OpenRouter Reasoning Toggle] {message}")

    async def inlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
        __event_emitter__=None,
        __model__: Optional[dict] = None,
    ) -> dict:
        """
        Modify the request body before sending to OpenRouter.
        Adds reasoning parameters when the toggle is enabled.
        """
        # Check if this filter is enabled via the toggle switch
        # The toggle state is stored in the filter instance
        if not getattr(self, "toggle", True):
            self._log("Toggle is OFF - skipping reasoning injection")
            return body

        # Get the model being used
        model = body.get("model", "unknown")
        self._log(f"Processing request for model: {model}")

        # Build the reasoning configuration
        reasoning_config: Dict[str, Any] = {"enabled": True}

        # Add effort level (maps to OpenRouter's reasoning.effort)
        if self.valves.default_effort:
            reasoning_config["effort"] = self.valves.default_effort

        # Add max_tokens if specified (for Anthropic-style token allocation)
        if self.valves.default_max_tokens:
            reasoning_config["max_tokens"] = self.valves.default_max_tokens

        # Add exclude flag if enabled
        if self.valves.exclude_reasoning:
            reasoning_config["exclude"] = True

        # Inject the reasoning parameter into the request body
        # OpenWebUI forwards unknown fields to the external API
        body["reasoning"] = reasoning_config

        self._log(f"Injected reasoning config: {reasoning_config}")

        # Send status notification to UI if event emitter is available
        if self.valves.show_status and __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Reasoning: {self.valves.default_effort}",
                        "done": True,
                        "hidden": False,
                    },
                }
            )

        return body

    async def stream(self, event: dict) -> dict:
        """
        Optional: Process streaming chunks to extract/display reasoning.
        This runs on each chunk during streaming responses.
        """
        # You can modify streaming events here if needed
        # For example, to highlight reasoning content differently
        return event

    async def outlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__=None,
    ) -> dict:
        """
        Optional: Process the final response.
        Can be used to format or log reasoning content.
        """
        # The reasoning content will be in the response message's "reasoning" field
        # or in "reasoning_details" array depending on the model
        return body
