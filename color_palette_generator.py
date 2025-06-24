import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB values (0-255)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """Convert RGB values (0-255) to hex color"""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def rgb_to_hsl(r, g, b):
    """Convert RGB (0-255) to HSL (H: 0-360, S: 0-100, L: 0-100)"""
    r, g, b = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h*360, s*100, l*100

def hsl_to_rgb(h, s, l):
    """Convert HSL (H: 0-360, S: 0-100, L: 0-100) to RGB (0-255)"""
    h, s, l = h/360.0, s/100.0, l/100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return r*255, g*255, b*255

def generate_color_palette(primary_hex, palette_name="color"):
    """
    Generate a 19-color palette from a primary color (550 variant)
    
    Args:
        primary_hex (str): Primary color in hex format (e.g., "#2f7d30")
        palette_name (str): Name prefix for the color variables
    
    Returns:
        dict: Dictionary with color names as keys and hex values as values
    """
    
    # Convert primary color to HSL
    primary_rgb = hex_to_rgb(primary_hex)
    primary_h, primary_s, primary_l = rgb_to_hsl(*primary_rgb)
    
    # Define the color variants and their lightness values
    # These are based on typical color scale progressions
    color_variants = [
        ("950", 8),   # Very dark
        ("900", 12),  # Dark
        ("850", 16),  # 
        ("800", 20),  #
        ("750", 24),  #
        ("700", 28),  #
        ("650", 32),  #
        ("600", 36),  #
        ("550", 40),  # Primary color (reference point)
        ("500", 48),  #
        ("450", 56),  #
        ("400", 64),  #
        ("350", 72),  #
        ("300", 80),  #
        ("250", 85),  #
        ("200", 88),  # Reduced from 90
        ("150", 91),  # Reduced from 94
        ("100", 94),  # Reduced from 97
        ("50", 97),   # Reduced from 99
    ]
    
    # Find the primary color position (550)
    primary_index = next(i for i, (variant, _) in enumerate(color_variants) if variant == "550")
    primary_target_lightness = color_variants[primary_index][1]
    
    # Calculate the lightness adjustment factor
    # This ensures the primary color matches the input color's lightness
    lightness_adjustment = primary_l - primary_target_lightness
    
    # Generate the color palette
    palette = {}
    
    for variant, base_lightness in color_variants:
        # IMPORTANT: Use the exact primary color for the 550 variant
        if variant == "550":
            palette[f"{palette_name}-{variant}"] = primary_hex.upper()
            continue
            
        # Adjust lightness based on the primary color
        adjusted_lightness = base_lightness + lightness_adjustment
        
        # Clamp lightness to valid range (0-100)
        adjusted_lightness = max(0, min(100, adjusted_lightness))
        
        # For very dark colors (950-800), reduce saturation slightly for better contrast
        if int(variant) >= 800:
            adjusted_saturation = primary_s * 0.8
        # For very light colors (200-50), use more aggressive saturation and lightness limits
        elif int(variant) <= 200:
            # More aggressive saturation reduction for very light colors
            if int(variant) <= 50:
                saturation_factor = 0.1  # Very low saturation for near-white colors
                # Cap the lightness to prevent pure white
                adjusted_lightness = min(adjusted_lightness, 97)
            elif int(variant) <= 100:
                saturation_factor = 0.15
                adjusted_lightness = min(adjusted_lightness, 94)
            elif int(variant) <= 150:
                saturation_factor = 0.25
                adjusted_lightness = min(adjusted_lightness, 91)
            else:  # 200
                saturation_factor = 0.35
                adjusted_lightness = min(adjusted_lightness, 88)
            adjusted_saturation = primary_s * saturation_factor
        else:
            adjusted_saturation = primary_s
        
        # Convert back to RGB and then to hex
        r, g, b = hsl_to_rgb(primary_h, adjusted_saturation, adjusted_lightness)
        hex_color = rgb_to_hex(r, g, b)
        
        palette[f"{palette_name}-{variant}"] = hex_color
    
    return palette

def print_scss_variables(palette):
    """Print the palette as SCSS variables"""
    print("// Generated color palette:")
    for color_name, hex_value in palette.items():
        print(f"${color_name}: {hex_value};")

def print_css_variables(palette):
    """Print the palette as CSS custom properties"""
    print("/* Generated color palette */")
    print(":root {")
    for color_name, hex_value in palette.items():
        css_name = color_name.replace("-", "-")
        print(f"  --{css_name}: {hex_value};")
    print("}")

def get_contrast_color(hex_color):
    """Get white or black text color based on background for better contrast"""
    r, g, b = hex_to_rgb(hex_color)
    # Calculate luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#000000" if luminance > 0.5 else "#ffffff"

def generate_html_palette(palette, palette_name, filename="palette.html"):
    """Generate an HTML file showing the color palette"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{palette_name.title()} Color Palette</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 18px;
        }}
        .palette-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .color-item {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .color-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .color-square {{
            width: 100%;
            height: 120px;
            cursor: pointer;
            position: relative;
            transition: all 0.2s ease;
        }}
        .color-square:hover {{
            transform: scale(1.02);
        }}
        .color-label {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: 600;
            font-size: 16px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
            pointer-events: none;
        }}
        .color-info {{
            padding: 20px;
        }}
        .color-name {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin: 0 0 8px 0;
        }}
        .color-hex {{
            font-size: 16px;
            font-family: 'Courier New', monospace;
            color: #666;
            background: #f8f9fa;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid #e9ecef;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .color-hex:hover {{
            background: #e9ecef;
            color: #333;
        }}
        .copy-feedback {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: 500;
            opacity: 0;
            transform: translateY(-20px);
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        .copy-feedback.show {{
            opacity: 1;
            transform: translateY(0);
        }}
        .primary-indicator {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255,255,255,0.9);
            color: #333;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        .scss-variables {{
            max-width: 1200px;
            margin: 40px auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .scss-header {{
            background: #2d3748;
            color: white;
            padding: 20px;
            font-weight: 600;
            font-size: 18px;
        }}
        .scss-content {{
            padding: 20px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.8;
            background: #f8f9fa;
            color: #333;
            white-space: pre-line;
            max-height: 400px;
            overflow-y: auto;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Pico CSS Color Palette - {palette_name.title()}</h1>
        <p>Click on any color square or hex code to copy to clipboard</p>
    </div>
    
    <div class="palette-container">
"""

    # Sort palette by variant number for proper display order
    sorted_palette = dict(sorted(palette.items(), key=lambda x: int(x[0].split('-')[1]), reverse=True))
    
    for color_name, hex_value in sorted_palette.items():
        variant = color_name.split('-')[1]
        text_color = get_contrast_color(hex_value)
        is_primary = variant == "550"
        
        html_content += f"""        <div class="color-item">
            <div class="color-square" style="background-color: {hex_value};" onclick="copyToClipboard('{hex_value}')">
                <div class="color-label" style="color: {text_color};">{variant}</div>
                {f'<div class="primary-indicator">PRIMARY</div>' if is_primary else ''}
            </div>
            <div class="color-info">
                <div class="color-name">${color_name}</div>
                <div class="color-hex" onclick="copyToClipboard('{hex_value}')">{hex_value.upper()}</div>
            </div>
        </div>
"""

    # Generate SCSS variables section
    scss_variables = ""
    for color_name, hex_value in sorted_palette.items():
        scss_variables += f"${color_name}: {hex_value};\n"

    html_content += f"""    </div>
    
    <div class="scss-variables">
        <div class="scss-header">
            SCSS Variables
        </div>
        <div class="scss-content">{scss_variables}</div>
    </div>
    
    <div class="copy-feedback" id="copyFeedback">
        Color copied to clipboard!
    </div>

    <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                showCopyFeedback();
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        
        function showCopyFeedback() {{
            const feedback = document.getElementById('copyFeedback');
            feedback.classList.add('show');
            setTimeout(() => {{
                feedback.classList.remove('show');
            }}, 2000);
        }}
    </script>
</body>
</html>"""

    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML palette saved to: {filename}")

# Example usage
if __name__ == "__main__":
    import sys
    
    def print_usage():
        print("Usage: python color_palette_generator.py --palette-name NAME --primary-color HEX")
        print("  --palette-name NAME   Name for the color palette (e.g., 'tracim', 'blue')")
        print("  --primary-color HEX   Primary color in hex format (e.g., '#2f7d30', '#0a7ce6')")
        print("\nExample:")
        print("  python color_palette_generator.py --palette-name tracim --primary-color '#2f7d30'")
        print("  python color_palette_generator.py --palette-name blue --primary-color '#0a7ce6'")
    
    # Parse command line arguments manually (no external dependencies)
    args = sys.argv[1:]  # Skip script name
    
    if len(args) == 0 or '--help' in args or '-h' in args:
        print_usage()
        sys.exit(0)
    
    # Initialize variables
    palette_name = None
    primary_color = None
    
    # Parse arguments
    i = 0
    while i < len(args):
        if args[i] == '--palette-name' and i + 1 < len(args):
            palette_name = args[i + 1]
            i += 2
        elif args[i] == '--primary-color' and i + 1 < len(args):
            primary_color = args[i + 1]
            i += 2
        else:
            print(f"Error: Unknown argument '{args[i]}'")
            print_usage()
            sys.exit(1)
    
    # Validate required arguments
    if palette_name is None:
        print("Error: --palette-name is required")
        print_usage()
        sys.exit(1)
    
    if primary_color is None:
        print("Error: --primary-color is required")
        print_usage()
        sys.exit(1)
    
    # Validate hex color format
    if not primary_color.startswith('#') or len(primary_color) != 7:
        print(f"Error: Primary color must be in hex format (e.g., '#2f7d30'), got: {primary_color}")
        sys.exit(1)
    
    try:
        # Test if it's a valid hex color
        int(primary_color[1:], 16)
    except ValueError:
        print(f"Error: Invalid hex color format: {primary_color}")
        sys.exit(1)
    
    # Validate palette name (alphanumeric and underscores/hyphens only)
    if not palette_name.replace('-', '').replace('_', '').isalnum():
        print(f"Error: Palette name must contain only letters, numbers, hyphens, and underscores: {palette_name}")
        sys.exit(1)
    
    print(f"Generating palette '{palette_name}' with primary color {primary_color}")
    print("=" * 60)
    
    # Generate the palette
    palette = generate_color_palette(primary_color, palette_name)
    
    print("\nSCSS Variables:")
    print_scss_variables(palette)
    
    print("\n" + "="*50 + "\n")
    
    print("CSS Variables:")
    print_css_variables(palette)
    
    print("\n" + "="*50 + "\n")
    
    # Generate HTML palette
    html_filename = f"{palette_name}_palette.html"
    generate_html_palette(palette, palette_name, html_filename)
    
    print("✅ HTML palette generated successfully!")
    print(f"📁 Open '{html_filename}' in your browser to view the palette")
    
    print(f"\n🎨 Generated {len(palette)} colors for the '{palette_name}' palette")
    print(f"🎯 Primary color: {primary_color}")
    
    # Optional: Generate additional palettes with different colors
    # Uncomment the lines below to generate example palettes with other colors
    
    # print("Example with a red primary color:")
    # red_palette = generate_color_palette("#e74c3c", "red")
    # generate_html_palette(red_palette, "red", "red_palette.html")
