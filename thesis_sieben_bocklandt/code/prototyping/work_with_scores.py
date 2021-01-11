import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
def work_with_scores(scores, archetypes, output_directory,name_output="responsive_scores.dat", make_images=True):
    """Slaat de scores op in de jusite file en maakt er een plot van"""
    save_data(scores,archetypes,output_directory, name_output)
    if make_images:
        get_score_chart(scores,output_directory)

def get_score_chart(scores,output_directory):
    x=range(1,len(scores)+1)
    fig, ax = plt.subplots()
    ax.scatter(x,[score[0] for score in scores])
    plt.xticks(x)
    plt.grid(axis='x')
    if len(x)>10:
        plt.gca().margins(x=0)
        plt.gcf().canvas.draw()
        tl = plt.gca().get_xticklabels()
        maxsize = max([t.get_window_extent().width for t in tl])
        m = 0.5  # inch margin
        s = maxsize / plt.gcf().dpi * len(scores)+1 + 2 * m
        margin = m / plt.gcf().get_size_inches()[0]+0.03

        plt.gcf().subplots_adjust(left=margin, right=1. - margin)
        plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

    ax.set_ylim([-0.05, 1.1])
    ax.margins(0.05, 0.05)
    for tick in ax.get_xticklabels():
        tick.set_rotation(-90)
    plt.xlabel("Dlidenummer")
    plt.ylabel("% behoud informatie")
    fig.savefig(output_directory+"\\scores.png")
    plt.close(fig)

    x = range(1, len(scores) + 1)
    fig, ax = plt.subplots()
    ax.scatter(x, [score[1] for score in scores])
    plt.xticks(x)
    plt.grid(axis='x')
    if len(x) > 10:
        plt.gca().margins(x=0)
        plt.gcf().canvas.draw()
        tl = plt.gca().get_xticklabels()
        maxsize = max([t.get_window_extent().width for t in tl])
        m = 0.5  # inch margin
        s = maxsize / plt.gcf().dpi * len(scores) + 1 + 2 * m
        margin = m / plt.gcf().get_size_inches()[0]+0.03

        plt.gcf().subplots_adjust(left=margin, right=1. - margin,)
        plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

    ax.set_ylim([-0.05, 1.1])
    ax.margins(0.05, 0.05)
    for tick in ax.get_xticklabels():
        tick.set_rotation(-90)
    plt.ylabel("% responsiviteit")
    plt.xlabel("Dianummer")
    fig.savefig(output_directory + "\\responsieve_scores.png")
    plt.close(fig)

def save_data(scores,archetypes,output_directory,name_output):
    # y_data=[i.internal_id for i in archetypes]
    # data = np.column_stack(([score[0] for score in scores], y_data))
    # header = "Score, Archetype-ID"
    # np.savetxt(output_directory+"\\scores.dat", data, header=header)
    if ".dat" not in name_output:
        name_output+=".dat"
    y_data = [i.internal_id for i in archetypes]
    data = np.column_stack(([score[1] for score in scores], y_data))
    header = "Responsive score, Archetype-ID"
    output_directory.mkdir(exist_ok=True)
    if not (output_directory/name_output).is_file():
        Path.touch(output_directory/name_output)
    np.savetxt(output_directory/name_output, data, header=header)

