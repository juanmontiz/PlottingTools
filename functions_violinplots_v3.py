import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

def plot_violins_generalized(ax, dataset, labels,
                             y_min=None, y_max=None,
                             h_line=None,
                             violin_palette=None, swarmplot_palette=None,
                             font_scale=1.4,
                             point_size=6,
                             plot_title='Title?',
                             y_axis_label='Y-axis label?',
                             show_p_values=True,
                             show_swarm_plot=True,
                             xgrid=False,
                             saveplot=False,
                             filename='filename',
                             dpi=300):
    
    sns.set_context('notebook', font_scale=font_scale)
    
    # Combine dataset into a single DataFrame
    all_data = []
    for i, (data, label) in enumerate(zip(dataset, labels)):
        temp_df = pd.DataFrame(data, columns=['value'])
        temp_df['cond'] = label  # Condition labels
        all_data.append(temp_df)
    data = pd.concat(all_data, ignore_index=True)
    
    # Set default palettes if not provided
    if violin_palette is None:
        violin_palette = sns.color_palette("deep")[0:len(dataset)]
    if swarmplot_palette is None:
        swarmplot_palette = sns.color_palette("deep")[0:len(dataset)]
    
    violin_parts = sns.violinplot(
        y="value",
        x="cond",
        data=data,
        linewidth=1.5,
        hue="cond",
        palette=violin_palette,
        saturation=1.0,
        legend=False,
        ax=ax,
        order=labels,
    )
    # Set transparency (alpha) for violins
    if show_swarm_plot:
        for pc in violin_parts.collections:
            pc.set_alpha(0.6)  # Adjust transparency level (0.0 = fully transparent, 1.0 = opaque)

    if show_swarm_plot:
        sns.swarmplot(
            y="value",
            x="cond",
            data=data,
            s=point_size,
            palette=swarmplot_palette,
            hue="cond",
            legend=False,
            ax=ax,
            order=labels,
            zorder=1 # Plots the swarm between the violin and the inner box
        )
        
    # Compute significance tests
    pairs = [(labels[i], labels[j]) for i in range(len(labels)) for j in range(i+1, len(labels))]
    (miny, maxy) = ax.get_ylim()
    y_increment = 0.1 * (maxy - miny)
    yposition = maxy
    
    h=0
    if show_p_values:
        for pair in pairs:
            group1 = data[data['cond'] == pair[0]]['value']
            group2 = data[data['cond'] == pair[1]]['value']
            
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
            
            # Add significance bar and annotation
            x_start = labels.index(pair[0])
            x_end = labels.index(pair[1])
            y = yposition * 1.0
            h = data['value'].max() * 0.01
            ax.plot([x_start, x_start, x_end, x_end], 
                    [y, y + h, y + h, y-h], 
                    color='black', lw=1.5, zorder=20)
            ax.text((x_start + x_end) / 2, y + h * 1.05, significance_asterisks,
                ha='center', va='bottom', fontsize=14, color='black')
            ax.set_ylim(top=y + h * 2)
            yposition += y_increment
    
    # Axis labels and title
    ax.set_xlabel('')
    ax.set_ylabel(y_axis_label)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title(plot_title)

    # Update axis limits
    if y_max is None:
        y_max = yposition
    else:
        y_max = max(y_max, yposition)
    ax.set_ylim(y_min, y_max+6*h)

    # Plot horizontal line
    if h_line is not None:
        ax.axhline(h_line, color='gray', linestyle='-', linewidth=2, zorder=0, alpha=0.75)

    if xgrid:
        ax.grid(axis='y')
        ax.set_axisbelow(True)
    
    if saveplot:
        plt.savefig(filename + '.pdf', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.svg', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.png', bbox_inches='tight', dpi=dpi)
