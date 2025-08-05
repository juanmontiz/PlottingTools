def plot_half_violin_box_swarm(ax, dataset, labels,
                                y_min=None, y_max=None,
                                h_line=None,
                                box_palette=None,
                                swarm_palette=None,
                                violin_palette=None,
                                bias=0.2,
                                font_scale=1.4,
                                point_size=6,
                                plot_title='Title?',
                                y_axis_label='Y-axis label?',
                                show_p_values=True,
                                ygrid=False,
                                saveplot=False,
                                filename='filename',
                                dpi=300):
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    import scipy.stats as stats
    
    sns.set_context('notebook', font_scale=font_scale)

    n_groups = len(labels)

    # Color palettes
    def resolve_palette(palette, n):
        if palette is None:
            return sns.color_palette("deep", n)
        elif isinstance(palette, str):
            return sns.color_palette(palette, n)
        elif isinstance(palette, list):
            if len(palette) < n:
                raise ValueError(f"Palette has fewer colors ({len(palette)}) than number of groups ({n})")
            return palette
        else:
            raise TypeError(f"Palette must be a string, list, or None, but got {type(palette)}")

    # Resolve palettes
    violin_palette = resolve_palette(violin_palette, n_groups)
    box_palette = resolve_palette(box_palette, n_groups)
    swarm_palette = resolve_palette(swarm_palette, n_groups)


    # Combine data
    all_data = []
    for i, (data, label) in enumerate(zip(dataset, labels)):
        df = pd.DataFrame({'value': data, 'group': i, 'label': label})
        all_data.append(df)
    df_all = pd.concat(all_data, ignore_index=True)

    # === Plot half-violins ===
    for i in range(n_groups):
        values = df_all[df_all['group'] == i]['value']
        parts = ax.violinplot(values, positions=[i + bias],
                              showmeans=False, showmedians=False,
                              showextrema=False, widths=0.6)
        for pc in parts['bodies']:
            pc.set_facecolor(violin_palette[i])
            pc.set_alpha(0.5)
            m = np.mean(pc.get_paths()[0].vertices[:, 0])
            pc.get_paths()[0].vertices[:, 0] = np.clip(pc.get_paths()[0].vertices[:, 0], m, np.inf)

    # === Plot boxplots manually ===
    widths=0.25
    for i in range(n_groups):
        values = df_all[df_all['group'] == i]['value']
        ax.boxplot(values,
                   positions=[i - bias - widths/2],
                   widths=widths,
                   patch_artist=True,
                   boxprops=dict(facecolor=box_palette[i], color='black', linewidth=1.5, alpha=0.5),
                   medianprops=dict(color=box_palette[i], linewidth=2, alpha=1),
                   whiskerprops=dict(color='black', linewidth=1.5),
                   capprops=dict(color='black', linewidth=1.5),
                   flierprops=dict(marker='', alpha=0))

    # === Swarmplot (centered) ===
    for i in range(n_groups):
        values = df_all[df_all['group'] == i]['value'].values
        x_positions = np.random.normal(loc=i, scale=0.03, size=len(values))  # jitter manually
        ax.scatter(x_positions, values, s=point_size**2, color=swarm_palette[i], zorder=10, alpha=0.9)

    # === Compute significance tests ===
    pairs = [(labels[i], labels[j]) for i in range(len(labels)) for j in range(i+1, len(labels))]
    (miny, maxy) = ax.get_ylim()
    y_increment = 0.1 * (maxy - miny)
    yposition = maxy
    
    h=0
    if show_p_values:
        for pair in pairs:
            group1 = df_all[df_all['label'] == pair[0]]['value']
            group2 = df_all[df_all['label'] == pair[1]]['value']

            stat_test = stats.ranksums(group1, group2)
            p_value = stat_test.pvalue
            
            # Significance asterisks
            if p_value < 1e-5:
                significance_asterisks = '*****'
            elif p_value < 1e-4:
                significance_asterisks = '****'
            elif p_value < 1e-3:
                significance_asterisks = '***'
            elif p_value < 1e-2:
                significance_asterisks = '**'
            elif p_value < 0.05:
                significance_asterisks = '*'
            else:
                significance_asterisks = '(n.s.)'

            x_start = labels.index(pair[0])
            x_end = labels.index(pair[1])
            y = yposition * 1.0
            h = df_all['value'].max() * 0.01
            ax.plot([x_start, x_start, x_end, x_end], 
                    [y, y + h, y + h, y-h], 
                    color='black', lw=1.5, zorder=20)
            ax.text((x_start + x_end) / 2, y + h * 1.05, significance_asterisks,
                ha='center', va='bottom', fontsize=14, color='black')
            ax.set_ylim(top=y + h * 2)
            yposition += y_increment

    # === Labels and formatting ===
    ax.set_xlim(-0.5 - bias/2, n_groups - 0.5 + bias/2)
    ax.set_xticks(range(n_groups))
    ax.set_xticklabels(labels)
    ax.set_ylabel(y_axis_label)
    ax.set_title(plot_title)
    ax.set_xlabel('')
    if y_max is None:
        y_max = yposition
    else:
        y_max = max(y_max, yposition)
    ax.set_ylim(y_min, y_max+6*h)
    # sns.despine()

    # Plot horizontal line
    if h_line is not None:
        ax.axhline(h_line, color='gray', linestyle='-', linewidth=2, zorder=0, alpha=0.5)

    if ygrid:
        ax.grid(axis='y')
        ax.set_axisbelow(True)

    if saveplot:
        plt.savefig(filename + '.png', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.pdf', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.svg', bbox_inches='tight', dpi=dpi)
