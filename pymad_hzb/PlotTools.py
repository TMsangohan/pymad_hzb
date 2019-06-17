import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pylab
import matplotlib.dates as mdates
import matplotlib
import numpy as np
import matplotlib.font_manager as font_manager

from copy import deepcopy

dict_plot = {'QUADRUPOLE': {"scale": 0.7, "color": "r", "edgecolor": "r", "label": "quad"},
             'SEXTUPOLE': {"scale": 0.5, "color": "g", "edgecolor": "g", "label": "sext"},
             'OCTUPOLE': {"scale": 0.5, "color": "g", "edgecolor": "g", "label": "sext"},
             'RFCAVITY': {"scale": 0.7, "color": "orange", "edgecolor": "lightgreen", "label": "cav"},
             'BEND': {"scale": 0.7, "color": "lightskyblue", "edgecolor": "k", "label": "bend"},
             'RBEND': {"scale": 0.7, "color": "lightskyblue", "edgecolor": "k", "label": "bend"},
             'SBEND': {"scale": 0.7, "color": "lightskyblue", "edgecolor": "k", "label": "bend"},
             'Matrix': {"scale": 0.7, "color": "pink", "edgecolor": "k", "label": "mat"},
             'MULTIPOLE': {"scale": 0.7, "color": "g", "edgecolor": "k", "label": "mult"},
             'Undulator': {"scale": 0.7, "color": "pink", "edgecolor": "k", "label": "und"},
             'MONITOR': {"scale": 0.5, "color": "orange", "edgecolor": "orange", "label": "mon"},
             'HKICKER': {"scale": 0.7, "color": "c", "edgecolor": "c", "label": "cor"},
             'KICKER': {"scale": 0.7, "color": "c", "edgecolor": "c", "label": "cor"},
             'VKICKER': {"scale": 0.7, "color": "c", "edgecolor": "c", "label": "cor"},
             'DRIFT': {"scale": 0., "color": "k", "edgecolor": "k", "label": ""},
             'MARKER': {"scale": 0., "color": "k", "edgecolor": "k", "label": "mark"},
             'DIPEDGE': {"scale": 0., "color": "k", "edgecolor": "k", "label": ""},
             'Solenoid': {"scale": 0.7, "color": "g", "edgecolor": "g", "label": "sol"},
             'TDCavity': {"scale": 0.7, "color": "magenta", "edgecolor": "g", "label": "tds"},
             'UnknownElement': {"scale": 0.7, "color": "g", "edgecolor": "g", "label": "unk"},
             }


class PlotOverLoadError:
    """
    Raised when trying to plot more than 2 columns in a single plot grid
    """
    pass


def new_plot_elems_madx(fig, ax, lat, s_point=0, nturns=1, y_scale=1, legend=True):
    alpha = 1
    dict_copy = deepcopy(dict_plot)
    points_with_annotation = []
    L = 0.
    q = []
    b = []
    c = []
    s = []
    u = []
    rf = []
    m = []
    for i, elem in lat.iterrows():
        if elem['KEYWORD'] == 'QUADRUPOLE':
            q.append(elem.K1L)
        elif elem['KEYWORD'] in ['BEND', 'RBEND', 'SBEND']:
            b.append(elem.ANGLE)
        elif elem['KEYWORD'] in ['HKICKER', 'VKICKER']:
            c.append(elem.ANGLE)
        elif elem['KEYWORD'] == 'SEXTUPOLE':
            s.append(elem.K2L)
        elif elem['KEYWORD'] == 'CAVITY':
            rf.append(elem.V)
        elif elem['KEYWORD'] == 'MULTIPOLE':
            m.append(sum(np.abs(elem.KN)))

    q_max = np.max(np.abs(q)) if len(q) != 0 else 0
    b_max = np.max(np.abs(b)) if len(b) != 0 else 0
    s_max = np.max(np.abs(s)) if len(s) != 0 else 0
    c_max = np.max(np.abs(c)) if len(c) != 0 else 0
    u_max = np.max(np.abs(u)) if len(u) != 0 else 0
    rf_max = np.max(np.abs(rf)) if len(rf) != 0 else 0
    m_max = np.max(m) if len(m) != 0 else 0

    ncols = np.sign(len(q)) + np.sign(len(b)) + np.sign(len(s)) + np.sign(len(c)) + np.sign(len(u)) + np.sign(
        len(rf)) + np.sign(len(m))

    labels_dict = {}
    for elem in dict_copy.keys():
        labels_dict[elem] = dict_copy[elem]["label"]

    for i, elem in lat.iterrows():
        if elem['KEYWORD'] in ['MARKER', 'DIPEDGE']:
            L += elem.L
            continue
        l = elem.L
        if l == 0:
            l = 0.03
        # type = elem.type
        scale = dict_copy[elem['KEYWORD']]["scale"]
        color = dict_copy[elem['KEYWORD']]["color"]
        label = dict_copy[elem['KEYWORD']]["label"]
        ecolor = dict_copy[elem['KEYWORD']]["edgecolor"]
        ampl = 1
        s_coord = np.array(
            [L + elem.L / 2. - l / 2., L + elem.L / 2. - l / 2., L + elem.L / 2. + l / 2., L + elem.L / 2. + l / 2.,
             L + elem.L / 2. - l / 2.]) + s_point

        if elem['KEYWORD'] == 'QUADRUPOLE':
            ampl = elem.K1L / q_max if q_max != 0 else 1
            point, = ax.fill(s_coord, (np.array([-1, 1, 1, -1, -1]) + 1) * ampl * scale * y_scale, color,
                             edgecolor=ecolor,
                             alpha=alpha, label=dict_copy[elem['KEYWORD']]["label"])
            dict_copy[elem['KEYWORD']]["label"] = ""

        elif elem['KEYWORD'] in ['BEND', 'RBEND', 'SBEND']:
            ampl = elem.ANGLE / b_max if b_max != 0 else 1
            point, = ax.fill(s_coord, (np.array([-1, 1, 1, -1, -1]) + 1) * ampl * scale * y_scale, color,
                             alpha=alpha, label=dict_copy[elem['KEYWORD']]["label"])
            dict_copy[elem['KEYWORD']]["label"] = ""

        elif elem['KEYWORD'] in ['HKICKER', 'VKICKER', 'KICKER']:

            ampl = elem.ANGLE / c_max if c_max != 0 else 0.5
            # print c_max, elem.angle, ampl
            if elem.ANGLE == 0:
                ampl = 0.5
                point, = ax.fill(s_coord, (np.array([-1, 1, 1, -1, -1])) * ampl * scale * y_scale, "lightcyan",
                                 edgecolor="k",
                                 alpha=0.5, label=dict_copy[elem['KEYWORD']]["label"])
            else:
                point, = ax.fill(s_coord, (np.array([-1, 1, 1, -1, -1]) + 1) * ampl * scale * y_scale, color,
                                 edgecolor=ecolor,
                                 alpha=alpha, label=dict_copy[elem['KEYWORD']]["label"])
            dict_copy['HKICKER']["label"] = ""
            dict_copy['VKICKER']["label"] = ""

        elif elem['KEYWORD'] == 'SEXTUPOLE':
            ampl = (elem.K2L) / s_max if s_max != 0 else 1
            point, = ax.fill(s_coord, (np.array([-1, 1, 1, -1, -1]) + 1) * ampl * scale * y_scale, color,
                             alpha=alpha, label=dict_copy[elem['KEYWORD']]["label"])
            dict_copy[elem['KEYWORD']]["label"] = ""

        elif elem['KEYWORD'] == 'CAVITY':
            ampl = 1  # elem.v/rf_max if rf_max != 0 else 0.5
            point, = ax.fill(s_coord, np.array([-1, 1, 1, -1, -1]) * ampl * scale * y_scale, color,
                             alpha=alpha, edgecolor="lightgreen", label=dict_copy[elem['KEYWORD']]["label"])
            dict_copy[elem['KEYWORD']]["label"] = ""

        elif elem['KEYWORD'] == 'MULTIPOLE':
            ampl = sum(elem.KN) / m_max if u_max != 0 else 0.5
            point, = ax.fill(s_coord, np.array([-1, 1, 1, -1, -1]) * ampl * scale * y_scale, color,
                             alpha=alpha, label=dict_copy[elem['KEYWORD']]["label"])
            dict_copy[elem['KEYWORD']]["label"] = ""

        else:
            point, = ax.fill(s_coord, np.array([-1, 1, 1, -1, -1]) * ampl * scale * y_scale, color, edgecolor=ecolor,
                             alpha=alpha)
        annotation = ax.annotate(elem['KEYWORD'] + ": " + elem.NAME,
                                 xy=(L + l / 2., 0),  # xycoords='data',
                                 # xytext=(i + 1, i), textcoords='data',
                                 horizontalalignment="left",
                                 arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=+0.2"),
                                 bbox=dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9),
                                 fontsize=16
                                 )
        # by default, disable the annotation visibility
        annotation.set_visible(False)
        L += elem.L
        points_with_annotation.append([point, annotation])

    def on_move(event):
        visibility_changed = False
        for point, annotation in points_with_annotation:
            should_be_visible = (point.contains(event)[0] == True)
            if should_be_visible != annotation.get_visible():
                visibility_changed = True
                annotation.set_visible(should_be_visible)

        if visibility_changed:
            plt.draw()

    on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
    if legend:
        ax.legend(loc='upper center', ncol=ncols, shadow=False, prop=font_manager.FontProperties(size=15))


def plotTwissTriple(twissdata, cols0=['X', 'Y'], cols1=['BETX', 'BETY'], cols2=['DX', 'DY'], fontsize=12, legend=True):
    if cols0:
        if len(cols0) > 2 or len(cols1) > 2 or len(cols2) > 2:
            raise PlotOverLoadError('Too much data for single grid, keep the number of cols per grid lower than 2.')
    else:
        if len(cols1) > 2 or len(cols2) > 2:
            raise PlotOverLoadError('Too much data for single grid, keep the number of cols per grid lower than 2.')
    matplotlib.rcParams.update({'font.size': fontsize})

    x = np.arange(len(twissdata))
    s = twissdata['S']

    # colors
    mainbg = '#07000d'  # '#808080' #'#F8F8FF' #'#ffffff'# '#07000d'
    axspinecolor = "#5998ff"

    ax0colors = ['#e1edf9', '#4ee6fd']
    ax1colors = ['#0080FF', '#C04000']

    ax2fillcolor = '#00ffe8'

    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    negCol = '#8f2020'

    with plt.style.context(['seaborn-poster']):
        fig = plt.figure(facecolor=mainbg)

        ax0 = plt.subplot2grid((8, 4), (0, 0), rowspan=1, colspan=4, facecolor=mainbg)
        ax0.xaxis.set_major_locator(mticker.MaxNLocator(10))

        if cols0:
            for i, el in enumerate(cols0):
                ax0.plot(s, twissdata[el], ax0colors[i], label=el, linewidth=1.5)
                ax0.fill_between(s, twissdata[el], 0, where=(twissdata[el] >= 0),
                                 facecolor=negCol, edgecolor=negCol, alpha=0.5)
                ax0.fill_between(s, twissdata[el], 0, where=(twissdata[el] <= 0),
                                 facecolor=posCol, edgecolor=posCol, alpha=0.5)
                plt.ylabel(' '.join(cols0))
        else:
            new_plot_elems_madx(plt.gcf(), ax0, twissdata, s_point=twissdata.iloc[0]['S'], nturns=1, y_scale=1,
                                legend=legend)

        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color(axspinecolor)
        ax0.spines['top'].set_color(axspinecolor)
        ax0.spines['left'].set_color(axspinecolor)
        ax0.spines['right'].set_color(axspinecolor)
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        ax0.grid(True, axis='x', which='minor')

        ax1 = plt.subplot2grid((8, 4), (1, 0), sharex=ax0, rowspan=4, colspan=4, facecolor=mainbg)

        for i, el in enumerate(cols1):
            ax1.plot(s, twissdata[el], ax1colors[i], label=el, linewidth=2)

        ax1.grid(True, color='w')
        ax1.xaxis.set_tick_params(which='major', length=3.0, direction='in', top='off')
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color(axspinecolor)
        ax1.spines['top'].set_color(axspinecolor)
        ax1.spines['left'].set_color(axspinecolor)
        ax1.spines['right'].set_color(axspinecolor)
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel(' '.join(cols1))

        cols1Legend = plt.legend(loc=9, ncol=2, prop={'size': fontsize}, fancybox=True, borderaxespad=0.)
        cols1Legend.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color='w')

        # TODO : LOCAL ALFA
        #         ax1v = ax1.twinx()
        #         ax1v.fill_between(s, twissdata['A'], pricing['Volume'], facecolor='#00ffe8', alpha=.4)

        ax2 = plt.subplot2grid((8, 4), (5, 0), sharex=ax0, rowspan=1, colspan=4, facecolor=mainbg)
        for i, el in enumerate(cols2):
            ax2.plot(s, twissdata[el], ax0colors[i], label=el, linewidth=2)
            ax2.fill_between(s, twissdata[el], 0, alpha=0.4, facecolor=ax2fillcolor, edgecolor=ax2fillcolor)

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.yaxis.label.set_color("w")
        ax2.spines['bottom'].set_color(axspinecolor)
        ax2.spines['top'].set_color(axspinecolor)
        ax2.spines['left'].set_color(axspinecolor)
        ax2.spines['right'].set_color(axspinecolor)
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel(' '.join(cols2))
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

    plt.show()


def plotCompareOptics(twissdata1, twissdata2, cols0=['BETX', 'BETY'], fontsize=12, legend=True):
    if cols0:
        if len(cols0) > 2:
            raise PlotOverLoadError('Too much data for single grid, keep the number of cols per grid lower than 2.')

    matplotlib.rcParams.update({'font.size': fontsize})

    x = np.arange(len(twissdata1))
    s1 = twissdata1['S']
    s2 = twissdata1['S']

    # colors
    mainbg = '#07000d'  # '#808080' #'#F8F8FF' #'#ffffff'# '#07000d'
    axspinecolor = "#5998ff"

    ax0colors = ['#e1edf9', '#4ee6fd']
    ax1colors = ['#0080FF', '#C04000']

    ax2fillcolor = '#00ffe8'

    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    negCol = '#8f2020'

    with plt.style.context(['seaborn-poster']):
        fig = plt.figure(facecolor=mainbg)

        # top plot - optical elements
        ax0 = plt.subplot2grid((8, 4), (0, 0), rowspan=1, colspan=4, facecolor=mainbg)
        ax0.xaxis.set_major_locator(mticker.MaxNLocator(10))

        new_plot_elems_madx(plt.gcf(), ax0, twissdata1, s_point=twissdata1.iloc[0]['S'], nturns=1, y_scale=1,
                            legend=legend)

        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color(axspinecolor)
        ax0.spines['top'].set_color(axspinecolor)
        ax0.spines['left'].set_color(axspinecolor)
        ax0.spines['right'].set_color(axspinecolor)
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        ax0.grid(True, axis='x', which='minor')
        ax0.axhline(0, color='w')

        # middle plot
        ax1 = plt.subplot2grid((8, 4), (1, 0), sharex=ax0, rowspan=4, colspan=4, facecolor=mainbg)

        for i, el in enumerate(cols0):
            ax1.plot(s1, twissdata1[el], ax1colors[i], label=el, linewidth=2, linestyle='dashed')
            ax1.plot(s2, twissdata2[el], ax1colors[i], label=el, linewidth=2)

        ax1.grid(True, color='w')
        ax1.xaxis.set_tick_params(which='major', length=3.0, direction='in', top='off')
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color(axspinecolor)
        ax1.spines['top'].set_color(axspinecolor)
        ax1.spines['left'].set_color(axspinecolor)
        ax1.spines['right'].set_color(axspinecolor)
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel(' '.join(cols0))

        cols1Legend = plt.legend(loc=9, ncol=2, prop={'size': fontsize}, fancybox=True, borderaxespad=0.)
        cols1Legend.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color='w')

        # TODO : LOCAL ALFA
        #         ax1v = ax1.twinx()
        #         ax1v.fill_between(s, twissdata['A'], pricing['Volume'], facecolor='#00ffe8', alpha=.4)

        # bottom plot diff
        ax2 = plt.subplot2grid((8, 4), (5, 0), sharex=ax0, rowspan=1, colspan=4, facecolor=mainbg)
        for i, el in enumerate(cols0):
            diff = twissdata1[el].sub(twissdata2[el], fill_value=0)
            if len(twissdata1) > len(twissdata2):
                s = twissdata1['S']
            else:
                s = twissdata2['S']

            ax2.plot(s, diff, ax0colors[i], label=el, linewidth=2)
            ax2.fill_between(s, diff, 0, where=(diff < 0), alpha=0.7, facecolor=negCol, edgecolor=negCol)
            ax2.fill_between(s, diff, 0, where=(diff >= 0), alpha=0.7, facecolor=posCol, edgecolor=posCol)

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.grid(True, color='g')
        ax2.yaxis.label.set_color("w")
        ax2.spines['bottom'].set_color(axspinecolor)
        ax2.spines['top'].set_color(axspinecolor)
        ax2.spines['left'].set_color(axspinecolor)
        ax2.spines['right'].set_color(axspinecolor)
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel(' '.join(['$\Delta${}'.format(k) for k in cols0]))
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

    plt.show()
