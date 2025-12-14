"""Text widget for GeekMagic displays."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..const import COLOR_GRAY, COLOR_WHITE
from .base import Widget, WidgetConfig
from .components import Column, Component, Text

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from ..render_context import RenderContext


# Map widget align to component align
ALIGN_MAP: dict[str, Literal["start", "center", "end"]] = {
    "left": "start",
    "center": "center",
    "right": "end",
}


class TextWidget(Widget):
    """Widget that displays static or dynamic text."""

    def __init__(self, config: WidgetConfig) -> None:
        """Initialize the text widget."""
        super().__init__(config)
        self.text = config.options.get("text", "")
        self.size = config.options.get("size", "regular")  # small, regular, large, xlarge
        self.align = config.options.get("align", "center")  # left, center, right
        # Entity ID for dynamic text (from options, takes precedence over widget entity_id)
        self.dynamic_entity_id = config.options.get("entity_id")

    def render(
        self,
        ctx: RenderContext,
        hass: HomeAssistant | None = None,
    ) -> Component:
        """Render the text widget.

        Args:
            ctx: RenderContext for drawing
            hass: Home Assistant instance

        Returns:
            Component tree for rendering
        """
        text = self._get_text(hass)
        color = self.config.color or COLOR_WHITE
        align = ALIGN_MAP.get(self.align, "center")

        children: list[Component] = []

        # Add label at top if provided
        if self.config.label:
            children.append(Text(self.config.label.upper(), font="small", color=COLOR_GRAY))

        # Main text
        children.append(Text(text, font=self.size, color=color, align=align))

        return Column(
            children=children,
            align="center",
            justify="center",
            gap=4,
        )

    def _get_text(self, hass: HomeAssistant | None) -> str:
        """Get the text to display.

        If entity_id is set (from options or widget config), returns the entity state.
        Otherwise returns the configured text.
        """
        # Check dynamic entity_id from options first, then widget config entity_id
        entity_id = self.dynamic_entity_id or self.config.entity_id
        if entity_id and hass:
            state = hass.states.get(entity_id)
            if state:
                return state.state

        return self.text
