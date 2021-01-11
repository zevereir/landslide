import numpy as np
import matplotlib.pyplot as plt
import datetime

from numpy.distutils.system_info import f2py_info


def data_abstraction(begin,end, ignore=[], name="responsive_scores.dat"):
    """"
    Deze functie groepeert de scores die gegeven zijn aan elke presentatie en vat deze samen in 2 plots.
    De eerste plot toont de gemiddeldes per archetype en het aantal slides per archetype, de tweede toont de vooruitgang
    in tijd die gemaakt is over de hele dataset. Het gemiddelde is het gewogen gemiddelde van alle slides"""
    set_output="D:\\Thesis\\landslide\\data\\american"
    names=["Titeldia","Titel Dubbele Inhoud","Titel Enkele Inhoud","Titel Tripel Inhoud","Achtergrond Quote","Vergelijking","Enkel Titel","Inhoud met Onderschrift","Enkel Inhoud","Sectiehoofd","Enkel Achtergrond"]
    count={}
    responsive_count={}
    for i in range(0,len(names)):
        count[i]=(0,0)
        responsive_count[i]=(0,0)

    for data_index in range(begin,end):
        if data_index not in ignore:
            print(data_index)
            output_directory = set_output+"\\"+ str(data_index) + "_data"
            #data = np.loadtxt(output_directory+"\\scores.dat")
            responsive_data = np.loadtxt(output_directory + "\\"+name)
            try:
                if len(responsive_data[0])==2:
                    #scores = data[:, 0]
                    responsive_scores = responsive_data[:, 0]
                    archetypes = responsive_data[:, 1]
            except:
                #scores=[data[0]]
                responsive_scores = [responsive_data[0]]
                archetypes = [responsive_data[1]]

            for i in range(0,len(responsive_scores)):
                index=archetypes[i]
                tup=count[index]
                resp_tup=responsive_count[index]
                #new_tup=(tup[0]+1,tup[1]+scores[i])
                new_resp_tup=(resp_tup[0]+1,resp_tup[1]+responsive_scores[i])
                #count[index]=new_tup
                responsive_count[index]=new_resp_tup
    means=[0 for i in range(0,len(names))]
    resp_means = [0 for i in range(0, len(names))]
    totals=[0 for i in range(0,len(names))]
    for i in count:
        # means[i]=count[i][1]/max(count[i][0],1)
        totals[i]=count[i][0]
        resp_means[i]=responsive_count[i][1]/max(count[i][0],1)

    f=plt.figure(figsize=(12,5))
    (ax2,ax3) = f.subplots(1, 3)


    # ax1.bar(names, means)
    # ax1.set_title('Gemiddeld behoud van informatie')
    # ax1.set_ylim([0,1.1])
    # ax1.set(ylabel="% behoud informatie")
    ax2.bar(names, resp_means)
    ax2.set_title('Gemiddelde responsiviteit')
    ax2.set_ylim([0, 1.1])
    ax2.set(ylabel="% responsiviteit")
    rects = ax3.bar(names,totals)
    autolabel(rects,ax3)
    ax3.set_title('Verdeling dataset over archetypes')
    ax3.set_ylim([0,12000])

    # for tick in ax1.get_xticklabels():
    #     tick.set_rotation(90)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(90)
    for tick in ax3.get_xticklabels():
        tick.set_rotation(90)

    f.show()
    f.savefig(set_output+"\\means_and_counts.png")
    # mean=0
    # total_amount=0
    # for i in range(0,len(means)):
    #     mean+=means[i]*totals[i]
    #     total_amount+=totals[i]
    # mean=mean/total_amount  #0.828201
    # print("Behoud van informatie:", mean)
    # data = np.column_stack((mean, str(datetime.datetime.now())))
    # with open('D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\total_accuracy.dat', 'ab') as set_mean_file:
    #     np.savetxt(set_mean_file, data, fmt="%s")
    mean = 0
    total_amount = 0
    for i in range(0, len(means)):
        mean += resp_means[i] * totals[i]
        total_amount += totals[i]
    mean = mean / total_amount
    print("Responsiviteit:",mean) #0.41188746559054
    #get_score_chart()

def get_score_chart():
    """"
    De functie die de 2de plot opbouwt"""
    data = np.loadtxt('D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\total_accuracy.dat',
                      dtype='str')
    dates = data[:, 1]
    scores = [float(x) for x in data[:, 0]]

    x = range(1, len(scores) + 1)
    fig, ax = plt.subplots()
    ax.plot(x, scores)
    plt.xticks(x, dates)
    plt.ylabel("Gemiddelde % behoud informatie")
    plt.xlabel("Datum")
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    plt.show()
    fig.savefig('D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\pdf_data_usa\\total_accuracy.png')
    plt.close(fig)

def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

data_abstraction(1,841,name="learned.dat")