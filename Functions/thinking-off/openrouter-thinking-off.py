"""
title: OpenRouter Disable Thinking
author: byfebian
version: 0.0.1
description: Explicitly disable reasoning/thinking for OpenRouter models.
             Use this to force models that think by default (DeepSeek R1,
             Claude thinking variants, Gemini thinking) to skip reasoning.
             Sends reasoning.effort = "none" to the OpenRouter API.
references:
  - https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0,
            description=(
                "Filter execution order. Lower values run first. "
                "If multiple Think filters are enabled at once, "
                "the highest priority (largest number) wins because "
                "it overwrites the reasoning parameter last."
            ),
        )
        show_status: bool = Field(default=True, description="Show thinking status notification in chat")

    def __init__(self):
        self.valves = self.Valves()

        # ------------------------------------------------------------------
        # toggle = True creates a clickable ON/OFF button in the chat UI.
        # ------------------------------------------------------------------
        self.toggle = True

        # ------------------------------------------------------------------
        # Icon: a circle with a line through it (universal "off" symbol).
        # ------------------------------------------------------------------
        self.icon = (
            "data:image/svg+xml;utf8,"
            "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' "
            "viewBox='0 0 24 24' fill='none' stroke='currentColor' "
            "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<line x1='4.93' y1='4.93' x2='19.07' y2='19.07'/>"
            "</svg>"
        )

    async def inlet(
        self,
        body: dict,
        __event_emitter__=None,
        __user__: Optional[dict] = None,
    ) -> dict:

        # Send effort "none" to explicitly suppress thinking.
        # This overrides the model's default behavior.
        body["reasoning"] = {
            "effort": "none",
        }

        if self.valves.show_status and __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Reasoning: off",
                        "done": True,
                        "hidden": False,
                    },
                }
            )

        return body
