#!/usr/bin/env python3
"""
Keyboard Layout SVG Generator

Reads keyboard.toml and vial.json to generate an SVG visualization
of all keyboard layers with proper key positioning.
"""

import tomllib
import json
from pathlib import Path
from typing import List, Tuple


class KeyboardLayoutGenerator:
    """Generate SVG visualization of keyboard layouts."""

    # Layer colors
    LAYER_COLORS = {
        0: "#f0f0f0",  # Base layer - light gray
        1: "#e8f4f8",  # Numbers - light blue
        2: "#fff4e8",  # Functions - light orange
        3: "#f0e8ff",  # Navigation - light purple
        4: "#f8e8f0",  # Custom - light pink
    }

    # Key positions for split 3x6+3 layout
    # Format: (x, y) for each key position
    # Each row has 6 positions for the left half
    LEFT_POSITIONS = [
        # Row 0 - all 6 keys
        (0, 40),
        (60, 40),
        (120, 30),
        (180, 20),
        (240, 30),
        (300, 40),
        # Row 1 - all 6 keys
        (0, 100),
        (60, 100),
        (120, 90),
        (180, 80),
        (240, 90),
        (300, 100),
        # Row 2 - all 6 keys (but first is empty in layout)
        (0, 160),
        (60, 160),
        (120, 150),
        (180, 140),
        (240, 150),
        (300, 160),
        # Row 3 / Thumb keys - 3 keys at positions 3, 4, 5
        None,
        None,
        None,
        (180, 220),
        (240, 235),
        (300, 250),
    ]

    RIGHT_POSITIONS = [
        # Row 0 - all 6 keys
        (500, 40),
        (560, 30),
        (620, 20),
        (680, 30),
        (740, 40),
        (800, 40),
        # Row 1 - all 6 keys
        (500, 100),
        (560, 90),
        (620, 80),
        (680, 90),
        (740, 100),
        (800, 100),
        # Row 2 - all 6 keys (but last is empty in layout)
        (500, 160),
        (560, 150),
        (620, 140),
        (680, 150),
        (740, 160),
        (800, 160),
        # Row 3 / Thumb keys - 3 keys at positions 0, 1, 2
        (500, 250),
        (560, 235),
        (620, 220),
        None,
        None,
        None,
    ]

    def __init__(self, toml_path: str = "keyboard.toml", json_path: str = "vial.json"):
        """Initialize generator with config files."""
        self.toml_path = Path(toml_path)
        self.json_path = Path(json_path)
        self.config = None
        self.vial = None
        self.layer_names = {}
        self.key_positions = {}  # Map of key name to position for each layer

    def load_config(self):
        """Load keyboard configuration from TOML file."""
        with open(self.toml_path, "rb") as f:
            self.config = tomllib.load(f)

        # Extract layer names from comments in the TOML file
        self._extract_layer_names()

    def _extract_layer_names(self):
        """Extract layer names from comments in the TOML file."""
        with open(self.toml_path, "r") as f:
            lines = f.readlines()

        layer_idx = 0
        in_keymap = False
        last_comment = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Check if we're entering the keymap array
            if "keymap = [" in stripped:
                in_keymap = True
                continue

            if not in_keymap:
                continue

            # Check if we're exiting the keymap array (closing bracket at start of line)
            if stripped == "]":
                break

            # Look for comments that might be layer names
            if stripped.startswith("#") and not stripped.startswith("##"):
                # Store this comment as a potential layer name
                last_comment = stripped[1:].strip()

            # Check if this line starts a new layer array (single '[' without '[')
            elif stripped == "[" and last_comment:
                # The previous comment was a layer name
                self.layer_names[layer_idx] = last_comment
                layer_idx += 1
                last_comment = None  # Reset after using

    def load_vial(self):
        """Load Vial configuration from JSON file."""
        with open(self.json_path, "r") as f:
            self.vial = json.load(f)

    def get_layer_name(self, layer_idx: int) -> str:
        """Get a descriptive name for the layer."""
        return self.layer_names.get(layer_idx, str(layer_idx))

    def escape_xml(self, text: str) -> str:
        """Escape XML special characters."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    def format_key_label(self, key: str) -> Tuple[List[str], bool]:
        """
        Format key label for display.
        Returns (lines, is_small) where lines is a list of text lines,
        and is_small indicates if small font should be used.
        """
        if not key or key == "_":
            return (["—"], False)

        # Handle mod-tap keys: MT(key, modifier)
        if key.startswith("MT("):
            # Extract key and modifier
            content = key[3:-1]  # Remove "MT(" and ")"
            parts = [p.strip() for p in content.split(",")]
            if len(parts) == 2:
                main_key, modifier = parts
                # Shorten modifier names
                mod_short = modifier.replace("LGui", "Gui").replace("LAlt", "Alt")
                mod_short = mod_short.replace("LShift", "Sft").replace("LCtrl", "Ctl")
                return ([f"{main_key}/{mod_short}"], True)

        # Handle SHIFTED keys
        if key.startswith("SHIFTED("):
            content = key[8:-1]  # Remove "SHIFTED(" and ")"
            # Map shifted keys to their actual symbols
            shifted_map = {
                "9": "(",
                "0": ")",
                "[": "{",
                "]": "}",
                "1": "!",
                "2": "@",
                "3": "#",
                "4": "$",
                "5": "%",
                "6": "^",
                "7": "&",
                "8": "*",
                "-": "_",
                "=": "+",
                ";": ":",
                "'": '"',
                ",": "<",
                ".": ">",
                "/": "?",
                "`": "~",
                "\\": "|",
            }
            display = shifted_map.get(content, f"S-{content}")
            return ([display], False)

        # Handle common keys
        replacements = {
            "tab": "TAB",
            "esc": "ESC",
            "bspc": "BSPC",
            "ent": "ENT",
            "spc": "SPC",
            "comm": ",",
            "lsft": "LSFT",
            "LShift": "LSft",
            "LCtrl": "LCtl",
            "mprv": "PREV",
            "mnxt": "NEXT",
            "volu": "VOL+",
            "vold": "VOL-",
            "mute": "MUTE",
            "mply": "PLAY",
            "PgUp": "PgUp",
            "PgDn": "PgDn",
            "Left": "Left",
            "Right": "Right",
            "Down": "Down",
            "Up": "Up",
            "Del": "Del",
            "Ins": "Ins",
        }

        display_key = replacements.get(key, key)

        # Use small font for longer labels
        is_small = len(display_key) > 3

        return ([display_key], is_small)

    def generate_svg_header(self, width: int, height: int) -> str:
        """Generate SVG header with styles."""
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <style>
      .layer-title {{ font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; fill: #333; }}
      .key {{ fill: #f0f0f0; stroke: #333; stroke-width: 2; rx: 6; }}
      .key-empty {{ fill: #fafafa; stroke: #ccc; stroke-width: 1; stroke-dasharray: 3,3; rx: 6; }}
      .key-text {{ font-family: 'Courier New', monospace; font-size: 12px; fill: #000; text-anchor: middle; }}
      .key-small {{ font-size: 9px; }}
      .empty-label {{ font-family: Arial, sans-serif; font-size: 10px; fill: #999; text-anchor: middle; }}
      .legend {{ font-family: Arial, sans-serif; font-size: 14px; fill: #666; }}
      .combo-line {{ stroke: #003366; stroke-width: 3; fill: none; opacity: 0.7; }}
      .combo-key {{ fill: #003366; stroke: #001a33; stroke-width: 1.5; rx: 3; }}
      .combo-text {{ font-family: 'Courier New', monospace; font-size: 8px; fill: #fff; text-anchor: middle; font-weight: bold; }}
      .combo-overlay {{ fill: #003366; stroke: #001a33; stroke-width: 2; rx: 6; opacity: 0.95; }}
      .combo-overlay-text {{ font-family: 'Courier New', monospace; font-size: 11px; fill: #fff; text-anchor: middle; font-weight: bold; }}
    </style>
  </defs>

'''

    def find_key_position(self, key_name: str, layer_idx: int) -> Tuple[int, int] | None:
        """Find the (x, y) position of a key in a layer."""
        if layer_idx not in self.key_positions:
            return None
        return self.key_positions[layer_idx].get(key_name)

    def are_keys_contiguous(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """Check if two key positions are adjacent (contiguous)."""
        x1, y1 = pos1
        x2, y2 = pos2
        # Keys are 50x50 with spacing, so within 80px is adjacent
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance < 80

    def generate_combo_visual(self, combo: dict, layer_idx: int, x_offset: int = 0, y_offset: int = 0) -> str:
        """Generate SVG visualization for a combo."""
        actions = combo.get("actions", [])
        output = combo.get("output", "")
        combo_layer = combo.get("layer", 0)

        if combo_layer != layer_idx:
            return ""

        if len(actions) < 2:
            return ""

        svg = ""
        
        # Find positions of all keys involved
        positions = []
        for action_key in actions:
            pos = self.find_key_position(action_key, layer_idx)
            if pos:
                positions.append((action_key, pos))

        if len(positions) < 2:
            return ""

        # Adjust positions by offset
        adjusted_positions = [(k, (x + x_offset, y + y_offset)) for k, (x, y) in positions]

        # Check if all keys are contiguous
        all_contiguous = True
        for i in range(len(adjusted_positions) - 1):
            if not self.are_keys_contiguous(adjusted_positions[i][1], adjusted_positions[i + 1][1]):
                all_contiguous = False
                break

        if all_contiguous and len(adjusted_positions) == 2:
            # Draw a small overlay between the two keys
            _, (x1, y1) = adjusted_positions[0]
            _, (x2, y2) = adjusted_positions[1]
            
            # Calculate center point between the two keys
            center_x = (x1 + x2) / 2 + 25  # +25 to get to center of key
            center_y = (y1 + y2) / 2 + 25
            
            # Draw small overlay key
            overlay_size = 28
            overlay_x = center_x - overlay_size / 2
            overlay_y = center_y - overlay_size / 2
            
            svg += f'    <rect x="{overlay_x}" y="{overlay_y}" width="{overlay_size}" height="{overlay_size}" class="combo-overlay"/>\n'
            
            # Format output label
            lines, _ = self.format_key_label(output)
            output_label = self.escape_xml(lines[0] if lines else output)
            
            svg += f'    <text x="{center_x}" y="{center_y + 5}" class="combo-overlay-text">{output_label}</text>\n'
        else:
            # Draw lines connecting the keys
            svg += "    <!-- Combo connection lines -->\n"
            
            # Draw lines from first key to all others
            _, (x1, y1) = adjusted_positions[0]
            key_center_x1 = x1 + 25
            key_center_y1 = y1 + 25
            
            for i in range(1, len(adjusted_positions)):
                _, (x2, y2) = adjusted_positions[i]
                key_center_x2 = x2 + 25
                key_center_y2 = y2 + 25
                
                svg += f'    <line x1="{key_center_x1}" y1="{key_center_y1}" x2="{key_center_x2}" y2="{key_center_y2}" class="combo-line"/>\n'
            
            # Draw small indicator at midpoint showing the output
            if len(adjusted_positions) == 2:
                _, (x2, y2) = adjusted_positions[1]
                mid_x = (key_center_x1 + (x2 + 25)) / 2
                mid_y = (key_center_y1 + (y2 + 25)) / 2
                
                # Format output label
                lines, _ = self.format_key_label(output)
                output_label = self.escape_xml(lines[0] if lines else output)
                
                # Draw small circle with output
                svg += f'    <circle cx="{mid_x}" cy="{mid_y}" r="15" class="combo-overlay"/>\n'
                svg += f'    <text x="{mid_x}" y="{mid_y + 4}" class="combo-overlay-text">{output_label}</text>\n'

        return svg

    def build_key_position_map(self, layer_idx: int):
        """Build a map of key names to their positions for a layer."""
        keymap = self.config["layout"]["keymap"]
        
        if layer_idx >= len(keymap):
            return

        layer_keys = keymap[layer_idx]
        self.key_positions[layer_idx] = {}

        # Map left half
        for row in range(4):
            for col in range(6):
                pos_idx = row * 6 + col
                pos = self.LEFT_POSITIONS[pos_idx]
                if pos is None:
                    continue
                key = layer_keys[row][col]
                if key and key != "_":
                    self.key_positions[layer_idx][key] = pos

        # Map right half
        for row in range(4):
            for col in range(6):
                pos_idx = row * 6 + col
                pos = self.RIGHT_POSITIONS[pos_idx]
                if pos is None:
                    continue
                key = layer_keys[row][col + 6]
                if key and key != "_":
                    self.key_positions[layer_idx][key] = pos

    def generate_key(
        self, x: int, y: int, label: str, layer_idx: int, is_transparent: bool = False
    ) -> str:
        """Generate SVG for a single key."""
        lines, is_small = self.format_key_label(label)

        svg = ""

        # Draw key rectangle with rounded corners
        if is_transparent or not label or label == "_":
            svg += f'    <rect x="{x}" y="{y}" width="50" height="50" rx="6" class="key-empty"/>\n'
            svg += f'    <text x="{x + 25}" y="{y + 28}" class="empty-label">—</text>\n'
        else:
            color = self.LAYER_COLORS.get(layer_idx, "#f0f0f0")
            svg += f'    <rect x="{x}" y="{y}" width="50" height="50" rx="6" class="key" style="fill: {color}"/>\n'

            # Draw text
            font_class = "key-small" if is_small else ""

            if len(lines) == 1:
                # Single line - center vertically
                text_y = y + 30
                escaped_text = self.escape_xml(lines[0])
                svg += f'    <text x="{x + 25}" y="{text_y}" class="key-text {font_class}">{escaped_text}</text>\n'
            else:
                # Multiple lines
                start_y = y + 22
                for i, line in enumerate(lines):
                    text_y = start_y + (i * 12)
                    escaped_text = self.escape_xml(line)
                    svg += f'    <text x="{x + 25}" y="{text_y}" class="key-text {font_class}">{escaped_text}</text>\n'

        return svg

    def generate_layer(self, layer_idx: int, y_offset: int) -> str:
        """Generate SVG for a complete layer."""
        keymap = self.config["layout"]["keymap"]

        if layer_idx >= len(keymap):
            # Layer not defined
            layer_name = self.get_layer_name(layer_idx)
            svg = f'  <g id="layer{layer_idx}" transform="translate(50, {y_offset})">\n'
            svg += f'    <text x="400" y="0" class="layer-title">Layer {layer_idx}: {layer_name}</text>\n'
            svg += '    <text x="400" y="150" class="legend" style="font-size: 18px;">'
            svg += (
                "(Layer is defined but has no key mappings in keyboard.toml)</text>\n"
            )
            svg += "  </g>\n\n"
            return svg

        layer_keys = keymap[layer_idx]
        layer_name = self.get_layer_name(layer_idx)

        svg = f"  <!-- Layer {layer_idx}: {layer_name} -->\n"
        svg += f'  <g id="layer{layer_idx}" transform="translate(50, {y_offset})">\n'
        svg += f'    <text x="400" y="0" class="layer-title">Layer {layer_idx}: {layer_name}</text>\n\n'

        # Draw left half (first 6 columns of each row)
        svg += "    <!-- Left half -->\n"
        for row in range(4):
            for col in range(6):
                pos_idx = row * 6 + col
                pos = self.LEFT_POSITIONS[pos_idx]
                if pos is None:
                    continue
                key = layer_keys[row][col]
                is_transparent = key == "_" and layer_idx > 0
                svg += self.generate_key(pos[0], pos[1], key, layer_idx, is_transparent)

        # Draw right half (last 6 columns of each row)
        svg += "\n    <!-- Right half -->\n"
        for row in range(4):
            for col in range(6):
                pos_idx = row * 6 + col
                pos = self.RIGHT_POSITIONS[pos_idx]
                if pos is None:
                    continue
                key = layer_keys[row][col + 6]  # Offset by 6 for right half
                is_transparent = key == "_" and layer_idx > 0
                svg += self.generate_key(pos[0], pos[1], key, layer_idx, is_transparent)

        # Draw combos for this layer
        if "behavior" in self.config and "combo" in self.config["behavior"]:
            combos = self.config["behavior"]["combo"].get("combos", [])
            if combos:
                svg += "\n    <!-- Combos -->\n"
                for combo in combos:
                    svg += self.generate_combo_visual(combo, layer_idx, 0, 0)

        svg += "  </g>\n\n"
        return svg

    def generate_legend(self, y_offset: int) -> str:
        """Generate legend section."""
        svg = "  <!-- Legend -->\n"
        svg += f'  <g id="legend" transform="translate(50, {y_offset})">\n'
        svg += '    <text x="0" y="0" class="layer-title">Legend &amp; Info</text>\n\n'

        keyboard_name = self.config["keyboard"]["name"]
        num_layers = self.config["layout"]["layers"]

        svg += f'    <text x="0" y="40" class="legend">• Keyboard: {keyboard_name} (Split 3×6+3 layout)</text>\n'
        svg += '    <text x="0" y="65" class="legend">• Total Keys: 42 (21 per side)</text>\n'

        # Show combos if defined
        if "behavior" in self.config and "combo" in self.config["behavior"]:
            combos = self.config["behavior"]["combo"].get("combos", [])
            if combos:
                for combo in combos[:3]:  # Show first 3 combos
                    actions = " + ".join(combo["actions"])
                    output = combo["output"]
                    y = 90 + (combos.index(combo) * 25)
                    svg += f'    <text x="0" y="{y}" class="legend">• Combo: {actions} = {output}</text>\n'

        svg += '    <text x="0" y="115" class="legend">• MT() = Mod-Tap (hold for modifier, tap for key)</text>\n\n'

        # Color legend
        y_pos = 140
        for layer_idx in range(min(num_layers, 5)):
            color = self.LAYER_COLORS.get(layer_idx, "#f0f0f0")
            name = self.get_layer_name(layer_idx)
            svg += f'    <rect x="0" y="{y_pos}" width="50" height="30" rx="6" class="key" style="fill: {color}"/>\n'
            svg += f'    <text x="60" y="{y_pos + 20}" class="legend">Layer {layer_idx}: {name}</text>\n\n'
            y_pos += 40

        # Transparent key legend
        svg += f'    <rect x="0" y="{y_pos}" width="50" height="30" rx="6" class="key-empty"/>\n'
        svg += f'    <text x="60" y="{y_pos + 20}" class="legend">Transparent key (passes through to lower layer)</text>\n'

        svg += "  </g>\n\n"
        return svg

    def generate(self, output_path: str = "keyboard.svg") -> None:
        """Generate complete SVG visualization."""
        self.load_config()

        num_layers = self.config["layout"]["layers"]

        # Build key position maps for all layers
        for layer_idx in range(num_layers):
            self.build_key_position_map(layer_idx)

        # Calculate dimensions
        layer_height = 350
        legend_height = 400
        total_height = 50 + (num_layers * layer_height) + legend_height
        total_width = 1600

        # Start building SVG
        svg = self.generate_svg_header(total_width, total_height)

        # Generate each layer
        for layer_idx in range(num_layers):
            y_offset = 50 + (layer_idx * layer_height)
            svg += self.generate_layer(layer_idx, y_offset)

        # Generate legend
        legend_offset = 50 + (num_layers * layer_height)
        svg += self.generate_legend(legend_offset)

        # Footer
        svg += "  <!-- Footer -->\n"
        svg += f'  <text x="{total_width - 50}" y="{total_height - 50}" class="legend" text-anchor="end">'
        svg += "Generated from keyboard.toml and vial.json</text>\n"

        # Close SVG
        svg += "</svg>\n"

        # Write to file
        output_file = Path(output_path)
        output_file.write_text(svg)
        print(f"✓ Generated {output_path}")
        print(f"  - Keyboard: {self.config['keyboard']['name']}")
        print(f"  - Layers: {num_layers}")
        print(f"  - Layer names: {dict(self.layer_names)}")
        print(f"  - Dimensions: {total_width}x{total_height}")


def main():
    """Main entry point."""
    import sys

    # Parse arguments
    toml_path = "keyboard.toml"
    json_path = "vial.json"
    output_path = "keyboard.svg"

    if len(sys.argv) > 1:
        toml_path = sys.argv[1]
    if len(sys.argv) > 2:
        json_path = sys.argv[2]
    if len(sys.argv) > 3:
        output_path = sys.argv[3]

    # Generate
    generator = KeyboardLayoutGenerator(toml_path, json_path)
    try:
        generator.generate(output_path)
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print(f"\nUsage: {sys.argv[0]} [keyboard.toml] [vial.json] [output.svg]")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error generating SVG: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
