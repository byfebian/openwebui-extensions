"""
title: Disable Thinking Toggle
author: ticoneva
version: 1.0.0
license: MIT
description: Toggle to disable thinking in Qwen3 and GLM models.
modified: byfebian (add show_status valve option and reasoning status notification)
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:

    class Valves(BaseModel):
        priority: int = Field(default=0)
        show_status: bool = Field(default=True, description="Show thinking status notification in chat")

    def __init__(self):
        self.valves = self.Valves()
        self.toggle = True
        self.icon = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMSIgdmlld0JveD0iMCAwIDI1LjMgMjUuMyI+CiAgPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDMwLjIuMSwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDIuMS4xIEJ1aWxkIDEpICAtLT4KICA8ZGVmcz4KICAgIDxzdHlsZT4KICAgICAgLnN0MCwgLnN0MSwgLnN0MiB7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgfQoKICAgICAgLnN0MSB7CiAgICAgICAgc3Ryb2tlLW1pdGVybGltaXQ6IDEwOwogICAgICB9CgogICAgICAuc3QxLCAuc3QyIHsKICAgICAgICBzdHJva2U6ICMwMDA7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAycHg7CiAgICAgIH0KCiAgICAgIC5zdDIgewogICAgICAgIHN0cm9rZS1saW5lY2FwOiByb3VuZDsKICAgICAgICBzdHJva2UtbGluZWpvaW46IHJvdW5kOwogICAgICB9CiAgICA8L3N0eWxlPgogIDwvZGVmcz4KICA8ZyBpZD0iTGF5ZXJfMSI+CiAgICA8Zz4KICAgICAgPHBhdGggY2xhc3M9InN0MCIgZD0iTTIuNzUsMi43NWgxOS44djE5LjhIMi43NVYyLjc1WiIvPgogICAgICA8cGF0aCBjbGFzcz0ic3QyIiBkPSJNMTUuNTQsMTMuNDhjLTEuNTksMC0yLjg5LDEuMjktMi44OSwyLjg5di44MmMwLDEuNTksMS4yOSwyLjg5LDIuODksMi44OXMyLjg5LTEuMjksMi44OS0yLjg5di0xLjQ4Ii8+CiAgICAgIDxwYXRoIGNsYXNzPSJzdDIiIGQ9Ik05Ljc2LDEzLjQ4YzEuNTksMCwyLjg5LDEuMjksMi44OSwyLjg5di44MmMwLDEuNTktMS4yOSwyLjg5LTIuODksMi44OXMtMi44OS0xLjI5LTIuODktMi44OXYtMS40OCIvPgogICAgICA8cGF0aCBjbGFzcz0ic3QyIiBkPSJNMTcuMTksMTUuOTVjMS41OSwwLDIuODktMS4yOSwyLjg5LTIuODlzLTEuMjktMi44OS0yLjg5LTIuODloLS40MSIvPgogICAgICA8cGF0aCBjbGFzcz0ic3QyIiBkPSJNMTguNDMsMTAuNDJ2LTIuMzFjMC0xLjU5LTEuMjktMi44OS0yLjg5LTIuODlzLTIuODksMS4yOS0yLjg5LDIuODkiLz4KICAgICAgPHBhdGggY2xhc3M9InN0MiIgZD0iTTguMTEsMTUuOTVjLTEuNTksMC0yLjg5LTEuMjktMi44OS0yLjg5czEuMjktMi44OSwyLjg5LTIuODloLjQxIi8+CiAgICAgIDxwYXRoIGNsYXNzPSJzdDIiIGQ9Ik02Ljg4LDEwLjQydi0yLjMxYzAtMS41OSwxLjI5LTIuODksMi44OS0yLjg5czIuODksMS4yOSwyLjg5LDIuODl2OC4yNSIvPgogICAgPC9nPgogIDwvZz4KICA8ZyBpZD0iTGF5ZXJfMiI+CiAgICA8ZWxsaXBzZSBjbGFzcz0ic3QxIiBjeD0iMTIuNjUiIGN5PSIxMi42NSIgcng9IjExLjEiIHJ5PSIxMS4zOSIvPgogICAgPGxpbmUgY2xhc3M9InN0MSIgeDE9IjQuNyIgeTE9IjQuNyIgeDI9IjIwLjYiIHkyPSIyMC42Ii8+CiAgPC9nPgo8L3N2Zz4="

    async def inlet(self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None) -> dict:
        body["chat_template_kwargs"] = {"enable_thinking": False}

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
