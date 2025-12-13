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
    """Generate a system monitor dashboard with ring gauges."""
    img, draw = renderer.create_canvas()

    # Title bar
    renderer.draw_text(
        draw, "SYSTEM", (120, 12), font=renderer.font_small, color=COLOR_GRAY, anchor="mm"
    )

    # Top section: CPU and Memory ring gauges
    # CPU Ring (left)
    cpu_center = (60, 70)
    cpu_percent = 42
    renderer.draw_ring_gauge(
        draw, cpu_center, 35, cpu_percent, COLOR_TEAL, COLOR_DARK_GRAY, width=5
    )
    renderer.draw_text(
        draw,
        f"{cpu_percent}%",
        cpu_center,
        font=renderer.font_large,
        color=COLOR_WHITE,
        anchor="mm",
    )
    renderer.draw_text(
        draw, "CPU", (60, 115), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )

    # Memory Ring (right)
    mem_center = (180, 70)
    mem_percent = 68
    renderer.draw_ring_gauge(
        draw, mem_center, 35, mem_percent, COLOR_PURPLE, COLOR_DARK_GRAY, width=5
    )
    renderer.draw_text(
        draw,
        f"{mem_percent}%",
        mem_center,
        font=renderer.font_large,
        color=COLOR_WHITE,
        anchor="mm",
    )
    renderer.draw_text(
        draw, "MEM", (180, 115), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )

    # Middle section: Disk and Network bars
    y_start = 135

    # Disk usage bar
    renderer.draw_icon(draw, "disk", (12, y_start), size=14, color=COLOR_ORANGE)
    renderer.draw_text(
        draw, "DISK", (32, y_start + 7), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )
    renderer.draw_segmented_bar(
        draw,
        (75, y_start + 2, 190, y_start + 12),
        [(45, COLOR_ORANGE), (20, COLOR_GOLD)],
        COLOR_DARK_GRAY,
    )
    renderer.draw_text(
        draw, "65%", (200, y_start + 7), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
    )

    # Network bar
    y_start += 22
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
        draw, (75, y_start, 190, y_start + 14), net_data, COLOR_LIME, bar_width=4, gap=2
    )
    renderer.draw_text(
        draw, "48Mb", (200, y_start + 7), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
    )

    # Bottom section: Process list
    y_start = 185

    # Panel background
    renderer.draw_panel(draw, (8, y_start, 232, 232), COLOR_PANEL, radius=4)

    # Process header
    renderer.draw_text(
        draw,
        "TOP PROCESSES",
        (16, y_start + 10),
        font=renderer.font_tiny,
        color=COLOR_GRAY,
        anchor="lm",
    )

    # Process rows
    processes = [
        ("node", 12.4, COLOR_TEAL),
        ("python", 8.2, COLOR_PURPLE),
        ("chrome", 5.1, COLOR_LIME),
    ]

    for i, (name, cpu, color) in enumerate(processes):
        row_y = y_start + 22 + i * 14
        renderer.draw_text(
            draw, name, (16, row_y), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
        )
        bar_width = int(cpu * 8)
        renderer.draw_rounded_rect(
            draw, (80, row_y - 4, 80 + bar_width, row_y + 4), radius=2, fill=color
        )
        renderer.draw_text(
            draw, f"{cpu}%", (200, row_y), font=renderer.font_tiny, color=color, anchor="lm"
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
    """Generate a server statistics dashboard."""
    img, draw = renderer.create_canvas()

    # Header
    renderer.draw_text(
        draw, "SERVER DASHBOARD", (120, 12), font=renderer.font_small, color=COLOR_TEAL, anchor="mm"
    )

    # Large CPU metric with ring
    cpu_center = (60, 65)
    cpu = 73
    renderer.draw_ring_gauge(draw, cpu_center, 32, cpu, COLOR_TEAL, COLOR_DARK_GRAY, width=6)
    renderer.draw_text(
        draw, f"{cpu}", cpu_center, font=renderer.font_large, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "CPU %", (60, 105), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )

    # Side metrics
    metrics = [
        ("LOAD", "2.4", COLOR_LIME),
        ("TEMP", "58\u00b0C", COLOR_ORANGE),
        ("UPTIME", "14d", COLOR_PURPLE),
    ]

    for i, (label, value, color) in enumerate(metrics):
        y = 35 + i * 28
        renderer.draw_text(
            draw, label, (130, y), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw, value, (130, y + 12), font=renderer.font_medium, color=color, anchor="lm"
        )

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
    renderer.draw_panel(draw, (125, 100, 230, 115), COLOR_PANEL, radius=2)
    renderer.draw_sparkline(draw, (128, 102, 227, 113), cpu_history, COLOR_TEAL, fill=True)

    # Resource bars section
    y_section = 125
    renderer.draw_text(
        draw, "RESOURCES", (16, y_section), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
    )

    resources = [
        ("MEM", 68, COLOR_PURPLE, "5.4/8 GB"),
        ("DISK", 45, COLOR_ORANGE, "180/400 GB"),
        ("SWAP", 12, COLOR_BLUE, "0.5/4 GB"),
    ]

    for i, (name, percent, color, _detail) in enumerate(resources):
        y = y_section + 18 + i * 24
        renderer.draw_text(
            draw, name, (16, y + 5), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_rounded_rect(draw, (50, y, 180, y + 10), radius=2, fill=COLOR_DARK_GRAY)
        bar_width = int(130 * percent / 100)
        renderer.draw_rounded_rect(draw, (50, y, 50 + bar_width, y + 10), radius=2, fill=color)
        renderer.draw_text(
            draw, f"{percent}%", (188, y + 5), font=renderer.font_tiny, color=color, anchor="lm"
        )

    # Network I/O
    y_net = 210
    renderer.draw_text(
        draw, "\u25b2", (16, y_net), font=renderer.font_tiny, color=COLOR_LIME, anchor="lm"
    )
    renderer.draw_text(
        draw, "125 MB/s", (28, y_net), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_text(
        draw, "\u25bc", (100, y_net), font=renderer.font_tiny, color=COLOR_RED, anchor="lm"
    )
    renderer.draw_text(
        draw, "48 MB/s", (112, y_net), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
    )

    # Connections (right-aligned to fit)
    renderer.draw_text(
        draw, "CONN: 1,247", (224, y_net), font=renderer.font_tiny, color=COLOR_GRAY, anchor="rm"
    )

    save_image(renderer, img, "04_server_stats", output_dir)


def generate_media_player(renderer: Renderer, output_dir: Path) -> None:
    """Generate a media player display."""
    img, draw = renderer.create_canvas()

    # Album art placeholder (gradient)
    for i in range(80):
        grad_color = renderer.blend_color(COLOR_PURPLE, COLOR_TEAL, i / 80)
        renderer.draw_line(draw, [(80 + i, 20), (80 + i, 100)], fill=grad_color, width=1)

    # Track info
    renderer.draw_text(
        draw, "NOW PLAYING", (120, 115), font=renderer.font_tiny, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw, "Bohemian", (120, 135), font=renderer.font_medium, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "Rhapsody", (120, 152), font=renderer.font_medium, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "Queen", (120, 172), font=renderer.font_small, color=COLOR_TEAL, anchor="mm"
    )

    # Progress bar
    progress = 65
    renderer.draw_rounded_rect(draw, (20, 192, 220, 198), radius=3, fill=COLOR_DARK_GRAY)
    bar_width = int(200 * progress / 100)
    renderer.draw_rounded_rect(draw, (20, 192, 20 + bar_width, 198), radius=3, fill=COLOR_TEAL)

    # Time labels
    renderer.draw_text(
        draw, "2:45", (20, 208), font=renderer.font_tiny, color=COLOR_WHITE, anchor="lm"
    )
    renderer.draw_text(
        draw, "5:54", (220, 208), font=renderer.font_tiny, color=COLOR_GRAY, anchor="rm"
    )

    # Controls
    controls_y = 225
    renderer.draw_text(
        draw, "\u23ee", (70, controls_y), font=renderer.font_regular, color=COLOR_GRAY, anchor="mm"
    )
    renderer.draw_text(
        draw, "\u23f8", (120, controls_y), font=renderer.font_large, color=COLOR_WHITE, anchor="mm"
    )
    renderer.draw_text(
        draw, "\u23ed", (170, controls_y), font=renderer.font_regular, color=COLOR_GRAY, anchor="mm"
    )

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
    """Generate a fitness tracking dashboard."""
    img, draw = renderer.create_canvas()

    # Activity rings (stacked)
    center = (70, 80)

    # Move ring (outer)
    renderer.draw_ring_gauge(
        draw, center, 50, 85, COLOR_PINK, renderer.dim_color(COLOR_PINK), width=8
    )
    # Exercise ring (middle)
    renderer.draw_ring_gauge(
        draw, center, 38, 60, COLOR_LIME, renderer.dim_color(COLOR_LIME), width=8
    )
    # Stand ring (inner)
    renderer.draw_ring_gauge(
        draw, center, 26, 100, COLOR_TEAL, renderer.dim_color(COLOR_TEAL), width=8
    )

    # Center icon
    renderer.draw_text(
        draw, "\u2665", center, font=renderer.font_large, color=COLOR_PINK, anchor="mm"
    )

    # Ring labels
    labels = [
        ("MOVE", "680/800 CAL", COLOR_PINK),
        ("EXERCISE", "24/40 MIN", COLOR_LIME),
        ("STAND", "12/12 HR", COLOR_TEAL),
    ]

    for i, (label, value, color) in enumerate(labels):
        y = 25 + i * 36
        renderer.draw_text(draw, label, (140, y), font=renderer.font_tiny, color=color, anchor="lm")
        renderer.draw_text(
            draw, value, (140, y + 12), font=renderer.font_small, color=COLOR_WHITE, anchor="lm"
        )

    # Stats section
    y_stats = 145
    renderer.draw_panel(draw, (8, y_stats, 232, 232), COLOR_PANEL, radius=4)

    stats = [
        ("STEPS", "8,542", "\U0001f6b6"),
        ("DIST", "5.2 km", "\U0001f4cd"),
        ("FLOORS", "14", "\U0001f3e2"),
        ("HR", "72 bpm", "\u2665"),
    ]

    for i, (label, value, icon) in enumerate(stats):
        x = 16 + (i % 2) * 110
        y = y_stats + 12 + (i // 2) * 38
        renderer.draw_text(
            draw, icon, (x, y + 8), font=renderer.font_regular, color=COLOR_WHITE, anchor="lm"
        )
        renderer.draw_text(
            draw, label, (x + 25, y), font=renderer.font_tiny, color=COLOR_GRAY, anchor="lm"
        )
        renderer.draw_text(
            draw, value, (x + 25, y + 14), font=renderer.font_medium, color=COLOR_WHITE, anchor="lm"
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


def main() -> None:
    """Generate all sample renders."""
    output_dir = Path(__file__).parent.parent / "samples"
    output_dir.mkdir(exist_ok=True)

    # Remove old samples
    for old_file in output_dir.glob("*.png"):
        old_file.unlink()

    print("Generating sample renders with Cairo...")
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

    print(f"\n+ Generated 9 sample images in {output_dir}/")


if __name__ == "__main__":
    main()
