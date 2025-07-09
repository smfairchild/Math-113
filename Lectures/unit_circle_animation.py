import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arc
from pyscript import display # Import display for PyScript output

# --- Setup the plot ---
# Increased figure width significantly to provide ample space for both components
fig = plt.figure(figsize=(20, 10))

# Manually add axes to control its position (left, bottom, width, height)
# Values are fractions of the figure width/height (0 to 1)
# This positions the unit circle to the left side of the figure
ax = fig.add_axes([0.08, 0.1, 0.40, 0.8]) # left: 8%, bottom: 10%, width: 40%, height: 80%

ax.set_xlim(-1.2, 1.2) # Keep original x-limits for the circle itself
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal', adjustable='box')
ax.grid(True, linestyle='--', alpha=0.6)

# Remove spines and ticks for a cleaner unit circle look
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xticks([-1, -0.5, 0.5, 1])
ax.set_yticks([-1, -0.5, 0.5, 1])

# Draw the unit circle (static)
circle = plt.Circle((0, 0), 1, color='blue', fill=False, linewidth=2, alpha=0.7)
ax.add_patch(circle)

# Add origin label
ax.text(0.05, 0.05, 'O', verticalalignment='bottom', horizontalalignment='left', fontsize=12)

# Add cardinal points (0,1), (-1,0), (0,-1), (1,0) (Static)
cardinal_points_data = [
    (1, 0, '1,0'),
    (0, 1, '0,1'),
    (-1, 0, '-1,0'),
    (0, -1, '0,-1')
]
for x, y, label_coords in cardinal_points_data:
    ax.plot(x, y, 'ko', markersize=5) # 'ko' for black circle markers
    # Adjust label positions slightly for better readability
    if x == 1:
        ax.text(x + 0.05, y, f'({label_coords})', fontsize=10, ha='left', va='center')
    elif x == -1:
        ax.text(x - 0.05, y, f'({label_coords})', fontsize=10, ha='right', va='center')
    elif y == 1:
        ax.text(x, y + 0.05, f'({label_coords})', fontsize=10, ha='center', va='bottom')
    elif y == -1:
        ax.text(x, y - 0.05, f'({label_coords})', fontsize=10, ha='center', va='top')

# --- Define Angles and Coordinates ---
angles_rad = {
    r'$\frac{\pi}{6}$': np.pi / 6,
    r'$\frac{\pi}{4}$': np.pi / 4,
    r'$\frac{\pi}{3}$': np.pi / 3
}

angle_lines = []
angle_labels = []
point_labels = []
points = []
angle_arcs = [] # List to store the angle arc patches

# --- Initialize elements for animation (initially hidden or empty) ---
# For pi/6 triangle
triangle_lines = []
hypotenuse_label = ax.text(0, 0, '', fontsize=10, color='purple', ha='center', va='bottom')
opposite_label = ax.text(0, 0, '', fontsize=10, color='green', ha='left', va='center')
adjacent_label = ax.text(0, 0, '', fontsize=10, color='red', ha='center', va='top')

# For formula box - Using fig.text for absolute positioning relative to figure
# Adjusted x to 0.65, which should be well to the right of the now-left-shifted ax
formula_box_text = fig.text(0.65, 0.88, '',
                           bbox=dict(boxstyle="round,pad=0.5", fc="yellow", ec="k", lw=1, alpha=0.8),
                           fontsize=12, verticalalignment='top', horizontalalignment='left')

# --- Animation Initialization Function ---
def init():
    # Hide all angle-related elements initially
    for line in angle_lines:
        line.set_visible(False)
    for label in angle_labels:
        label.set_visible(False)
    for label in point_labels:
        label.set_visible(False)
    for point in points:
        point.set_visible(False)
    for arc in angle_arcs: # Hide the newly added arcs
        arc.set_visible(False)

    # Hide triangle and formula box initially
    for line in triangle_lines:
        line.set_visible(False)
    hypotenuse_label.set_text('')
    hypotenuse_label.set_visible(False) # Ensure labels are hidden
    opposite_label.set_text('')
    opposite_label.set_visible(False)
    adjacent_label.set_text('')
    adjacent_label.set_visible(False)

    formula_box_text.set_text('')
    formula_box_text.set_visible(False)

    # Return all artists that were modified
    return angle_lines + angle_labels + point_labels + points + angle_arcs + \
           triangle_lines + [hypotenuse_label, opposite_label, adjacent_label, formula_box_text]

# --- Animation Function ---
def animate(frame):
    # Frame 0: Unit circle and cardinal points are already static

    # Frames 1-3: Show angles, points, and angle arcs with distinct radii
    if frame == 1: # pi/6
        theta = angles_rad[r'$\frac{\pi}{6}$']
        x, y = np.cos(theta), np.sin(theta)
        line, = ax.plot([0, x], [0, y], 'r--', alpha=0.7)
        angle_lines.append(line)
        label = ax.text(x * 0.5, y * 0.5 + 0.05, r'$\frac{\pi}{6}$', color='red', fontsize=12)
        angle_labels.append(label)
        point, = ax.plot(x, y, 'ro', markersize=6)
        points.append(point)
        point_label = ax.text(x + 0.05, y + 0.05, r'$\left(\frac{\sqrt{3}}{2}, \frac{1}{2}\right)$', fontsize=10)
        point_labels.append(point_label)

        # Add arc for pi/6 (radius 0.3)
        arc = Arc((0, 0), 0.3, 0.3, angle=0, theta1=0, theta2=np.degrees(theta), color='red', linewidth=1.5, alpha=0.8)
        ax.add_patch(arc)
        angle_arcs.append(arc)

        line.set_visible(True)
        label.set_visible(True)
        point.set_visible(True)
        point_label.set_visible(True)
        arc.set_visible(True)

    elif frame == 2: # pi/4
        theta = angles_rad[r'$\frac{\pi}{4}$']
        x, y = np.cos(theta), np.sin(theta)
        line, = ax.plot([0, x], [0, y], 'g--', alpha=0.7)
        angle_lines.append(line)
        label = ax.text(x * 0.5, y * 0.5 + 0.05, r'$\frac{\pi}{4}$', color='green', fontsize=12)
        angle_labels.append(label)
        point, = ax.plot(x, y, 'go', markersize=6)
        points.append(point)
        point_label = ax.text(x + 0.05, y + 0.05, r'$\left(\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2}\right)$', fontsize=10)
        point_labels.append(point_label)

        # Add arc for pi/4 (radius 0.4) - Increased radius
        arc = Arc((0, 0), 0.4, 0.4, angle=0, theta1=0, theta2=np.degrees(theta), color='green', linewidth=1.5, alpha=0.8)
        ax.add_patch(arc)
        angle_arcs.append(arc)

        line.set_visible(True)
        label.set_visible(True)
        point.set_visible(True)
        point_label.set_visible(True)
        arc.set_visible(True)

    elif frame == 3: # pi/3
        theta = angles_rad[r'$\frac{\pi}{3}$']
        x, y = np.cos(theta), np.sin(theta)
        line, = ax.plot([0, x], [0, y], 'b--', alpha=0.7)
        angle_lines.append(line)
        label = ax.text(x * 0.5, y * 0.5 + 0.05, r'$\frac{\pi}{3}$', color='blue', fontsize=12)
        angle_labels.append(label)
        point, = ax.plot(x, y, 'bo', markersize=6)
        points.append(point)
        point_label = ax.text(x + 0.05, y + 0.05, r'$\left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$', fontsize=10)
        point_labels.append(point_label)

        # Add arc for pi/3 (radius 0.5) - Increased radius further
        arc = Arc((0, 0), 0.5, 0.5, angle=0, theta1=0, theta2=np.degrees(theta), color='blue', linewidth=1.5, alpha=0.8)
        ax.add_patch(arc)
        angle_arcs.append(arc)

        line.set_visible(True)
        label.set_visible(True)
        point.set_visible(True)
        point_label.set_visible(True)
        arc.set_visible(True)

    # Frames 4-7: Animate pi/6 triangle and formulas
    if frame >= 4:
        # Get pi/6 coordinates
        theta_pi6 = angles_rad[r'$\frac{\pi}{6}$']
        x_pi6, y_pi6 = np.cos(theta_pi6), np.sin(theta_pi6)

        # Draw triangle lines
        if frame == 4: # Hypotenuse
            line_hyp, = ax.plot([0, x_pi6], [0, y_pi6], 'purple', linewidth=2)
            triangle_lines.append(line_hyp)
            line_hyp.set_visible(True)
        elif frame == 5: # Adjacent
            line_adj, = ax.plot([0, x_pi6], [0, 0], 'red', linewidth=2)
            triangle_lines.append(line_adj)
            line_adj.set_visible(True)
        elif frame == 6: # Opposite
            line_opp, = ax.plot([x_pi6, x_pi6], [0, y_pi6], 'green', linewidth=2)
            triangle_lines.append(line_opp)
            line_opp.set_visible(True)

        # Label sides with exact fractions/values
        if frame == 7:
            hypotenuse_label.set_position((x_pi6 / 2, y_pi6 / 2 + 0.05))
            hypotenuse_label.set_text(r'Hypotenuse = 1')
            hypotenuse_label.set_visible(True)

            opposite_label.set_position((x_pi6 + 0.05, y_pi6 / 2))
            opposite_label.set_text(r'Opposite = $\frac{1}{2}$')
            opposite_label.set_visible(True)

            adjacent_label.set_position((x_pi6 / 2, -0.05))
            adjacent_label.set_text(r'Adjacent = $\frac{\sqrt{3}}{2}$')
            adjacent_label.set_visible(True)

            # Display formulas with fractions
            formula_text = r"""
            For $\theta = \frac{\pi}{6}$:

            $\sin\left(\frac{\pi}{6}\right) = \frac{\text{Opposite}}{\text{Hypotenuse}} = \frac{1/2}{1} = \frac{1}{2}$

            $\cos\left(\frac{\pi}{6}\right) = \frac{\text{Adjacent}}{\text{Hypotenuse}} = \frac{\sqrt{3}/2}{1} = \frac{\sqrt{3}}{2}$

            $\tan\left(\frac{\pi}{6}\right) = \frac{\text{Opposite}}{\text{Adjacent}} = \frac{1/2}{\sqrt{3}/2} = \frac{1}{\sqrt{3}} = \frac{\sqrt{3}}{3}$
            """
            formula_box_text.set_text(formula_text)
            formula_box_text.set_visible(True)

    # Return all artists that were modified
    return angle_lines + angle_labels + point_labels + points + angle_arcs + \
           triangle_lines + [hypotenuse_label, opposite_label, adjacent_label, formula_box_text]

# Create the animation
# frames: 0 (initial state) + 3 (angles + arcs + points) + 4 (triangle steps + labels/formulas) = 8 frames
# Keeping blit=False for consistent rendering in Colab as per previous troubleshooting.
ani = FuncAnimation(fig, animate, frames=range(8), init_func=init, blit=False, interval=1500, repeat=False)

# To get the HTML output for embedding in PyScript, we use to_jshtml()
# We don't call HTML() directly here, as that's for Jupyter/Colab display.
# Instead, the output will be captured by PyScript and displayed in the target div.
# We will explicitly return this HTML string at the end of the PyScript block.
animation_html_output = ani.to_jshtml()
