"""Tests for flexbox layout helpers."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from custom_components.geekmagic.widgets.flex_layout import (
    LayoutBox,
    Priority,
    create_horizontal_layout,
    create_vertical_layout,
    layout_bar_gauge,
    layout_centered_stack,
    layout_icon_value_label,
)


class TestLayoutBox:
    """Tests for LayoutBox dataclass."""

    def test_center(self) -> None:
        """Test center property calculation."""
        box = LayoutBox(x=10, y=20, width=100, height=50)
        assert box.center == (60, 45)  # (10 + 50, 20 + 25)

    def test_right(self) -> None:
        """Test right edge calculation."""
        box = LayoutBox(x=10, y=20, width=100, height=50)
        assert box.right == 110  # 10 + 100

    def test_bottom(self) -> None:
        """Test bottom edge calculation."""
        box = LayoutBox(x=10, y=20, width=100, height=50)
        assert box.bottom == 70  # 20 + 50


class TestPriority:
    """Tests for Priority enum."""

    def test_priority_ordering(self) -> None:
        """Test that priorities are ordered correctly."""
        assert Priority.CRITICAL < Priority.HIGH
        assert Priority.HIGH < Priority.MEDIUM
        assert Priority.MEDIUM < Priority.LOW


class TestCreateVerticalLayout:
    """Tests for create_vertical_layout function."""

    def test_single_element_fills_space(self) -> None:
        """Test that single flex element fills container."""
        boxes = create_vertical_layout(100, 200, {"content": None})

        assert "content" in boxes
        assert boxes["content"].width == 100
        assert boxes["content"].height == 200

    def test_fixed_height_elements(self) -> None:
        """Test layout with fixed height elements."""
        boxes = create_vertical_layout(100, 200, {"header": 30, "content": 50, "footer": 20})

        assert boxes["header"].height == 30
        assert boxes["content"].height == 50
        assert boxes["footer"].height == 20
        assert boxes["header"].y == 0
        assert boxes["content"].y == 30
        assert boxes["footer"].y == 80

    def test_mixed_fixed_and_flex(self) -> None:
        """Test layout with mix of fixed and flex elements."""
        boxes = create_vertical_layout(100, 200, {"header": 30, "content": None, "footer": 20})

        assert boxes["header"].height == 30
        assert boxes["content"].height == 150  # 200 - 30 - 20
        assert boxes["footer"].height == 20

    def test_all_elements_full_width(self) -> None:
        """Test that all elements span full width."""
        boxes = create_vertical_layout(100, 200, {"a": 50, "b": None})

        assert boxes["a"].width == 100
        assert boxes["b"].width == 100


class TestCreateHorizontalLayout:
    """Tests for create_horizontal_layout function."""

    def test_single_element_fills_space(self) -> None:
        """Test that single flex element fills container."""
        boxes = create_horizontal_layout(200, 100, {"content": None})

        assert "content" in boxes
        assert boxes["content"].width == 200
        assert boxes["content"].height == 100

    def test_fixed_width_elements(self) -> None:
        """Test layout with fixed width elements."""
        boxes = create_horizontal_layout(200, 100, {"left": 30, "center": 50, "right": 20})

        assert boxes["left"].width == 30
        assert boxes["center"].width == 50
        assert boxes["right"].width == 20

    def test_mixed_fixed_and_flex(self) -> None:
        """Test layout with mix of fixed and flex elements."""
        boxes = create_horizontal_layout(200, 100, {"icon": 30, "label": None, "value": 50})

        assert boxes["icon"].width == 30
        assert boxes["label"].width == 120  # 200 - 30 - 50
        assert boxes["value"].width == 50

    def test_all_elements_full_height(self) -> None:
        """Test that all elements span full height."""
        boxes = create_horizontal_layout(200, 100, {"a": 50, "b": None})

        assert boxes["a"].height == 100
        assert boxes["b"].height == 100


class TestLayoutBarGauge:
    """Tests for layout_bar_gauge function."""

    @pytest.fixture
    def mock_ctx(self) -> MagicMock:
        """Create a mock RenderContext."""
        ctx = MagicMock()
        ctx.width = 120
        ctx.height = 80
        ctx.get_font.return_value = MagicMock()
        ctx.get_text_size.return_value = (40, 16)
        return ctx

    def test_horizontal_layout_wide(self, mock_ctx: MagicMock) -> None:
        """Test that wide containers use horizontal layout."""
        mock_ctx.width = 120  # Above min_horizontal_width=90

        use_vertical, boxes = layout_bar_gauge(
            mock_ctx, value_text="50%", label_text="CPU", has_icon=True
        )

        assert use_vertical is False
        assert "value" in boxes
        assert "bar" in boxes
        assert "label" in boxes
        assert "icon" in boxes

    def test_vertical_layout_narrow(self, mock_ctx: MagicMock) -> None:
        """Test that narrow containers use vertical layout."""
        mock_ctx.width = 70  # Below min_horizontal_width=90

        use_vertical, boxes = layout_bar_gauge(
            mock_ctx, value_text="50%", label_text="CPU", has_icon=True
        )

        assert use_vertical is True
        assert "value" in boxes
        assert "bar" in boxes
        assert "label" in boxes
        # Icon is not included in vertical layout (by design)
        assert "icon" not in boxes

    def test_no_label(self, mock_ctx: MagicMock) -> None:
        """Test layout without label."""
        mock_ctx.width = 70

        use_vertical, boxes = layout_bar_gauge(
            mock_ctx, value_text="50%", label_text=None, has_icon=False
        )

        assert "value" in boxes
        assert "bar" in boxes
        assert "label" not in boxes

    def test_no_icon(self, mock_ctx: MagicMock) -> None:
        """Test layout without icon."""
        mock_ctx.width = 120

        use_vertical, boxes = layout_bar_gauge(
            mock_ctx, value_text="50%", label_text="CPU", has_icon=False
        )

        assert use_vertical is False
        assert "icon" not in boxes


class TestLayoutIconValueLabel:
    """Tests for layout_icon_value_label function."""

    @pytest.fixture
    def mock_ctx(self) -> MagicMock:
        """Create a mock RenderContext."""
        ctx = MagicMock()
        ctx.width = 100
        ctx.height = 80
        ctx.get_font.return_value = MagicMock()
        ctx.get_text_size.return_value = (40, 16)
        return ctx

    def test_horizontal_layout(self, mock_ctx: MagicMock) -> None:
        """Test horizontal layout for wide containers."""
        mock_ctx.width = 100  # Above min_horizontal_width=80

        use_vertical, boxes = layout_icon_value_label(
            mock_ctx, value_text="21°C", label_text="Temp", has_icon=True
        )

        assert use_vertical is False
        assert "icon" in boxes
        assert "value" in boxes
        assert "label" in boxes

    def test_vertical_layout(self, mock_ctx: MagicMock) -> None:
        """Test vertical layout for narrow containers."""
        mock_ctx.width = 60  # Below min_horizontal_width=80

        use_vertical, boxes = layout_icon_value_label(
            mock_ctx, value_text="21°C", label_text="Temp", has_icon=True
        )

        assert use_vertical is True
        assert "icon" in boxes
        assert "value" in boxes
        assert "label" in boxes


class TestLayoutCenteredStack:
    """Tests for layout_centered_stack function."""

    @pytest.fixture
    def mock_ctx(self) -> MagicMock:
        """Create a mock RenderContext."""
        ctx = MagicMock()
        ctx.width = 100
        ctx.height = 200
        return ctx

    def test_single_element_centered(self, mock_ctx: MagicMock) -> None:
        """Test that single element is centered."""
        boxes = layout_centered_stack(mock_ctx, [("content", 50)])

        assert boxes["content"].width == 100
        assert boxes["content"].height == 50
        assert boxes["content"].y == 75  # (200 - 50) // 2

    def test_multiple_elements_centered(self, mock_ctx: MagicMock) -> None:
        """Test that multiple elements are centered as a group."""
        boxes = layout_centered_stack(mock_ctx, [("a", 30), ("b", 40)], gap=10)

        # Total height = 30 + 10 + 40 = 80
        # Start y = (200 - 80) // 2 = 60
        assert boxes["a"].y == 60
        assert boxes["a"].height == 30
        assert boxes["b"].y == 100  # 60 + 30 + 10
        assert boxes["b"].height == 40

    def test_custom_gap(self, mock_ctx: MagicMock) -> None:
        """Test custom gap between elements."""
        boxes = layout_centered_stack(mock_ctx, [("a", 20), ("b", 20), ("c", 20)], gap=20)

        # Total height = 20 + 20 + 20 + 20 + 20 = 100 (3 elements, 2 gaps)
        # Start y = (200 - 100) // 2 = 50
        assert boxes["a"].y == 50
        assert boxes["b"].y == 90  # 50 + 20 + 20
        assert boxes["c"].y == 130  # 90 + 20 + 20
