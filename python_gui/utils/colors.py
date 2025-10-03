"""
Color scheme matching the React app's dark theme with yellow accents
"""

# Main colors
BG_PRIMARY = "#1c1c1c"  # Main background
BG_SECONDARY = "#2a2a2a"  # Cards and sections
BG_DARK = "#121212"  # Darker sections

# Yellow accent
YELLOW_PRIMARY = "#f59e0b"  # Yellow-500
YELLOW_HOVER = "#fbbf24"  # Yellow-400
YELLOW_DARK = "#d97706"  # Yellow-600

# Text colors
TEXT_WHITE = "#ffffff"
TEXT_GRAY_300 = "#d1d5db"
TEXT_GRAY_400 = "#9ca3af"
TEXT_GRAY_500 = "#6b7280"
TEXT_GRAY_600 = "#4b5563"

# Border and line colors
BORDER_GRAY = "#4b5563"
BORDER_GRAY_LIGHT = "#6b7280"

# Status colors
GREEN_SUCCESS = "#10b981"
RED_ERROR = "#ef4444"
BLUE_INFO = "#3b82f6"

# Hover and active states
HOVER_GRAY = "#374151"
ACTIVE_BG = "#1f2937"

# Opacity for overlays
BLACK_OVERLAY = "#000000"
OVERLAY_ALPHA = 0.7

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)
