import matplotlib.pyplot as plt
import seaborn as sns

bidmc_deep_blue = '#283891'

def hist_plots(column, title, xaxis, yaxis, save=False, rotate=False):

    plt.figure(figsize=(10,5))
    plt.hist(column, color=bidmc_deep_blue, bins=50)

    plt.title(title, fontsize=18)
    plt.ylabel(xaxis, fontsize=14)
    plt.xlabel(yaxis, fontsize=14);

    if rotate:
        plt.xticks(rotation=45, ha='right')

    if save:
        plt.savefig(title + '.png')
    return

def bar_plots(x, y, title, xaxis, yaxis, order=None, save=False, rotate=False):
    plt.figure(figsize=(10,5))
    ax = sns.barplot(x =x, y=y, color=bidmc_deep_blue, order=order);

    ax.set_title(title, fontsize=18)
    ax.set_ylabel(xaxis, fontsize=14)
    ax.set_xlabel(yaxis, fontsize=14);
    sns.despine()

    if rotate:
        plt.xticks(rotation=45, ha='right')

    if save:
        plt.savefig(title + '.png')
    return

def boxplots(x, y, title, xaxis, yaxis, order=None, save=False, rotate=False):
    plt.figure(figsize=(10,5))
    ax = sns.boxplot(x=x, y=y, color='white', order=order, showfliers=False);

    ax.set_title(title, fontsize=18)
    ax.set_ylabel(xaxis, fontsize=14)
    ax.set_xlabel(yaxis, fontsize=14);
    sns.despine()

    if rotate:
        plt.xticks(rotation=45, ha='right')

    if save:
        plt.savefig(title + '.png')
    return

def lineplots(x, y, title, xaxis, yaxis, save=False, rotate=False):
    plt.figure(figsize=(10,5))
    ax = sns.lineplot(x=x, y=y);

    ax.set_title(title, fontsize=18)
    ax.set_ylabel(xaxis, fontsize=14)
    ax.set_xlabel(yaxis, fontsize=14);
    sns.despine()

    if rotate:
        plt.xticks(rotation=45, ha='right')

    if save:
        plt.savefig(title + '.png')
    return 
