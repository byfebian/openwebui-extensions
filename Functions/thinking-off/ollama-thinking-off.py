"""
title: Disable Ollama Thinking
author: byfebian
version: 0.0.1
icon_url: https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/26a1.svg
"""

from pydantic import BaseModel, Field
from typing import Optional
import traceback


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Filter execution order (0 = runs first)"
        )
        verbose_logging: bool = Field(default=False, description="Enable debug logging")
        show_status: bool = Field(default=True, description="Show thinking status notification in chat")

    def __init__(self):
        self.valves = self.Valves()
        self.toggle = True
        self.icon = (
            "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/26a1.svg"
        )

    def _is_gpt_oss(self, model_name: str) -> bool:
        return "gpt-oss" in model_name.lower()

    async def inlet(
        self, body: dict, __event_emitter__=None, __model__: Optional[dict] = None
    ) -> dict:
        try:
            # Resolve base model name (handles workspace/custom model wrappers)
            model_name = body.get("model", "unknown")
            if __model__ and "info" in __model__:
                base = __model__["info"].get("base_model_id")
                if base:
                    model_name = base

            # -----------------------------------------------------------------
            # Determine think value based on model type:
            # - GPT-OSS: Only accepts "low", "medium", or "high".
            #   "false" is ignored by GPT-OSS, so "low" is the minimum.
            # - All other thinking models: Accept boolean true/false.
            # -----------------------------------------------------------------
            if self._is_gpt_oss(model_name):
                think_value = "low"
                message = "Reasoning: low"
            else:
                think_value = False
                message = "Reasoning: off"

            # -----------------------------------------------------------------
            # Set think parameter in BOTH locations for maximum compatibility:
            #
            # 1. body["think"] — Top-level parameter per Ollama native API spec
            #    (/api/chat). This is the correct placement for direct Ollama
            #    API calls, but OpenWebUI may not forward it when using the
            #    OpenAI-compatible endpoint.
            #
            # 2. body["options"]["think"] — Inside the options dict, which
            #    OpenWebUI maps directly to Ollama's options parameter and
            #    forwards reliably through the OpenAI-compatible endpoint.
            #    This is the path that actually works in practice with
            #    OpenWebUI → Ollama Cloud Pro API.
            #
            # Setting both ensures it works regardless of how the request
            # is routed. Ollama will read the value from whichever location
            # it checks first.
            # -----------------------------------------------------------------
            body["think"] = think_value

            if "options" not in body:
                body["options"] = {}
            body["options"]["think"] = think_value

            if self.valves.verbose_logging:
                print(f"[Disable Thinking] Model: {model_name}, think={think_value}")

            if self.valves.show_status and __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": message,
                            "done": True,
                            "hidden": False,
                        },
                    }
                )
        except Exception as e:
            print(f"[Disable Thinking] Error in inlet: {e}")
            traceback.print_exc()

        # Always return body, even on error
        return body

    async def stream(self, event: dict) -> dict:
        # Pass through unchanged
        return event

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Pass through unchanged - don't modify response
        return body
