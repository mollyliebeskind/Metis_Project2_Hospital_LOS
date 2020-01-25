import matplotlib.pyplot as plt
import seaborn as sns

bidmc_deep_blue = '#283891'

def hist_plots(column, title, xaxis, yaxis, save=False):

    plt.figure(figsize=(10,5))
    plt.hist(column, color=bidmc_deep_blue)

    plt.title(title, fontsize=18)
    plt.ylabel(xaxis, fontsize=14)
    plt.xlabel(yaxis, fontsize=14);
    return

def bar_plots(x, y, title, xaxis, yaxis, order=None, save=False):
    plt.figure(figsize=(10,5))
    ax = sns.barplot(x =x, y=y, color=bidmc_deep_blue, order=order);

    ax.set_title(title, fontsize=12)
    ax.set_ylabel(xaxis, fontsize=12)
    ax.set_xlabel(yaxis, fontsize=12);
    sns.despine()

    if save:
        plt.savefig(title + '.png')

def boxplots(x, y, title, xaxis, yaxis, order=None, save=False):
    plt.figure(figsize=(10,5))
    ax = sns.boxplot(x=x, y=y, color='white', order=order, showfliers=False);

    ax.set_title(title, fontsize=12)
    ax.set_ylabel(xaxis, fontsize=12)
    ax.set_xlabel(yaxis, fontsize=12);
    sns.despine()

    if save:
        plt.savefig(title + '.png')
