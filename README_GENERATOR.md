# Keyboard Layout SVG Generator

Automatically generates a visual SVG representation of your keyboard layout from `keyboard.toml` and `vial.json` configuration files.

## Features

- **Multi-layer visualization**: Shows all keyboard layers with different colors
- **Transparent keys**: Empty/transparent keys shown with dashed borders and "—" symbol
- **Mod-tap support**: Properly formats MT() keys (e.g., "N/Gui" for tap-N-hold-GUI)
- **Color-coded layers**: Each layer has a distinct color for easy identification
- **Rounded corners**: Keys have rounded corners (rx: 6) for a modern look
- **Legend**: Includes keyboard info, combos, and color legend
- **Split layout support**: Designed for split 3×6+3 keyboards (like Piantor)

## Usage

### Basic usage:
```bash
./generate_keyboard_svg.py
```

This will read `keyboard.toml` and `vial.json` from the current directory and generate `keyboard.svg`.

### Custom paths:
```bash
./generate_keyboard_svg.py [keyboard.toml] [vial.json] [output.svg]
```

Example:
```bash
./generate_keyboard_svg.py config/kb.toml config/vial.json output/layout.svg
```

## Output

The generated SVG includes:
- **All layers** defined in keyboard.toml
- **Layer names** with descriptive titles
- **Key labels** with proper formatting
- **Combo information** from the config
- **Color legend** explaining each layer

## Layer Colors

- Layer 0 (Base): Light gray (#f0f0f0)
- Layer 1 (Numbers): Light blue (#e8f4f8)
- Layer 2 (Functions): Light orange (#fff4e8)
- Layer 3 (Navigation): Light purple (#f0e8ff)
- Layer 4 (Custom): Light pink (#f8e8f0)
- Transparent keys: Dashed border with light gray fill

## Requirements

- Python 3.11+ (uses `tomllib` for TOML parsing)
- No external dependencies (uses only standard library)

## Key Formatting

The script intelligently formats key labels:
- **Mod-tap keys**: `MT(N, LGui)` → "N/Gui"
- **Shifted keys**: `SHIFTED(Tab)` → "S-Tab"
- **Common keys**: Uppercase for visibility (tab → TAB, esc → ESC)
- **Special keys**: Short names (volu → VOL+, mprv → PREV)
- **Long labels**: Automatically use smaller font

## Example

```bash
./generate_keyboard_svg.py
# ✓ Generated keyboard.svg
#   - Keyboard: Piantor
#   - Layers: 5
#   - Dimensions: 1600x2200
```

View the generated SVG in any web browser or SVG-compatible application.
