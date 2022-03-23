import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.patches as mpatches


_color = {
    "Biomass": "#A6CF98",
    "Direct electric": "#FFAB76",
    "Geothermal": "#D4AC2B",
    "Synthetic gas" : "#D3DEDC",
    "Heat pump (air)": "#A2D2FF",
    "Heat pump (ground)": "#577BC1",
    "Hydrogen": "#B983FF",
    "Waste":"#8B9A46",
    "Oil":"#DA0037",
    }


def draw_brace(ax, xspan, text):
    """Draws an annotated brace on the axes."""
    xmin, xmax = xspan
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    resolution = int(xspan/xax_span*100)*2+1 # guaranteed uneven
    beta = 300./xax_span # the higher this is, the smaller the radius

    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:resolution//2+1]
    y_half_brace = (1/(1.+np.exp(-beta*(x_half-x_half[0])))
                    + 1/(1.+np.exp(-beta*(x_half-x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = ymin + (.05*y - .01)*yspan # adjust vertical position

    ax.autoscale(False)
    ax.plot(x, y, lw=0.75, color="gray", zorder=-10)

    ax.text((xmax+xmin)/2., ymin+.09*yspan, text, ha='center', va='bottom',
            fontsize=10, color="gray",
            bbox=dict(facecolor='none', edgecolor='black', linewidth=0.,
                                 boxstyle="round,pad=0.3"))
    


if __name__ == "__main__":
    fig, axes = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [2.25, 0.9]})
    
    density = [4.92, 7.23, 9.64, 9.11, 10.93, 6.52, 3.99]
    x_val = [0.51, 0.75, 1., 1.25, 1.5, 1.75, 0.51+1.45]
    
    axes[0].plot(x_val, density, linewidth=1.5, color="black", zorder=10)
    axes[0].set_xlim([0, 3.5])
    axes[0].set_ylim([0, 12])
    
    axes[0].plot([0.51, 0.51], [0, 12], linestyle="dotted", linewidth=1.5, color="#A2D2FF")
    axes[0].plot([0.51+1.45, 0.51+1.45], [0, 12], linestyle="dotted", linewidth=1.5, color="#A2D2FF")
    # axes[0].plot([0.51+0.21+1.45, 0.51+0.21+1.45], [0, 12], linestyle="dotted", linewidth=1.5, color="gray")
    
    axes[0].plot([0.51], [4.92], marker="d", zorder=11, color="black", markersize=5)
    axes[0].plot([0.51+1.45], [3.99], marker="o", zorder=11, color="black", markersize=5)
    
    axes[0].plot([1.5], [10.93], marker="*", zorder=11, color="#F47340", markersize=6)
    axes[0].plot([1.5, 1.5], [10.93, 6], zorder=-2, color="#F47340", linewidth=1)
    axes[0].plot([1.4, 1.5], [6, 6], zorder=11, color="#F47340", linewidth=1)
    axes[0].text(x=1.1, y=5.5, s="10.9", color="#F47340", fontsize=12)
    axes[0].text(x=0.25, y=3.8, s="4.9", color="black", fontsize=12)
    
    # axes[0].plot([0, 2.1], [10, 10], linestyle="solid", linewidth=1.5, color="#A2D2FF")
    
    axes[0].annotate(
        "",
        fontsize=3,
        color="#A2D2FF",
        multialignment="center",
        xy=(1.25, 1),
        xycoords="data",
        xytext=(0.55, 1),
        textcoords="data",
        arrowprops=dict(
            headlength=8,
            headwidth=4,
            width=0.5,
            connectionstyle="arc3,rad=0",
            color="#A2D2FF"),
        zorder=-1
        )
    
    axes[0].text(x=0.65, y=1.5, s="Heat pump (air) in DH", color="#11468F", fontsize=10)
    axes[0].set_xlabel("District heating (DH) in TWh")
    axes[0].set_ylabel("Heat density"+r"in $\frac{GWh}{km^2}$")
    
    # draw_brace(axes[0], (0.51+0.21+1.45, 3.43), 'No supply for DH')
    # draw_brace(axes[0], (0, 0.51), 'DH')
        
    
    _line = Line2D([0], [0], label = "Directed Transition incl.\nall heat pump (air) on-site",color="black", marker="d", linewidth=0, markersize=4)
    _line1 = Line2D([0], [0], label = "Maximum heat density",color="#F47340", marker="*", linewidth=0)
    _line2 = Line2D([0], [0], label = "All heat pump (air) in DH",color="black", marker="o", linewidth=0, markersize=4)
    leg = axes[0].legend(handles=[_line1, _line, _line2], loc='upper right', fontsize=8, framealpha=1, handlelength=1, handletextpad=0.75, borderpad=0.75, columnspacing=1, edgecolor="black", frameon=True, ncol=1)
    leg.get_frame().set_linewidth(0.1)
    
    gen = [0.5, 0.6, 1.45, 0.21, 1.12]
    
    axes[1].barh([0], 0.08, color="#D3DEDC", height=0.5)
    axes[1].barh([0], 0.43, color="#8B9A46", left=0.08, height=0.5)
    axes[1].barh([0], 1.45, color="#A2D2FF", left=0.51, height=0.5)
    axes[1].barh([0], 0.21, color="#A6CF98", left=0.51+1.45, height=0.5)
    axes[1].barh([0], 0.14, color="#FFAB76", left=0.51+1.45+0.21, height=0.5)
    axes[1].barh([0], 1.12, color="#577BC1", left=0.51+1.45+0.21+0.14, height=0.5)
    
    axes[1].plot([0.51, 0.51], [0, 0.5], linestyle="dotted", linewidth=1.5, color="#A2D2FF", zorder=-100)
    axes[1].plot([0.51+1.45, 0.51+1.45], [0, 0.5], linestyle="dotted", linewidth=1.5, color="#A2D2FF", zorder=-100)
    # axes[1].plot([0.51+0.21+1.45, 0.51+0.21+1.45], [0, 0.5], linestyle="dotted", linewidth=1.5, color="gray", zorder=-100)
    
    axes[1].plot([1.5, 1.5], [-0.25, 0.25], zorder=100, color="#F47340", linewidth=2)
    
    axes[1].set_xlim([0, 3.5])
    axes[1].set_ylim([-1, 0.5])
    
    _patches = []
    for _key in ["Synthetic gas", "Waste", "Heat pump (air)", "Biomass", "Direct electric", "Heat pump (ground)"]:
        _patches.append(mpatches.Patch(color=_color[_key], label=_key))
    
    axes[1].legend(handles=_patches, loc='lower center', fontsize=6.6, framealpha=1, handlelength=0.7, handletextpad=0.3, ncol=9, borderpad=0.35, columnspacing=1, bbox_to_anchor=(0.5, 0.1))
    axes[1].set_yticks([])
    axes[1].xaxis.set_ticks_position("top")
    axes[1].set_xticklabels([])
    axes[1].set_xlabel("Heat generation by source")
    
    # fig.suptitle("Heat density of district heating in Graz (AT221)\nby amount of heat pumps (air) generation used in district heating")
    plt.tight_layout()
    fig.savefig("Sen_District_heating.eps", format="eps")
    fig.savefig("Sen_District_heating.png", dpi=1000)