#!/usr/bin/env python3
"""Generate sample renders showcasing GeekMagic display layouts and widgets.

Usage:
    uv run python scripts/generate_samples.py

Outputs PNG images to the samples/ directory.

Uses Cairo for high-quality anti-aliased rendering.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

# Add the custom_components to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from custom_components.geekmagic.const import (
    COLOR_BLUE,
    COLOR_DARK_GRAY,
    COLOR_GOLD,
    COLOR_GRAY,
    COLOR_LIME,
    COLOR_ORANGE,
    COLOR_PANEL,
    COLOR_PINK,
    COLOR_PURPLE,
    COLOR_RED,
    COLOR_TEAL,
    COLOR_WHITE,
    COLOR_YELLOW,
)
from custom_components.geekmagic.renderer import Renderer


def save_image(renderer: Renderer, img: Image.Image, name: str, output_dir: Path) -> None:
    """Save image as PNG."""
    # Finalize compositing Cairo + PIL
    final_img = renderer.finalize(img)
    output_path = output_dir / f"{name}.png"
    final_img.save(output_path, format="PNG")
    print(f"  + {output_path}")


def generate_system_monitor(renderer: Renderer, output_dir: Path) -> None:
    """Generate a system monitor dashboard with horizontal bars."""
    img, draw = renderer.create_canvas()

    # Title bar
    renderer.draw_text(
        draw, "SYSTEM", (120, 12), font=renderer.font_small_bold, color=COLOR_WHITE, anchor="mm"
    )

    # Top section: CPU and Memory as horizontal bars
    # CPU bar (left panel)
    renderer.draw_panel(draw, (8, 28, 116, 80), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "cpu", (16, 36), size=14, color=COLOR_TEAL)
    renderer.draw_text(
        draw, "CPU", (36, 43), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    cpu_percent = 42
    renderer.draw_text(
        draw,
        f"{cpu_percent}%",
        (100, 43),
        font=renderer.font_medium_bold,
        color=COLOR_WHITE,
        anchor="rm",
    )
    renderer.draw_bar(draw, (16, 58, 108, 70), cpu_percent, COLOR_TEAL, COLOR_DARK_GRAY)

    # Memory bar (right panel)
    renderer.draw_panel(draw, (124, 28, 232, 80), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "memory", (132, 36), size=14, color=COLOR_PURPLE)
    renderer.draw_text(
        draw, "MEM", (152, 43), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    mem_percent = 68
    renderer.draw_text(
        draw,
        f"{mem_percent}%",
        (216, 43),
        font=renderer.font_medium_bold,
        color=COLOR_WHITE,
        anchor="rm",
    )
    renderer.draw_bar(draw, (132, 58, 224, 70), mem_percent, COLOR_PURPLE, COLOR_DARK_GRAY)

    # Middle section: Disk and Network bars
    y_start = 90

    # Disk usage bar
    renderer.draw_icon(draw, "disk", (12, y_start), size=14, color=COLOR_ORANGE)
    renderer.draw_text(
        draw, "DISK", (32, y_start + 7), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_segmented_bar(
        draw,
        (70, y_start + 2, 185, y_start + 12),
        [(45, COLOR_ORANGE), (20, COLOR_GOLD)],
        COLOR_DARK_GRAY,
    )
    renderer.draw_text(
        draw, "65%", (195, y_start + 7), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    # Network bar
    y_start += 24
    renderer.draw_icon(draw, "network", (12, y_start), size=14, color=COLOR_LIME)
    renderer.draw_text(
        draw, "NET", (32, y_start + 7), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    net_data = [
        20,
        25,
        35,
        40,
        45,
        38,
        30,
        40,
        55,
        65,
        70,
        68,
        65,
        72,
        80,
        78,
        75,
        68,
        60,
        52,
        45,
        50,
        55,
    ]
    renderer.draw_mini_bars(
        draw, (70, y_start, 185, y_start + 14), net_data, COLOR_LIME, bar_width=4, gap=2
    )
    renderer.draw_text(
        draw, "48Mb", (195, y_start + 7), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    # Bottom section: Process list
    y_start = 140

    # Panel background
    renderer.draw_panel(draw, (8, y_start, 232, 232), COLOR_PANEL, radius=4)

    # Process header
    renderer.draw_text(
        draw,
        "TOP PROCESSES",
        (16, y_start + 12),
        font=renderer.font_small_bold,
        color=COLOR_GRAY,
        anchor="lm",
    )

    # Process rows
    processes = [
        ("node", 12.4, COLOR_TEAL),
        ("python", 8.2, COLOR_PURPLE),
        ("chrome", 5.1, COLOR_LIME),
        ("docker", 4.8, COLOR_BLUE),
    ]

    for i, (name, cpu, color) in enumerate(processes):
        row_y = y_start + 30 + i * 20
        renderer.draw_text(
            draw, name, (16, row_y), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
        )
        bar_width = int(cpu * 8)
        renderer.draw_rounded_rect(
            draw, (80, row_y - 5, 80 + bar_width, row_y + 5), radius=3, fill=color
        )
        renderer.draw_text(
            draw, f"{cpu}%", (195, row_y), font=renderer.font_small, color=color, anchor="lm"
        )

    save_image(renderer, img, "01_system_monitor", output_dir)


def generate_smart_home(renderer: Renderer, output_dir: Path) -> None:
    """Generate a smart home dashboard."""
    img, draw = renderer.create_canvas()

    # Title
    renderer.draw_icon(draw, "home", (10, 8), size=16, color=COLOR_TEAL)
    renderer.draw_text(
        draw, "HOME", (32, 16), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    # Temperature panel (top left)
    renderer.draw_panel(draw, (8, 32, 116, 100), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "temp", (16, 40), size=14, color=COLOR_ORANGE)
    renderer.draw_text(
        draw, "LIVING ROOM", (36, 47), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw, "21.5", (50, 75), font=renderer.font_xlarge, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "\u00b0", (80, 68), font=renderer.font_medium, color=COLOR_GRAY, anchor="mm"
    )
    temp_data = [
        20.2,
        20.4,
        20.5,
        20.7,
        20.8,
        20.9,
        21.0,
        21.1,
        21.2,
        21.3,
        21.4,
        21.5,
        21.4,
        21.3,
        21.4,
        21.5,
    ]
    renderer.draw_sparkline(draw, (16, 85, 108, 95), temp_data, COLOR_ORANGE, fill=True)

    # Humidity panel (top right)
    renderer.draw_panel(draw, (124, 32, 232, 100), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "drop", (132, 40), size=14, color=COLOR_BLUE)
    renderer.draw_text(
        draw, "HUMIDITY", (152, 47), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw, "58%", (178, 75), font=renderer.font_xlarge, color=COLOR_WHITE, anchor="mm"
    )
    humidity_data = [54, 54, 55, 55, 56, 56, 57, 57, 58, 58, 57, 57, 58, 58, 58, 58]
    renderer.draw_sparkline(draw, (132, 85, 224, 95), humidity_data, COLOR_BLUE, fill=True)

    # Devices section
    renderer.draw_text(
        draw, "DEVICES", (16, 115), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    devices = [
        ("Lights", True, COLOR_YELLOW),
        ("AC", True, COLOR_TEAL),
        ("TV", False, COLOR_GRAY),
        ("Music", True, COLOR_LIME),
    ]

    for i, (name, on, color) in enumerate(devices):
        x = 16 + (i % 2) * 112
        y = 130 + (i // 2) * 50
        renderer.draw_panel(draw, (x, y, x + 104, y + 42), COLOR_PANEL, radius=4)

        # Status indicator
        status_color = color if on else COLOR_DARK_GRAY
        renderer.draw_ellipse(draw, (x + 10, y + 16, x + 18, y + 24), fill=status_color)

        renderer.draw_text(
            draw, name, (x + 28, y + 13), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
        )
        status_text = "ON" if on else "OFF"
        renderer.draw_text(
            draw,
            status_text,
            (x + 28, y + 28),
            font=renderer.font_tiny,
            color=status_color,
            anchor="lm",
        )

    save_image(renderer, img, "02_smart_home", output_dir)


def generate_weather(renderer: Renderer, output_dir: Path) -> None:
    """Generate a weather dashboard."""
    img, draw = renderer.create_canvas()

    # Current weather - large display
    renderer.draw_icon(draw, "sun", (100, 20), size=24, color=COLOR_YELLOW)

    renderer.draw_text(
        draw, "24", (105, 75), font=renderer.font_huge, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "\u00b0", (140, 60), font=renderer.font_large, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw, "Sunny", (120, 105), font=renderer.font_regular, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw, "San Francisco", (120, 122), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )

    # Weather details row
    y_row = 145
    details = [
        ("H: 28\u00b0", COLOR_RED),
        ("L: 18\u00b0", COLOR_BLUE),
        ("45%", COLOR_TEAL),
        ("12km/h", COLOR_WHITE),
    ]

    for i, (text, color) in enumerate(details):
        x = 25 + i * 55
        renderer.draw_text(
            draw, text, (x, y_row), font=renderer.font_tiny, color=color, anchor="lm"
        )

    # Forecast section
    renderer.draw_panel(draw, (8, 165, 232, 232), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "5-DAY FORECAST", (16, 177), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    forecast = [
        ("Mon", 26, 19, COLOR_YELLOW),
        ("Tue", 24, 18, COLOR_YELLOW),
        ("Wed", 22, 17, COLOR_GRAY),
        ("Thu", 20, 15, COLOR_BLUE),
        ("Fri", 23, 17, COLOR_YELLOW),
    ]

    for i, (day, high, _low, color) in enumerate(forecast):
        x = 24 + i * 44
        renderer.draw_text(
            draw, day, (x, 195), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
        )
        renderer.draw_ellipse(draw, (x - 4, 203, x + 4, 211), fill=color)
        renderer.draw_text(
            draw, f"{high}\u00b0", (x, 222), font=renderer.font_tiny, color=COLOR_WHITE, anchor="mm"
        )

    save_image(renderer, img, "03_weather", output_dir)


def generate_server_stats(renderer: Renderer, output_dir: Path) -> None:
    """Generate a server statistics dashboard with horizontal bars."""
    img, draw = renderer.create_canvas()

    # Header
    renderer.draw_text(
        draw, "SERVER", (120, 12), font=renderer.font_small_bold, color=COLOR_WHITE, anchor="mm"
    )

    # CPU section with bar and sparkline
    renderer.draw_panel(draw, (8, 28, 232, 85), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "cpu", (16, 36), size=14, color=COLOR_TEAL)
    renderer.draw_text(
        draw, "CPU", (36, 43), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    cpu = 73
    renderer.draw_text(
        draw, f"{cpu}%", (220, 43), font=renderer.font_large, color=COLOR_WHITE, anchor="rm"
    )
    renderer.draw_bar(draw, (16, 55, 224, 65), cpu, COLOR_TEAL, COLOR_DARK_GRAY)

    # Sparkline for history
    cpu_history = [
        45,
        47,
        50,
        52,
        49,
        48,
        55,
        62,
        65,
        68,
        72,
        70,
        68,
        72,
        75,
        78,
        82,
        80,
        78,
        75,
        73,
    ]
    renderer.draw_sparkline(draw, (16, 70, 224, 80), cpu_history, COLOR_TEAL, fill=True)

    # Metrics grid (2x2)
    metrics = [
        ("LOAD", "2.4", COLOR_LIME),
        ("UPTIME", "14d", COLOR_PURPLE),
        ("TEMP", "58°C", COLOR_ORANGE),
        ("CONN", "1,247", COLOR_BLUE),
    ]

    for i, (label, value, color) in enumerate(metrics):
        col = i % 2
        row = i // 2
        x = 16 + col * 112
        y = 95 + row * 32
        renderer.draw_text(
            draw, label, (x, y), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw, value, (x, y + 14), font=renderer.font_medium_bold, color=color, anchor="lm"
        )

    # Resource bars section
    y_section = 160
    renderer.draw_text(
        draw,
        "RESOURCES",
        (16, y_section),
        font=renderer.font_small_bold,
        color=COLOR_GRAY,
        anchor="lm",
    )

    resources = [
        ("MEM", 68, COLOR_PURPLE, "5.4/8 GB"),
        ("DISK", 45, COLOR_ORANGE, "180/400 GB"),
    ]

    for i, (name, percent, color, detail) in enumerate(resources):
        y = y_section + 18 + i * 22
        renderer.draw_text(
            draw, name, (16, y + 5), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_rounded_rect(draw, (50, y, 170, y + 10), radius=2, fill=COLOR_DARK_GRAY)
        bar_width = int(120 * percent / 100)
        renderer.draw_rounded_rect(draw, (50, y, 50 + bar_width, y + 10), radius=2, fill=color)
        renderer.draw_text(
            draw, detail, (180, y + 5), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
        )

    # Network I/O with geometric arrows
    y_net = 215
    renderer.draw_icon(draw, "arrow_up", (16, y_net - 2), size=10, color=COLOR_LIME)
    renderer.draw_text(
        draw, "125 MB/s", (30, y_net + 3), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_icon(draw, "arrow_down", (120, y_net - 2), size=10, color=COLOR_RED)
    renderer.draw_text(
        draw, "48 MB/s", (134, y_net + 3), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    save_image(renderer, img, "04_server_stats", output_dir)


def generate_media_player(renderer: Renderer, output_dir: Path) -> None:
    """Generate a media player display with geometric icons."""
    img, draw = renderer.create_canvas()

    # Album art placeholder (gradient with music note)
    for i in range(80):
        grad_color = renderer.blend_color(COLOR_PURPLE, COLOR_TEAL, i / 80)
        renderer.draw_line(draw, [(80 + i, 20), (80 + i, 100)], fill=grad_color, width=1)
    # Music note icon in center of album art
    renderer.draw_icon(draw, "music", (112, 52), size=16, color=COLOR_WHITE)

    # Track info
    renderer.draw_text(
        draw, "NOW PLAYING", (120, 115), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw,
        "Bohemian Rhapsody",
        (120, 138),
        font=renderer.font_medium_bold,
        color=COLOR_WHITE,
        anchor="mm",
    )
    renderer.draw_text(
        draw, "Queen", (120, 160), font=renderer.font_small, color=COLOR_TEAL, anchor="mm"
    )

    # Progress bar
    progress = 65
    renderer.draw_rounded_rect(draw, (20, 180, 220, 188), radius=4, fill=COLOR_DARK_GRAY)
    bar_width = int(200 * progress / 100)
    renderer.draw_rounded_rect(draw, (20, 180, 20 + bar_width, 188), radius=4, fill=COLOR_TEAL)

    # Time labels
    renderer.draw_text(
        draw, "2:45", (20, 198), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_text(
        draw, "5:54", (220, 198), font=renderer.font_tiny, color=COLOR_GRAY, anchor="rm"
    )

    # Controls with geometric icons
    controls_y = 218
    renderer.draw_icon(draw, "skip_prev", (60, controls_y), size=18, color=COLOR_GRAY)
    renderer.draw_icon(draw, "pause", (107, controls_y - 3), size=24, color=COLOR_WHITE)
    renderer.draw_icon(draw, "skip_next", (160, controls_y), size=18, color=COLOR_GRAY)

    save_image(renderer, img, "05_media_player", output_dir)


def generate_energy_monitor(renderer: Renderer, output_dir: Path) -> None:
    """Generate an energy monitoring dashboard."""
    img, draw = renderer.create_canvas()

    # Header
    renderer.draw_icon(draw, "bolt", (10, 8), size=16, color=COLOR_YELLOW)
    renderer.draw_text(
        draw, "ENERGY", (32, 16), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    # Main power display
    renderer.draw_panel(draw, (8, 32, 232, 95), COLOR_PANEL, radius=4)

    # Current power with large display
    renderer.draw_text(
        draw, "2.4", (70, 55), font=renderer.font_huge, color=COLOR_LIME, anchor="mm"
    )
    renderer.draw_text(
        draw, "kW", (70, 82), font=renderer.font_small, color=COLOR_GRAY, anchor="mm"
    )

    # Solar generation
    renderer.draw_icon(draw, "sun", (130, 40), size=14, color=COLOR_YELLOW)
    renderer.draw_text(
        draw, "SOLAR", (150, 47), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw, "3.8 kW", (150, 62), font=renderer.font_medium, color=COLOR_YELLOW, anchor="lm"
    )

    # Grid
    renderer.draw_text(
        draw, "GRID", (150, 78), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw, "-1.4 kW", (150, 88), font=renderer.font_small, color=COLOR_LIME, anchor="lm"
    )

    # Today's usage section
    renderer.draw_text(
        draw, "TODAY", (16, 108), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    usage_data = [
        1.2,
        1.0,
        0.8,
        0.6,
        0.5,
        0.4,
        0.5,
        0.6,
        0.9,
        1.2,
        1.5,
        2.0,
        2.5,
        2.8,
        3.0,
        3.2,
        3.0,
        2.7,
        2.4,
        2.2,
        2.0,
        1.9,
        1.8,
        2.0,
        2.2,
        2.4,
    ]
    renderer.draw_panel(draw, (8, 118, 232, 165), COLOR_PANEL, radius=4)
    renderer.draw_sparkline(draw, (16, 125, 224, 158), usage_data, COLOR_TEAL, fill=True)

    # Stats row
    stats = [
        ("USED", "18.4 kWh", COLOR_ORANGE),
        ("SOLAR", "24.2 kWh", COLOR_YELLOW),
        ("EXPORT", "8.1 kWh", COLOR_LIME),
    ]

    for i, (label, value, color) in enumerate(stats):
        x = 16 + i * 75
        y = 175
        renderer.draw_text(
            draw, label, (x, y), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw, value, (x, y + 14), font=renderer.font_small, color=color, anchor="lm"
        )

    # Cost (adjusted layout for larger fonts)
    renderer.draw_panel(draw, (8, 205, 232, 232), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "COST", (16, 218), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw, "$2.45", (55, 218), font=renderer.font_medium, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_text(
        draw, "SAVED", (135, 218), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw, "$4.80", (180, 218), font=renderer.font_medium, color=COLOR_LIME, anchor="lm"
    )

    save_image(renderer, img, "06_energy_monitor", output_dir)


def generate_fitness(renderer: Renderer, output_dir: Path) -> None:
    """Generate a fitness tracking dashboard with horizontal progress bars."""
    img, draw = renderer.create_canvas()

    # Header with heart rate
    renderer.draw_text(
        draw, "FITNESS", (16, 14), font=renderer.font_small_bold, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_icon(draw, "heart", (180, 6), size=14, color=COLOR_PINK)
    renderer.draw_text(
        draw, "72 bpm", (200, 14), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    # Activity progress bars (replacing Apple Watch rings)
    activities = [
        ("MOVE", 680, 800, "CAL", COLOR_PINK, 85),
        ("EXERCISE", 24, 40, "MIN", COLOR_LIME, 60),
        ("STAND", 12, 12, "HR", COLOR_TEAL, 100),
    ]

    for i, (label, current, goal, unit, color, percent) in enumerate(activities):
        y = 35 + i * 45

        # Activity panel
        renderer.draw_panel(draw, (8, y, 232, y + 40), COLOR_PANEL, radius=4)

        # Icon placeholder (colored dot for activity type)
        renderer.draw_ellipse(draw, (16, y + 12, 26, y + 22), fill=color)

        # Label and progress
        renderer.draw_text(
            draw, label, (34, y + 10), font=renderer.font_small_bold, color=color, anchor="lm"
        )
        renderer.draw_text(
            draw,
            f"{current}/{goal} {unit}",
            (34, y + 26),
            font=renderer.font_tiny,
            color=COLOR_GRAY,
            anchor="lm",
        )

        # Percentage on right
        renderer.draw_text(
            draw,
            f"{percent}%",
            (220, y + 18),
            font=renderer.font_medium_bold,
            color=COLOR_WHITE,
            anchor="rm",
        )

        # Progress bar
        renderer.draw_bar(draw, (120, y + 28, 220, y + 35), percent, color, COLOR_DARK_GRAY)

    # Stats section (simpler, with dots instead of emoji)
    y_stats = 175
    renderer.draw_panel(draw, (8, y_stats, 232, 232), COLOR_PANEL, radius=4)

    stats = [
        ("STEPS", "8,542", COLOR_PINK),
        ("DISTANCE", "5.2 km", COLOR_LIME),
        ("FLOORS", "14", COLOR_TEAL),
        ("ACTIVE", "45 min", COLOR_PURPLE),
    ]

    for i, (label, value, color) in enumerate(stats):
        col = i % 2
        row = i // 2
        x = 16 + col * 112
        y = y_stats + 10 + row * 28

        renderer.draw_ellipse(draw, (x, y + 4, x + 6, y + 10), fill=color)
        renderer.draw_text(
            draw, label, (x + 12, y), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw,
            value,
            (x + 12, y + 14),
            font=renderer.font_medium_bold,
            color=COLOR_WHITE,
            anchor="lm",
        )

    save_image(renderer, img, "07_fitness", output_dir)


def generate_clock_dashboard(renderer: Renderer, output_dir: Path) -> None:
    """Generate an advanced clock dashboard."""
    img, draw = renderer.create_canvas()

    # Large time display
    renderer.draw_text(
        draw, "14:32", (120, 60), font=renderer.font_huge, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, ":48", (185, 55), font=renderer.font_medium, color=COLOR_GRAY, anchor="lm"
    )

    # Date
    renderer.draw_text(
        draw,
        "Saturday, December 14",
        (120, 95),
        font=renderer.font_small,
        color=COLOR_GRAY,
        anchor="mm",
    )

    # Weather inline
    renderer.draw_icon(draw, "sun", (70, 115), size=16, color=COLOR_YELLOW)
    renderer.draw_text(
        draw,
        "24\u00b0C  Sunny",
        (92, 123),
        font=renderer.font_small,
        color=COLOR_WHITE,
        anchor="lm",
    )

    # Calendar events panel
    renderer.draw_panel(draw, (8, 145, 232, 232), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "UPCOMING", (16, 157), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    events = [
        ("15:00", "Team Meeting", COLOR_TEAL),
        ("17:30", "Gym Session", COLOR_LIME),
        ("19:00", "Dinner with Alex", COLOR_ORANGE),
    ]

    for i, (time, event, color) in enumerate(events):
        y = 172 + i * 20
        renderer.draw_rect(draw, (16, y, 20, y + 14), fill=color)
        renderer.draw_text(
            draw, time, (28, y + 7), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw, event, (70, y + 7), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
        )

    save_image(renderer, img, "08_clock_dashboard", output_dir)


def generate_network_monitor(renderer: Renderer, output_dir: Path) -> None:
    """Generate a network monitoring dashboard."""
    img, draw = renderer.create_canvas()

    # Header
    renderer.draw_icon(draw, "network", (10, 8), size=16, color=COLOR_LIME)
    renderer.draw_text(
        draw, "NETWORK", (32, 16), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
    )

    # Status indicator
    renderer.draw_ellipse(draw, (200, 10, 210, 20), fill=COLOR_LIME)
    renderer.draw_text(
        draw, "OK", (215, 15), font=renderer.font_tiny, color=COLOR_LIME, anchor="lm"
    )

    # Speed test results
    renderer.draw_panel(draw, (8, 32, 116, 100), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "DOWNLOAD", (62, 45), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw, "245", (62, 70), font=renderer.font_xlarge, color=COLOR_TEAL, anchor="mm"
    )
    renderer.draw_text(
        draw, "Mbps", (62, 90), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )

    renderer.draw_panel(draw, (124, 32, 232, 100), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "UPLOAD", (178, 45), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw, "48", (178, 70), font=renderer.font_xlarge, color=COLOR_PURPLE, anchor="mm"
    )
    renderer.draw_text(
        draw, "Mbps", (178, 90), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )

    # Traffic graph
    renderer.draw_text(
        draw, "TRAFFIC (24H)", (16, 115), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    traffic = [
        45,
        48,
        52,
        48,
        42,
        38,
        45,
        55,
        65,
        68,
        72,
        68,
        60,
        55,
        52,
        48,
        55,
        65,
        75,
        82,
        88,
        90,
        85,
        78,
        75,
        72,
        68,
        62,
        55,
        48,
        42,
        38,
        42,
        45,
        48,
        52,
        58,
        65,
        72,
        78,
        85,
        80,
        75,
        72,
        68,
        62,
        58,
        52,
        48,
        45,
        42,
        38,
        40,
        42,
    ]
    renderer.draw_panel(draw, (8, 125, 232, 175), COLOR_PANEL, radius=4)
    renderer.draw_sparkline(draw, (16, 132, 224, 168), traffic, COLOR_TEAL, fill=True)

    # Connected devices
    renderer.draw_text(
        draw, "DEVICES", (16, 185), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    devices = [
        ("iPhone", "192.168.1.42", COLOR_LIME),
        ("MacBook", "192.168.1.15", COLOR_LIME),
        ("Smart TV", "192.168.1.80", COLOR_GOLD),
    ]

    for i, (name, ip, color) in enumerate(devices):
        y = 198 + i * 12
        renderer.draw_ellipse(draw, (16, y, 20, y + 4), fill=color)
        renderer.draw_text(
            draw, name, (28, y + 2), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
        )
        renderer.draw_text(
            draw, ip, (140, y + 2), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )

    save_image(renderer, img, "09_network_monitor", output_dir)


def generate_thermostat(renderer: Renderer, output_dir: Path) -> None:
    """Generate a climate control dashboard with arc gauge."""
    img, draw = renderer.create_canvas()

    # Header
    renderer.draw_text(
        draw, "CLIMATE", (120, 14), font=renderer.font_small_bold, color=COLOR_WHITE, anchor="mm"
    )

    # Large temperature arc gauge
    renderer.draw_arc(draw, (40, 35, 200, 145), 72, COLOR_ORANGE, COLOR_DARK_GRAY, width=12)

    # Target temperature in center
    renderer.draw_text(
        draw, "22", (120, 85), font=renderer.font_huge, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "°C", (160, 75), font=renderer.font_medium, color=COLOR_GRAY, anchor="lm"
    )

    # Up/down controls
    renderer.draw_icon(draw, "arrow_up", (85, 130), size=16, color=COLOR_GRAY)
    renderer.draw_text(
        draw, "TARGET", (120, 138), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_icon(draw, "arrow_down", (140, 130), size=16, color=COLOR_GRAY)

    # Current conditions panel
    renderer.draw_panel(draw, (8, 155, 232, 205), COLOR_PANEL, radius=4)

    conditions = [
        ("CURRENT", "21.5°C", COLOR_TEAL),
        ("HUMIDITY", "58%", COLOR_BLUE),
        ("MODE", "Heating", COLOR_ORANGE),
    ]

    for i, (label, value, color) in enumerate(conditions):
        x = 20 + i * 72
        renderer.draw_text(
            draw, label, (x, 165), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw, value, (x, 182), font=renderer.font_small, color=color, anchor="lm"
        )

    # Room temperatures footer
    renderer.draw_text(
        draw, "ROOMS", (16, 215), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    rooms = [
        ("Living", "22°", COLOR_LIME),
        ("Bed", "19°", COLOR_TEAL),
        ("Bath", "24°", COLOR_ORANGE),
    ]

    for i, (room, temp, color) in enumerate(rooms):
        x = 70 + i * 58
        renderer.draw_ellipse(draw, (x, 216, x + 6, 222), fill=color)
        renderer.draw_text(
            draw,
            f"{room} {temp}",
            (x + 10, 219),
            font=renderer.font_tiny,
            color=COLOR_WHITE,
            anchor="lm",
        )

    save_image(renderer, img, "10_thermostat", output_dir)


def generate_batteries(renderer: Renderer, output_dir: Path) -> None:
    """Generate a battery status dashboard with vertical battery bars."""
    img, draw = renderer.create_canvas()

    # Header
    renderer.draw_icon(draw, "battery", (10, 6), size=16, color=COLOR_LIME)
    renderer.draw_text(
        draw, "BATTERIES", (32, 14), font=renderer.font_small_bold, color=COLOR_WHITE, anchor="lm"
    )

    # Battery grid
    batteries = [
        ("iPhone", 87, COLOR_LIME),
        ("iPad", 42, COLOR_GOLD),
        ("Watch", 15, COLOR_RED),
        ("AirPods", 100, COLOR_LIME),
    ]

    for i, (name, percent, color) in enumerate(batteries):
        x = 16 + i * 56
        y_top = 35

        # Battery outline
        renderer.draw_rounded_rect(
            draw, (x, y_top, x + 44, y_top + 90), radius=4, outline=COLOR_GRAY
        )
        # Battery cap
        renderer.draw_rounded_rect(
            draw, (x + 14, y_top - 4, x + 30, y_top), radius=2, fill=COLOR_GRAY
        )

        # Battery fill (from bottom up)
        fill_height = int(82 * percent / 100)
        if fill_height > 0:
            fill_y = y_top + 86 - fill_height
            renderer.draw_rounded_rect(
                draw, (x + 4, fill_y, x + 40, y_top + 86), radius=2, fill=color
            )

        # Percentage
        renderer.draw_text(
            draw,
            f"{percent}%",
            (x + 22, y_top + 45),
            font=renderer.font_small_bold,
            color=COLOR_WHITE,
            anchor="mm",
        )

        # Device name
        renderer.draw_text(
            draw,
            name,
            (x + 22, y_top + 100),
            font=renderer.font_tiny,
            color=COLOR_WHITE,
            anchor="mm",
        )

    # Warning panel for low battery
    renderer.draw_panel(draw, (8, 155, 232, 195), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "warning", (16, 165), size=16, color=COLOR_RED)
    renderer.draw_text(
        draw, "LOW BATTERY", (40, 168), font=renderer.font_small_bold, color=COLOR_RED, anchor="lm"
    )
    renderer.draw_text(
        draw,
        "Watch needs charging soon",
        (40, 182),
        font=renderer.font_tiny,
        color=COLOR_GRAY,
        anchor="lm",
    )

    # Last updated
    renderer.draw_text(
        draw,
        "Updated 2 min ago",
        (120, 215),
        font=renderer.font_tiny,
        color=COLOR_GRAY,
        anchor="mm",
    )

    save_image(renderer, img, "11_batteries", output_dir)


def generate_security(renderer: Renderer, output_dir: Path) -> None:
    """Generate a home security dashboard with sensor status."""
    img, draw = renderer.create_canvas()

    # Header with status
    renderer.draw_icon(draw, "lock", (10, 6), size=16, color=COLOR_LIME)
    renderer.draw_text(
        draw, "SECURITY", (32, 14), font=renderer.font_small_bold, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_ellipse(draw, (195, 10, 205, 20), fill=COLOR_LIME)
    renderer.draw_text(
        draw, "ARMED", (210, 15), font=renderer.font_tiny, color=COLOR_LIME, anchor="lm"
    )

    # Doors section
    renderer.draw_panel(draw, (8, 28, 232, 105), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "DOORS", (16, 40), font=renderer.font_small_bold, color=COLOR_GRAY, anchor="lm"
    )

    doors = [
        ("Front Door", "LOCKED", True, COLOR_LIME),
        ("Back Door", "LOCKED", True, COLOR_LIME),
        ("Garage", "OPEN", False, COLOR_RED),
    ]

    for i, (name, status, _locked, color) in enumerate(doors):
        y = 55 + i * 16
        renderer.draw_ellipse(draw, (16, y, 22, y + 6), fill=color)
        renderer.draw_text(
            draw, name, (30, y + 3), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
        )
        renderer.draw_text(
            draw, status, (140, y + 3), font=renderer.font_tiny, color=color, anchor="lm"
        )

    # Motion section
    renderer.draw_panel(draw, (8, 112, 232, 180), COLOR_PANEL, radius=4)
    renderer.draw_text(
        draw, "MOTION", (16, 124), font=renderer.font_small_bold, color=COLOR_GRAY, anchor="lm"
    )

    motions = [
        ("Living Room", "Clear", False, COLOR_GRAY),
        ("Kitchen", "Clear", False, COLOR_GRAY),
        ("Backyard", "Detected", True, COLOR_ORANGE),
    ]

    for i, (area, status, detected, color) in enumerate(motions):
        y = 140 + i * 14
        if detected:
            renderer.draw_icon(draw, "motion", (16, y - 2), size=10, color=color)
        else:
            renderer.draw_ellipse(draw, (18, y, 24, y + 6), fill=color)
        renderer.draw_text(
            draw, area, (30, y + 3), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
        )
        renderer.draw_text(
            draw, status, (140, y + 3), font=renderer.font_tiny, color=color, anchor="lm"
        )

    # Last event panel
    renderer.draw_panel(draw, (8, 188, 232, 232), COLOR_PANEL, radius=4)
    renderer.draw_icon(draw, "bell", (16, 200), size=14, color=COLOR_ORANGE)
    renderer.draw_text(
        draw, "LAST EVENT", (36, 200), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_text(
        draw,
        "Backyard motion detected",
        (36, 215),
        font=renderer.font_small,
        color=COLOR_WHITE,
        anchor="lm",
    )

    save_image(renderer, img, "12_security", output_dir)


def main() -> None:
    """Generate all sample renders."""
    output_dir = Path(__file__).parent.parent / "samples"
    output_dir.mkdir(exist_ok=True)

    # Remove old samples
    for old_file in output_dir.glob("*.png"):
        old_file.unlink()

    print("Generating sample renders...")
    print(f"Output directory: {output_dir}\n")

    renderer = Renderer()

    # Generate all samples
    generate_system_monitor(renderer, output_dir)
    generate_smart_home(renderer, output_dir)
    generate_weather(renderer, output_dir)
    generate_server_stats(renderer, output_dir)
    generate_media_player(renderer, output_dir)
    generate_energy_monitor(renderer, output_dir)
    generate_fitness(renderer, output_dir)
    generate_clock_dashboard(renderer, output_dir)
    generate_network_monitor(renderer, output_dir)
    generate_thermostat(renderer, output_dir)
    generate_batteries(renderer, output_dir)
    generate_security(renderer, output_dir)

    print(f"\n+ Generated 12 sample images in {output_dir}/")


if __name__ == "__main__":
    main()
