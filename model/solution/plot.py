import pyam
import matplotlib.pyplot as plt

plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 5
plt.rcParams['ytick.labelsize'] = 5
plt.rc('legend', fontsize=5)

dt = pyam.IamDataFrame('Directed Transition-20220323T1405/heat-density-nuts3.xlsx').data
sc = pyam.IamDataFrame('Societal Commitment-20220323T1406/heat-density-nuts3.xlsx').data
tf = pyam.IamDataFrame('Techno-Friendly-20220323T1407/heat-density-nuts3.xlsx').data
tf = tf[tf['value'] != 0]
gd = pyam.IamDataFrame('Gradual Development-20220323T1407/heat-density-nuts3.xlsx').data


list_of_values = dict()
for region in tf.region:
    val_dt = dt[dt['region'] == region]['value'].item()
    val_sc = sc[sc['region'] == region]['value'].item()
    val_tf = tf[tf['region'] == region]['value'].item()
    val_gd = gd[gd['region'] == region]['value'].item()
    val = [val_dt, val_sc, val_tf, val_gd]
    val_min = min(val)
    val_max = max(val)
    list_of_values[region] = [val_min, val_max]

fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(1, 1)

figtop = fig.add_subplot(gs[:, :])
figtop.minorticks_off()

figtop.set_xticks(ticks=range(0, len(tf.region), 1))
figtop.set_xticklabels(labels=list_of_values.keys(), rotation=90)
figtop.set_xlim([-0.5, len(tf.region)-0.5])

x=0
for key in list_of_values.keys():
    large = list_of_values[key][1]
    figtop.scatter(x=x, y=large, marker='.', color='#3E497A', s=10)
    small = list_of_values[key][0]
    if small != 0:
        figtop.scatter(x=x, y=small, marker='.', color='#3E497A', s=10)
        figtop.plot(2*[x], [small, large], linewidth=2, color="#3E497A")
    x += 1
    
figtop.set_title('Heat density at NUTS3 level in '+r"$\frac{GWh}{km^2}$")


plt.tight_layout()
fig.savefig("heat-density-nuts3.eps", format="eps")
fig.savefig("heat-density-nuts3.png", dpi=900)