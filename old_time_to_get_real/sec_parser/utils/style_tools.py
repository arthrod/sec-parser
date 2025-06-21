"""CSS Style Processing Tools
Robust CSS reading with units, inheritance, classes, graceful fallback.
"""

import re
from functools import lru_cache

# Optional cssutils for better CSS parsing
try:
    import cssutils
    cssutils.log.setLevel(60)  # Suppress warnings
    _USE_CSSUTILS = True
except ImportError:
    _USE_CSSUTILS = False

# CSS unit conversion regex
_UNIT_RE = re.compile(r"([0-9.]+)\s*(pt|px|em|rem|%)", re.IGNORECASE)


def _to_pt(value: str, base_pt: float = 12.0) -> float:
    """Convert CSS length to points. Supports pt, px, em, rem, %.
    If unitless -> assume pt. Graceful fallback = 0.
    """
    if not value:
        return 0.0

    # Handle unitless numbers (assume pt)
    try:
        return float(value)
    except ValueError:
        pass

    m = _UNIT_RE.search(value)
    if not m:
        return 0.0

    try:
        num, unit = float(m.group(1)), m.group(2).lower()
        if unit == "pt":
            return num
        if unit == "px":
            return num * 0.75  # 96 dpi assumption
        if unit in {"em", "rem"}:
            return num * base_pt
        if unit == "%":
            return num * base_pt / 100.0
    except (ValueError, IndexError):
        pass

    return 0.0


@lru_cache(maxsize=1024)
def inline_style_dict(style_string: str) -> dict[str, str]:
    """Return a dict of CSS properties. Tiny, safe, no crash.
    If cssutils is present we use it – otherwise fall back to regex.
    """
    if not style_string:
        return {}

    out = {}

    if _USE_CSSUTILS:
        try:
            style = cssutils.parseStyle(style_string)
            out = {prop.name.lower(): prop.value for prop in style}
        except Exception:
            # Fallback to regex parsing
            pass

    # Regex fallback (or if cssutils unavailable)
    if not out:
        try:
            for part in style_string.split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    out[k.strip().lower()] = v.strip()
        except Exception:
            pass

    return out


def computed_style(bs4_node) -> dict[str, str]:
    """Merge inline + class-based rules (only those actually *used* in SEC
    filings: font-weight, font-size, margin-left/top, text-align).
    Cheap: look at class names on ancestors; we do *not* parse the whole
    <style> sheet.
    """
    props = {}
    node = bs4_node
    depth = 0

    while node and depth < 3:  # inheritance: at most 3 hops
        if isinstance(node, str):
            break

        try:
            # Get inline styles
            style_attr = node.get("style", "") if hasattr(node, "get") else ""
            node_props = inline_style_dict(style_attr)

            # Add only new properties (child overrides parent)
            for k, v in node_props.items():
                if k not in props:
                    props[k] = v

            # Naïve class rule: check style tags of form ".cls{prop:val}"
            if hasattr(node, "get") and hasattr(node, "has_attr"):
                classes = node.get("class", []) if node.has_attr("class") else []
                if isinstance(classes, str):
                    classes = classes.split()

                for cls in classes[:3]:  # speed: first 3 classes max
                    try:
                        rule_re = re.compile(rf"\.{re.escape(cls)}\s*\{{([^}}]+)\}}", re.IGNORECASE | re.DOTALL)
                        # Look for style tags in document
                        if hasattr(node, "find_all_previous"):
                            for style_tag in node.find_all_previous("style", limit=2):
                                try:
                                    m = rule_re.search(style_tag.get_text())
                                    if m:
                                        class_props = inline_style_dict(m.group(1))
                                        for k, v in class_props.items():
                                            if k not in props:
                                                props[k] = v
                                except Exception:
                                    continue
                    except Exception:
                        continue

            # Move to parent
            node = getattr(node, "parent", None)
            depth += 1

        except Exception:
            break

    return props


def is_bold(style_dict: dict[str, str]) -> bool:
    """Check if element is bold based on font-weight."""
    font_weight = style_dict.get("font-weight", "").lower()
    return font_weight in {"bold", "700", "800", "900", "bolder"}


def is_centered(style_dict: dict[str, str]) -> bool:
    """Check if element is centered based on text-align."""
    text_align = style_dict.get("text-align", "").lower()
    return text_align == "center"


def get_font_size_pt(style_dict: dict[str, str], base_pt: float = 12.0) -> float:
    """Get font size in points."""
    font_size = style_dict.get("font-size", "")
    return _to_pt(font_size, base_pt)


def get_margin_top_pt(style_dict: dict[str, str]) -> float:
    """Get top margin in points."""
    margin_top = style_dict.get("margin-top", "")
    return _to_pt(margin_top)


def get_margin_left_pt(style_dict: dict[str, str]) -> float:
    """Get left margin in points."""
    margin_left = style_dict.get("margin-left", "")
    return _to_pt(margin_left)
