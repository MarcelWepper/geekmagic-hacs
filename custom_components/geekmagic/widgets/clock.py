"""Clock widget for GeekMagic displays."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from ..const import COLOR_GRAY, COLOR_WHITE
from .base import Widget, WidgetConfig
from .components import Color, Column, Component, FillText, Row, Text

if TYPE_CHECKING:
    from ..render_context import RenderContext
    from .state import WidgetState


def ClockDisplay(
    time_str: str,
    date_str: str | None = None,
    ampm: str | None = None,
    label: str | None = None,
    time_color: Color = COLOR_WHITE,
    date_color: Color = COLOR_GRAY,
    label_color: Color = COLOR_GRAY,
) -> Component:
    """Create clock display using primitive components.

    Time uses FillText to fill available space, date scales proportionally.
    """
    children: list[Component] = []

    # Add label at top if provided
    if label:
        children.append(Text(label.upper(), font="tertiary", color=label_color))

    # Time display - fills available space
    if ampm:
        # 12-hour format: time + AM/PM in a row
        children.append(
            Row(
                children=[
                    FillText(time_str, hierarchy="primary", color=time_color),
                    Text(ampm, font="tertiary", color=COLOR_GRAY),
                ],
                gap=4,
                align="end",
                justify="center",
            )
        )
    else:
        # 24-hour format: just time
        children.append(FillText(time_str, hierarchy="primary", color=time_color))

    # Add date below time
    if date_str:
        children.append(FillText(date_str, hierarchy="secondary", color=date_color))

    return Column(
        children=children,
        gap=4,
        align="center",
        justify="center",
        padding=4,
    )


class ClockWidget(Widget):
    """Widget that displays current time and date."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the clock widget."""
        super().__init__(config)
        self.show_date = config.options.get("show_date", True)
        self.show_seconds = config.options.get("show_seconds", False)
        self.time_format = config.options.get("time_format", "24h")
        self.timezone = config.options.get("timezone")

    def get_entities(self) -> list[str]:
        """Clock widget doesn't depend on entities."""
        return []

    def render(self, ctx: RenderContext, state: WidgetState) -> Component:
        """Render the clock widget as a Component tree.

        Args:
            ctx: RenderContext for drawing
            state: Widget state with current time
        """
        # Get time from state (coordinator handles timezone)
        now = state.now or datetime.now(tz=UTC)

        # Format time
        if self.show_seconds:
            if self.time_format == "12h":
                time_str = now.strftime("%I:%M:%S")
                ampm = now.strftime("%p")
            else:
                time_str = now.strftime("%H:%M:%S")
                ampm = None
        elif self.time_format == "12h":
            time_str = now.strftime("%I:%M")
            ampm = now.strftime("%p")
        else:
            time_str = now.strftime("%H:%M")
            ampm = None

        date_str = now.strftime("%a, %b %d") if self.show_date else None
        color = self.config.color or COLOR_WHITE

        return ClockDisplay(
            time_str=time_str,
            date_str=date_str,
            ampm=ampm,
            label=self.config.label,
            time_color=color,
        )
