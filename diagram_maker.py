import math
import xml.etree.ElementTree as ET
from rps import rps, options, option_icons

# Set colors for each option
colors = ["#008000",
          "#ffff00",
          "#ffa500",
          "#808000",
          "#800000",
          "#00ff00",
          "#a52a2a",
          "#fa8072",
          "#800080",
          "#87ceeb",
          "#0000ff",
          "#ff0000",
          "#ff00ff",
          "#dda0dd",
          "#808080",
          ]

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

# Calculate the center position and inner position of each icon
N = len(option_icons)
threshold = N // 2
spacing_ang = 2 * math.pi / N
positions = []
# inner_positions = []
for i in range(N):
    angle = math.pi / 2 + spacing_ang * (threshold - i)
    x = outer_rad * math.cos(angle)
    y = outer_rad * math.sin(angle)
    positions.append((x, y))
    x_in = inner_rad * math.cos(angle)
    y_in = inner_rad * math.sin(angle)
    # inner_positions.append((x, y))

# Draw the connection arrows
for (x, y), option, color in zip(positions, options, colors):
    for (x_end, y_end), opponent in zip(positions, options):
        if rps(option, opponent) == option:
            angle = math.atan2(y-y_end, x-x_end)
            x_ah = x_end + (icon_rad + ah_h) * math.cos(angle)
            y_ah = y_end + (icon_rad + ah_h) * math.sin(angle)
            ET.SubElement(root, "path", {"d": f"M {x} {y} L {x_ah} {y_ah}",
                                         "stroke": color,
                                         "data-option": option,
                                         })
            x_con = x_end + icon_rad * math.cos(angle)
            y_con = y_end + icon_rad * math.sin(angle)
            ah_edge_1 = f"{ah_h * math.cos(angle) + ah_w/2 * math.sin(angle) + x_con} {ah_h * math.sin(angle) - ah_w/2 * math.cos(angle) + y_con}"
            ah_edge_2 = f"{ah_h * math.cos(angle) - ah_w/2 * math.sin(angle) + x_con} {ah_h * math.sin(angle) + ah_w/2 * math.cos(angle) + y_con}"
            ET.SubElement(root, "path", {"d": f"M {x_con} {y_con} L {ah_edge_1} L {ah_edge_2} Z",
                                         "fill": color,
                                         "data-option": option,
                                         })

# Draw the icon for each option
for (x, y), option, emoji, color in zip(positions, options, option_icons, colors):
    ET.SubElement(root, "circle", {"r": str(icon_rad),
                                   "cx": str(x),
                                   "cy": str(y),
                                   "fill": color,
                                   "stroke": "black",
                                   "data-option": option,
                                   })
    txt = ET.SubElement(root, "text", {"x": str(x),
                                       "y": str(y + shift_down),
                                       "text-anchor": "middle",
                                       "dominant-baseline": "middle",
                                       "data-option": option,
                                       "font-size": str(font_size),
                                       })
    txt.text = emoji

# Save the svg file
fname = "media/rps-move-diagram.svg"
tree = ET.ElementTree(root)
tree.write(fname, "utf-8")
