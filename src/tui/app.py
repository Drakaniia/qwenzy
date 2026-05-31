"""Modern Textual application for Windows Automation Toolkit."""

from __future__ import annotations

import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    LoadingIndicator,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from src.tui.services import ExecutionResult, ToolkitAction, ToolkitActionService, ToolkitSection


class ConfirmActionScreen(ModalScreen[bool]):
    """Confirm execution of a potentially destructive or networked action."""

    def __init__(self, action: ToolkitAction) -> None:
        super().__init__()
        self.action = action

    def compose(self) -> ComposeResult:
        with Container(id="confirm-dialog"):
            yield Static("Confirm action", id="confirm-title")
            yield Static(self.action.title, id="confirm-action")
            yield Static(self.action.description, id="confirm-description")
            yield Static(f"Target: {self.action.target}", id="confirm-target")
            with Horizontal(id="confirm-buttons"):
                yield Button("Cancel", id="confirm-cancel", variant="default")
                yield Button("Run", id="confirm-run", variant="error")

    def on_mount(self) -> None:
        self.query_one("#confirm-cancel", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm-run":
            self.dismiss(True)
        else:
            self.dismiss(False)


class WindowsToolkitApp(App[None]):
    """Textual control center for the Windows Automation Toolkit."""

    CSS_PATH = "toolkit.tcss"
    TITLE = "Windows Automation Toolkit"
    SUB_TITLE = "Windows 10/11 Optimization Suite"

    BINDINGS = [
        ("f", "focus_search", "Search"),
        ("r", "run_selected", "Run"),
        ("ctrl+r", "refresh", "Refresh"),
        ("d", "toggle_dark", "Theme"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, service: ToolkitActionService | None = None) -> None:
        super().__init__()
        self.service = service or ToolkitActionService()
        self.sections: list[ToolkitSection] = self.service.get_sections()
        self.active_section_id = self.sections[0].id if self.sections else ""
        self.selected_action_id = ""
        self._busy = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="app-shell"):
            with Container(id="hero"):
                yield Static("Windows Automation Toolkit", id="hero-title")
                yield Static("A keyboard-first control center for Windows cleanup, optimization, power, and automation.", id="hero-subtitle")
            with Horizontal(id="workspace"):
                with Vertical(id="status-panel"):
                    yield Static("System", classes="panel-title")
                    yield Static("", id="status-admin", classes="status-card")
                    yield Static("", id="status-winget", classes="status-card")
                    yield Static("", id="status-ahk", classes="status-card")
                    yield Static("Use Tab or arrow keys to move through controls. Press r to run the selected row.", id="keyboard-hint")
                with Vertical(id="main-panel"):
                    with Horizontal(id="toolbar"):
                        yield Input(placeholder="Filter actions by name, command, risk, or status", id="search")
                        yield Button("Run", id="run-action", variant="primary")
                        yield Button("Refresh", id="refresh-actions")
                    with TabbedContent(id="sections"):
                        for section in self.sections:
                            with TabPane(section.title, id=section.id):
                                yield Static(section.description, classes="section-summary")
                                yield DataTable(id=f"table-{section.id}", classes="action-table")
                    yield LoadingIndicator(id="loading")
                    yield RichLog(id="activity-log", wrap=True, highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self._set_busy(False)
        self._refresh_status_cards()
        self._populate_tables(self.sections)
        self.query_one("#search", Input).focus()
        self._log("Ready. Select an action row, then press r or use the Run button.")

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search":
            self._populate_tables(self.service.filter_actions(event.value))

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self.selected_action_id = str(event.row_key.value)

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.selected_action_id = str(event.row_key.value)
        await self._run_selected_action()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        if event.pane.id:
            self.active_section_id = event.pane.id
            self._select_first_row(event.pane.id)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-action":
            await self._run_selected_action()
        elif event.button.id == "refresh-actions":
            self.action_refresh()

    def action_focus_search(self) -> None:
        self.query_one("#search", Input).focus()

    async def action_run_selected(self) -> None:
        await self._run_selected_action()

    def action_refresh(self) -> None:
        self.sections = self.service.get_sections()
        self._refresh_status_cards()
        self._populate_tables(self.service.filter_actions(self.query_one("#search", Input).value))
        self._log("Catalog and status refreshed.")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def _populate_tables(self, sections: list[ToolkitSection]) -> None:
        first_action_id = ""

        for section in sections:
            table = self.query_one(f"#table-{section.id}", DataTable)
            table.clear(columns=True)
            table.cursor_type = "row"
            table.zebra_stripes = True
            table.add_column("Action", key="action", width=30)
            table.add_column("Target", key="target", width=34)
            table.add_column("Risk", key="risk", width=9)
            table.add_column("Status", key="status", width=14)

            for action in section.actions:
                if not first_action_id:
                    first_action_id = action.id
                table.add_row(
                    action.title,
                    action.target,
                    action.risk,
                    action.status,
                    key=action.id,
                )

        if first_action_id:
            self.selected_action_id = first_action_id
            self._select_first_row(self.active_section_id)

    def _select_first_row(self, section_id: str) -> None:
        try:
            table = self.query_one(f"#table-{section_id}", DataTable)
        except Exception:
            return
        if table.row_count:
            table.move_cursor(row=0, column=0, animate=False)
            row_key = table.ordered_rows[0].key
            self.selected_action_id = str(row_key.value)

    async def _run_selected_action(self) -> None:
        if self._busy:
            return
        if not self.selected_action_id:
            self._log("No action is selected.")
            return

        action = self.service.find_action(self.selected_action_id)
        if action.requires_confirmation:
            self._confirm_action(action)
            return

        await self._execute_action(action)

    def _confirm_action(self, action: ToolkitAction) -> None:
        async def handle_confirmation(confirmed: bool | None) -> None:
            if not confirmed:
                self._log(f"Cancelled: {action.title}")
                return
            await self._execute_action(action)

        self.push_screen(ConfirmActionScreen(action), callback=handle_confirmation)

    async def _execute_action(self, action: ToolkitAction) -> None:
        if self._busy:
            return
        self._set_busy(True)
        self._log(f"Running: {action.title}")
        try:
            result = await asyncio.to_thread(self.service.run_action, action.id)
            self._handle_result(result)
        finally:
            self._set_busy(False)

    def _handle_result(self, result: ExecutionResult) -> None:
        status = "OK" if result.success else "FAILED"
        self._log(f"[b]{status}[/b] {result.message}")
        if result.details:
            self._log(result.details)
        self.action_refresh()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        loading = self.query_one("#loading", LoadingIndicator)
        run_button = self.query_one("#run-action", Button)
        refresh_button = self.query_one("#refresh-actions", Button)

        loading.set_class(not busy, "hidden")
        run_button.disabled = busy
        refresh_button.disabled = busy

    def _refresh_status_cards(self) -> None:
        overview = self.service.get_overview()
        card_ids = ["#status-admin", "#status-winget", "#status-ahk"]
        for selector, (label, value, detail) in zip(card_ids, overview):
            self.query_one(selector, Static).update(f"[b]{label}[/b]\n{value}\n{detail}")

    def _log(self, message: str) -> None:
        self.query_one("#activity-log", RichLog).write(message)
