import math
import xml.etree.ElementTree as ET
from rps import rps, options, option_icons

# Set colors for each option
colors = ["#00ff00",
          "#ffff00",
          "#f0f0f0",
          "#808000",
          "#800000",
          "#3cb371",
          "#a52a2a",
          "#fa8072",
          "#ff00ff",
          "#87ceeb",
          "#0000ff",
          "#ff0000",
          "#800080",
          "#dda0dd",
          "#808080",
          ]

# Swap out some option_icons
option_icons[4] = "😃"

# Set various dimensions
ax_len = 220
icon_rad = 15
outer_rad = 200
inner_rad = outer_rad - icon_rad
font_size = 19
shift_down = 2
ah_w = 4
ah_h = 5

# Create the root svg element
# (0, 0) is at the center of the square
root = ET.Element("svg", {"version": "1.1",
                          "viewBox": f"-{ax_len} -{ax_len} {2 * ax_len} {2 * ax_len}",
                          "xmlns": "http://www.w3.org/2000/svg",
                          })

# Add a style element for some css hover effects and a custom font
css_base = """
/*
EmojiSymbols Font (c)blockworks - Kenichi Kaneko
http://emojisymbols.com/
*/
@font-face {
  font-family: 'EmojiSymbols';
  src: url(https://raw.githubusercontent.com/VinEdw/rps-discord-bot/master/font/EmojiSymbols-Regular.woff) format("woff");
  font-weight: normal;
  font-style: normal;
}
"""
css_template = """
circle[data-option="{option}"]:hover ~ path[data-option="{option}"] {{
    stroke-width: 3;
}}
text[data-option="{option}"]:hover ~ path[data-option="{option}"] {{
    stroke-width: 3;
}}
"""
style = ET.SubElement(root, "style")
style.text = css_base + "".join([css_template.format(option=option) for option in options])

# Add a background box
ET.SubElement(root, "rect", {"x": str(-ax_len),
                             "y": str(-ax_len),
                             "width": str(2 * ax_len),
                             "height": str(2 * ax_len),
                             "fill": "#0d1117",
                             })

# Calculate the center position and inner position of each icon
N = len(option_icons)
threshold = N // 2
spacing_ang = 2 * math.pi / N
positions = []
for i in range(N):
    angle = math.pi / 2 + spacing_ang * (threshold - i)
    x = outer_rad * math.cos(angle)
    y = outer_rad * math.sin(angle)
    positions.append((x, y))

# Draw the icon for each option
for (x, y), option, emoji, color in zip(positions, options, option_icons, colors):
    # Draw the circle
    ET.SubElement(root, "circle", {"r": str(icon_rad),
                                   "cx": str(x),
                                   "cy": str(y),
                                   "fill": color,
                                   "stroke": "black",
                                   "data-option": option,
                                   })
    # Draw the emoji on top of the circle
    txt = ET.SubElement(root, "text", {"x": str(x),
                                       "y": str(y + shift_down),
                                       "text-anchor": "middle",
                                       "dominant-baseline": "middle",
                                       "data-option": option,
                                       "font-size": str(font_size),
                                       "font-family": "EmojiSymbols",
                                       "filter": "grayscale(1) brightness(0.2)",
                                       })
    txt.text = emoji

# Draw the connection arrows
for (x, y), option, color in zip(positions, options, colors):
    for (x_end, y_end), opponent in zip(positions, options):
        if rps(option, opponent) == option:
            angle = math.atan2(y-y_end, x-x_end)
            # Calculate the position on the surface of the starting circle
            x_sur = x - icon_rad * math.cos(angle)
            y_sur = y - icon_rad * math.sin(angle)
            # Calculate the position where the line transitions into the arrowhead
            x_ah = x_end + (icon_rad + ah_h) * math.cos(angle)
            y_ah = y_end + (icon_rad + ah_h) * math.sin(angle)
            # Draw the line
            ET.SubElement(root, "path", {"d": f"M {x_sur} {y_sur} L {x_ah} {y_ah}",
                                         "stroke": color,
                                         "data-option": option,
                                         })
            # Calculate the position where the arrow contacts the surface of the ending circle
            x_con = x_end + icon_rad * math.cos(angle)
            y_con = y_end + icon_rad * math.sin(angle)
            # Calculate the positions of the edges of the arrowhead
            ah_edge_1 = f"{ah_h * math.cos(angle) + ah_w/2 * math.sin(angle) + x_con} {ah_h * math.sin(angle) - ah_w/2 * math.cos(angle) + y_con}"
            ah_edge_2 = f"{ah_h * math.cos(angle) - ah_w/2 * math.sin(angle) + x_con} {ah_h * math.sin(angle) + ah_w/2 * math.cos(angle) + y_con}"
            # Draw the arrowhead
            ET.SubElement(root, "path", {"d": f"M {x_con} {y_con} L {ah_edge_1} L {ah_edge_2} Z",
                                         "fill": color,
                                         "data-option": option,
                                         })

# Save the svg file
fname = "media/rps-move-diagram.svg"
tree = ET.ElementTree(root)
tree.write(fname, "utf-8")
