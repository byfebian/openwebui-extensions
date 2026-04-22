"""
title: ZDR: Private
author: byfebian
version: 0.0.1
description: Toggle Zero Data Retention (ZDR) for OpenRouter requests.
             When enabled, your request will ONLY be routed to providers
             that do not store your prompts. If no ZDR-compliant provider
             is available for the selected model, the request will fail
             rather than violating the policy. Use this for sensitive
             conversations where you want maximum privacy.
references:
  - https://openrouter.ai/docs/guides/features/zdr
  - https://openrouter.ai/docs/features/provider-routing
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0,
            description="Filter execution order. Lower values run first.",
        )

    def __init__(self):
        self.valves = self.Valves()

        # ------------------------------------------------------------------
        # toggle = True creates a clickable ON/OFF button in the chat UI.
        # ------------------------------------------------------------------
        self.toggle = True

        # ------------------------------------------------------------------
        # Icon: a shield (universal "protection/privacy" symbol).
        # ------------------------------------------------------------------
        self.icon = (
            "data:image/svg+xml;utf8,"
            "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' "
            "viewBox='0 0 24 24' fill='none' stroke='currentColor' "
            "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
            "<path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/>"
            "</svg>"
        )

    async def inlet(
        self,
        body: dict,
        __event_emitter__=None,
        __user__: Optional[dict] = None,
    ) -> dict:

        # ------------------------------------------------------------------
        # Inject the provider.zdr parameter into the request body.
        # OpenRouter reads this and only routes to ZDR-compliant endpoints.
        #
        # If the body already has a "provider" dict (e.g. from another
        # filter setting provider preferences), we merge into it rather
        # than overwriting.
        #
        # Docs: https://openrouter.ai/docs/guides/features/zdr
        # ------------------------------------------------------------------
        if "provider" not in body:
            body["provider"] = {}

        body["provider"]["zdr"] = True

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "ZDR enabled — private mode",
                        "done": True,
                        "hidden": False,
                    },
                }
            )

        return body
