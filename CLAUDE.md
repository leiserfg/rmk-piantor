# Claude Development Rules for RMK Piantor Project

## Workflow Rules

### 1. Always Verify Changes
After making ANY change to `keyboard.toml` or the `generate_keyboard_svg.py` script:
1. Run `cargo check` to verify the keyboard configuration is valid
2. Run `python3 generate_keyboard_svg.py` to regenerate the SVG
3. Open the SVG in Firefox: `firefox keyboard.svg &`

**Command sequence:**
```bash
cd /home/leiserfg/projects/rmk-piantor && cargo check 2>&1 | head -50
cd /home/leiserfg/projects/rmk-piantor && python3 generate_keyboard_svg.py && firefox keyboard.svg &
```

### 2. Combo Symbol Mapping
In RMK keyboard configs, some symbols require SHIFTED() because they are uppercase on regular keyboards:

- `(` = `SHIFTED(9)`
- `)` = `SHIFTED(0)`
- `{` = `SHIFTED([)`
- `}` = `SHIFTED(])`
- `!` = `SHIFTED(1)`
- `@` = `SHIFTED(2)`
- `#` = `SHIFTED(3)`
- `$` = `SHIFTED(4)`
- `%` = `SHIFTED(5)`
- `^` = `SHIFTED(6)`
- `&` = `SHIFTED(7)`
- `*` = `SHIFTED(8)`
- `_` = `SHIFTED(-)`
- `+` = `SHIFTED(=)`
- `:` = `SHIFTED(;)`
- `"` = `SHIFTED(')`
- `<` = `SHIFTED(,)`
- `>` = `SHIFTED(.)`
- `?` = `SHIFTED(/)`
- `~` = `SHIFTED(\`)`
- `|` = `SHIFTED(\\)`

**Important:** The SVG script automatically displays the actual symbol (e.g., `(`) instead of the notation (e.g., `SHIFTED(9)`).

### 3. XML Escaping in SVG
The `generate_keyboard_svg.py` script must escape XML special characters when outputting text:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&apos;`

This is handled by the `escape_xml()` method.

### 4. Combo Configuration Limits
When adding combos, you may need to increase `combo_max_num` in `keyboard.toml`:
```toml
[rmk]
debounce_time=50
combo_max_num=30  # Increase as needed
```

### 5. Mod-Tap Key References
When referencing mod-tap keys in combos, use the full MT() notation:
- `MT(N, LGui)` not just `N`
- `MT(R, LAlt)` not just `R`
- `MT(T, LShift)` not just `T`
- etc.

## Current Combo Styling

Combos are visualized with:
- **Color:** Dark blue (#003366 fill, #001a33 stroke)
- **Text:** White, bold, 11px font
- **Size:** 28x28 for rectangular overlays, radius 15 for circles
- **Rounded corners:** rx: 6

### Contiguous vs Non-Contiguous
- **Contiguous keys** (adjacent): Small overlay rectangle between keys
- **Non-contiguous keys** (separated): Connection lines with circle at midpoint

## Key Layout Reference

```
Base Layer (Layer 0):
Row 1: tab  B    L    D    C    V    J    Y    O    U    ,    bspc
Row 2: esc  N/Gui R/Alt T/Sft S/Ctl G    P    H/Ctl A/Sft E/Alt I/Gui ent
Row 3: _    X    Q    M    W    Z    K    F    '    ;    .    Del
Row 4: _    _    _    A    spc  lsft RAlt ent  A    _    _    _
```

## Project Structure

- `keyboard.toml` - Main keyboard configuration
- `vial.json` - Vial configuration (not heavily used)
- `generate_keyboard_svg.py` - Python script to generate visual layout
- `keyboard.svg` - Generated SVG output (regenerated on every change)

## Common Tasks

### Adding a New Combo
1. Add to `[behavior.combo]` section in `keyboard.toml`
2. Use proper SHIFTED() notation for symbols
3. Reference mod-tap keys with full MT() notation
4. Increase `combo_max_num` if needed
5. Run verification workflow

### Updating Combo Visuals
1. Edit `generate_keyboard_svg.py`
2. Modify styles in `generate_svg_header()` method
3. Adjust sizes/colors in `generate_combo_visual()` method
4. Run verification workflow
