import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

def plot_boxes_W_N3(ax, data,
                 font_scale=1.4,
                 metric='metric?',
                 point_size=6,
                 ygrid=False,
                 connect_pairs=False,
                 legends=True,
                 saveplot=0,
                 filename='filename',
                 dpi=300):

    sns.set_context('notebook', font_scale=font_scale)

    box_palette = {'W': '#FFE994', 'N3': '#9BDDF9'}
    swarmplot_palette = {'W': '#FF6600', 'N3': '#2A7FFF'}

    sns.boxplot(y="value", x="cond", data=data, linewidth=1.5, hue="cond",
                palette=box_palette, saturation=1.0, showmeans=True, meanline=True,
                legend=False, meanprops=dict(linestyle='dashed', color='gray', linewidth=2),
                medianprops=dict(linestyle=None, linewidth=2), ax=ax)

    sns.swarmplot(y="value", x="cond", data=data, s=point_size,
                  palette=swarmplot_palette, hue="cond", legend=False, ax=ax)

    # Optional: connect i-th elements
    if connect_pairs:
        group_W = data[data['cond'] == 'W']['value'].to_numpy()
        group_N3 = data[data['cond'] == 'N3']['value'].to_numpy()
        if len(group_W) == len(group_N3):
            for y1, y2 in zip(group_W, group_N3):
                ax.plot([0, 1], [y1, y2], color='gray', alpha=0.4, linewidth=1)
        else:
            print("⚠️ Cannot connect pairs: groups have different lengths.")

    # Calculate means #############################
    means = data.groupby("cond")["value"].mean()
    means = means.iloc[::-1]
    datax0W = data[data["cond"] == "W"]
    datax0N = data[data["cond"] == "N3"]
    dataxW = datax0W[["value"]].to_numpy()
    dataxN = datax0N[["value"]].to_numpy()
    datax = [dataxW, dataxN]

    if legends:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc='lower left')

    # Calculate statistical significance between 'W' and 'N3' groups ###############
    stat_test = stats.ranksums(data[data['cond'] == 'W']['value'], data[data['cond'] == 'N3']['value'])
    # Calculate significance level (adjust p-value if necessary)
    p_value = stat_test.pvalue
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

    # Add a bar or bracket between the box plots
    (miny, maxy) = ax.get_ylim()
    yposition = maxy
    maxy = maxy + 0.1 * (maxy - miny)
    ax.set_ylim(miny, maxy)
    endwidth = (maxy - miny) / 100
    ax.plot([0, 1], [yposition, yposition], color='black', lw=1.5, zorder=20)  # Adjust the coordinates and style as needed
    ax.plot([0, 0], [yposition - endwidth, yposition + endwidth], color='black', lw=1.5, zorder=20)
    ax.plot([1, 1], [yposition - endwidth, yposition + endwidth], color='black', lw=1.5, zorder=20)
    # Add significance annotation to the plot
    if p_value < 0.05:
        ax.annotate(f'{significance_asterisks}', xy=(0.5, yposition + endwidth), ha='center', fontsize=12)
    else:
        ax.annotate(f'p = {p_value:.5f} {significance_asterisks}', xy=(0.5, yposition + endwidth), ha='center', fontsize=12)
    ################################################################################

    # Change axis labels, ticks, and title
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Wakefulness", "Deep Sleep"])
    ax.set_xlabel('')
    ax.set_ylabel(metric)
    
    # Add horizontal grid
    if ygrid:
        ax.grid(axis='y')
        ax.set_axisbelow(True)

    if saveplot == 1:
        # Save plots
        plt.savefig(filename + '.pdf', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.svg', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.png', bbox_inches='tight', dpi=dpi)
        plt.tight_layout()
        plt.show()


###########################################################

def plot_boxes_generalized(ax, dataset, labels,
                           y_min=None, y_max=None,
                           h_line=None,
                           box_palette=None, swarmplot_palette=None,
                           font_scale=1.4,
                           point_size=6,
                           plot_title='Title?',
                           y_axis_label='Y-axis label?',
                           show_p_values=True,
                           ygrid=False,
                           connect_pairs=False,
                           saveplot=False,
                           filename='filename',
                           dpi=300):

    sns.set_context('notebook', font_scale=font_scale)

    all_data = []
    for data, label in zip(dataset, labels):
        temp_df = pd.DataFrame(data, columns=['value'])
        temp_df['cond'] = label
        all_data.append(temp_df)
    data = pd.concat(all_data, ignore_index=True)

    if box_palette is None:
        box_palette = sns.color_palette("deep")[0:len(dataset)]
    if swarmplot_palette is None:
        swarmplot_palette = sns.color_palette("deep")[0:len(dataset)]

    sns.boxplot(y="value", x="cond", data=data, linewidth=1.5, hue="cond",
                palette=box_palette, saturation=1.0, showmeans=True, meanline=True,
                legend=False, boxprops=dict(alpha=0.5),
                meanprops=dict(linestyle='dashed', color='gray', linewidth=2),
                medianprops=dict(linestyle=None, linewidth=2), ax=ax, order=labels)

    sns.swarmplot(y="value", x="cond", data=data, s=point_size,
                  palette=swarmplot_palette, hue="cond", legend=False, ax=ax, order=labels)

    # Optional: connect i-th elements between consecutive groups
    if connect_pairs:
        for i in range(len(labels) - 1):
            g1 = data[data['cond'] == labels[i]]['value'].to_numpy()
            g2 = data[data['cond'] == labels[i+1]]['value'].to_numpy()
            if len(g1) == len(g2):
                for y1, y2 in zip(g1, g2):
                    ax.plot([i, i+1], [y1, y2], color='gray', alpha=0.4, linewidth=1)
            else:
                print(f"⚠️ Cannot connect pairs between '{labels[i]}' and '{labels[i+1]}': different lengths.")

    # Compute significance for each pair of conditions
    pairs = [(labels[i], labels[j]) for i in range(len(labels)) for j in range(i+1, len(labels))]
    (miny, maxy) = ax.get_ylim()
    y_increment = 0.1 * (maxy - miny)
    yposition = maxy

    h=0
    if show_p_values:
        for pair in pairs:
            group1 = data[data['cond'] == pair[0]]['value']
            group2 = data[data['cond'] == pair[1]]['value']

            # Perform statistical test
            stat_test = stats.ranksums(group1, group2)
            p_value = stat_test.pvalue

            # Determine significance level
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

    # Change axis labels, ticks, and title
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

    # Add horizontal grid
    if ygrid:
        ax.grid(axis='y')
        ax.set_axisbelow(True)

    if saveplot:
        plt.savefig(filename + '.pdf', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.svg', bbox_inches='tight', dpi=dpi)
        plt.savefig(filename + '.png', bbox_inches='tight', dpi=dpi)
