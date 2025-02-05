import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

def plot_boxes_generalized(ax, dataset, labels,
                           box_palette=None, swarmplot_palette=None,
                           font_scale=1.4,
                           point_size=6,
                           plot_title='Title?',
                           y_axis_label='Y-axis label?',
                           show_p_values=True,
                           xgrid=False,
                           saveplot=False,
                           filename='filename',
                           dpi=300):

    # Create seaborn context
    sns.set_context('notebook', font_scale=font_scale)

    # Combine all dataset into a single DataFrame
    all_data = []
    for i, (data, label) in enumerate(zip(dataset, labels)):
        temp_df = pd.DataFrame(data, columns=['value'])
        temp_df['cond'] = label  # Add a column for condition labels
        all_data.append(temp_df)
    data = pd.concat(all_data, ignore_index=True)

    # Set default palettes if not provided
    if box_palette is None:
        box_palette = sns.color_palette("deep")[0:len(dataset)]
    if swarmplot_palette is None:
        swarmplot_palette = sns.color_palette("deep")[0:len(dataset)]

    sns.boxplot(
        y="value",
        x="cond",
        data=data,
        linewidth=1.5,
        hue="cond",
        palette=box_palette,
        saturation=1.0,
        showmeans=True,
        meanline=True,
        legend=False,
        boxprops=dict(alpha=0.5),  # Lighter tone for the boxes
        meanprops=dict(linestyle='dashed', color='gray', linewidth=2),
        medianprops=dict(linestyle=None, linewidth=2),
        ax=ax,
        order=labels  # Ensure consistent order
    )

    sns.swarmplot(
        y="value",
        x="cond",
        data=data,
        s=point_size,  # Circle size
        palette=swarmplot_palette,
        hue="cond",  # Use `cond` as hue
        legend=False,  # Disable legend
        ax=ax,
        order=labels  # Ensure consistent order
    )

    # Compute significance for each pair of conditions
    pairs = [(labels[i], labels[j]) for i in range(len(labels)) for j in range(i+1, len(labels))]
    (miny, maxy) = ax.get_ylim()
    y_increment = 0.1 * (maxy - miny)
    yposition = maxy

    if show_p_values:
        for pair in pairs:
            group1 = data[data['cond'] == pair[0]]['value']
            group2 = data[data['cond'] == pair[1]]['value']

            # Perform statistical test
            stat_test = stats.ranksums(group1, group2)
            p_value = stat_test.pvalue

            # Determine significance level
            if p_value < 0.00001:
                significance_asterisks = '*****'
            elif p_value < 0.0001:
                significance_asterisks = '****'
            elif p_value < 0.001:
                significance_asterisks = '***'
            elif p_value < 0.01:
                significance_asterisks = '**'
            elif p_value < 0.05:
                significance_asterisks = '*'
            else:
                significance_asterisks = '(n.s.)'

            # Add significance bar and annotation
            ax.plot([labels.index(pair[0]), labels.index(pair[1])],
                    [yposition, yposition],
                    color='black', lw=1.5, zorder=20)
            ax.annotate(f'{significance_asterisks}', 
                        xy=((labels.index(pair[0]) + labels.index(pair[1])) / 2, yposition + y_increment / 2), 
                        ha='center', fontsize=12)
            yposition += y_increment

    # Update axis limits
    ax.set_ylim(miny, yposition)

    # Change axis labels, ticks, and title
    ax.set_xlabel('')
    ax.set_ylabel(y_axis_label)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title(plot_title)

    # Add horizontal grid
    if xgrid:
        ax.grid(axis='y')
        ax.set_axisbelow(True)

    if saveplot:
        plt.savefig(filename + '.pdf', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.svg', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.png', bbox_inches='tight', dpi=dpi)
        plt.tight_layout()
        plt.show()
