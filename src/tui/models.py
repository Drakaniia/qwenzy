"""Data models shared across the Textual interface layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolkitAction:
    """A structured command the TUI can render and execute."""

    id: str
    section: str
    title: str
    target: str
    description: str
    action_type: str
    risk: str = "Low"
    status: str = "Ready"
    requires_confirmation: bool = False
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolkitSection:
    """A group of related toolkit actions."""

    id: str
    title: str
    description: str
    actions: list[ToolkitAction]


@dataclass(frozen=True)
class ExecutionResult:
    """Result returned after running a toolkit action."""

    action_id: str
    title: str
    success: bool
    message: str
    details: str = ""
