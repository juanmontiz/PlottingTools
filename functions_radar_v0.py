import matplotlib.pyplot as plt
import numpy as np
import itertools

def plot_radar(groups, rsn_labels, title="Radar Chart", colors=None):
    """
    Plot a radar (spider) chart for any number of groups.

    Parameters
    ----------
    groups : list of dict
        Each dict should have:
            - "label": name of the group (str)
            - "values": list/array of values (len = number of RSNs)
    rsn_labels : list of str
        Labels for the RSNs (must match the length of "values" for each group).
    title : str, optional
        Title of the chart.
    colors : list of str, optional
        List of matplotlib color names or hex codes. If None, uses tab colors.
    """

    num_vars = len(rsn_labels)

    # Check that all groups have the same number of values as RSNs
    for g in groups:
        if len(g["values"]) != num_vars:
            raise ValueError(f"Group '{g['label']}' has {len(g['values'])} values, "
                             f"but there are {num_vars} RSNs.")

    # Default color cycle if none provided
    if colors is None:
        colors = plt.cm.tab10.colors  # 10 distinct colors
    color_cycle = itertools.cycle(colors)

    # Compute max value for scaling
    max_val = max(max(g["values"]) for g in groups)

    # Angles for each RSN axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # close the loop

    # --- PLOT ---
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for g, color in zip(groups, color_cycle):
        values = list(g["values"]) + [g["values"][0]]  # close loop
        ax.plot(angles, values, 'o-', markersize=6, linewidth=2.0, label=g["label"], color=color)
        ax.fill(angles, values, alpha=0.1, color=color)

    # Set positions of RSN labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([''] * num_vars)  # Hide default labels
    for angle, label in zip(angles[:-1], rsn_labels):
        angle_deg = np.rad2deg(angle)
        ha = 'center'
        if 95 < angle_deg < 265:
            ha = 'right'
        elif angle_deg < 85 or angle_deg > 275:
            ha = 'left'
        ax.text(angle, max_val * 1.05, label,
                size=12, horizontalalignment=ha, verticalalignment='center',
                rotation=0, rotation_mode='anchor')

    # Y-axis settings
    yticks = np.linspace(0, max_val, 5)
    ax.set_rlabel_position(180 / num_vars)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f'{v:.2f}' for v in yticks])
    ax.set_ylim(0, max_val)

    # Title and legend
    plt.title(title, size=14, pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.show()