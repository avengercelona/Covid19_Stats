import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Wedge

def pie1(x1,x2,y=['']*6):
    plt.style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(5.5,3),squeeze=True)

    wedgelist=[Wedge((0, 0), 0.5, 0, 30,width=.2),
    Wedge((0, 0), 0.5, 0, 30,width=.2,ls='--',ec='white',hatch='//')]#patches for legends
    
    autotexts=ax.pie(x1,explode=[0.085]*6,#the pie chart (outer)
    shadow=True,radius=1,
    autopct='%1.1f%%',
    pctdistance=0.87,labels=y,
    textprops={'size': 8},
    wedgeprops={'edgecolor':'white','width':.25})[2]
    plt.setp(autotexts, size=8,weight='bold',rotation=27)#setting up the autotexts

    autotexts2=ax.pie(x2,explode=[0.085]*6,#the pie chart (inner)
    shadow=True,radius=0.65,
    autopct='%1.1f%%',
    pctdistance=0.80,
    wedgeprops={'width':.3,'ec':'white','ls':'--','hatch':'/'})[2]
    plt.setp(autotexts2, size=8,rotation=27)#setting up the autotexts

    fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
    hspace = 0, wspace = 0)#adjusting placement of figure
    ax.bbox_inches = 'tight'
    ax.pad_inches=0
    
    ax.legend(wedgelist,['Total Cases','Total Deaths'],fontsize='x-small',loc='center right',bbox_to_anchor=(1.4, 0.7))
    return fig

def barhorz(dic):
    x,y=list(dic.keys()),list(dic.values())
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(5.5,4.8),squeeze=True)

    rect=ax.barh(x,y,align='center')#bar chart of countries
    def autolabel(rects):#labels for the bar chart of countries
        i=0
        for rect in rects:
            ax.annotate('{},{}'.format(rect.get_width(),list(dic.keys())[i]),
            xy=(rect.get_width(),rect.get_y()+rect.get_height()),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='left', va='center')
            i+=1
    autolabel(rect)

    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Population in mill.')
    plt.subplots_adjust(left=0.0, right=0.835, bottom=0.0, top=1.0,wspace=0,hspace=0)
    plt.yticks(rotation=30)
    
    return fig

def linegr(dates,data,hd):
    fig,ax = plt.subplots(figsize=(8,4.8),tight_layout=True)
    ax.plot(dates,data,'c') # line graph plot for total counts

    ax.set_title(hd,font='times new roman',size=20)
    ax.set_ylabel('Population affected',size=11)

    tiklist=['']*len(dates)
    for i in range(0,len(dates),len(dates)//10):
        tiklist[i]=dates[i]
    tiklist[-1]=dates[-1]

    ax.xaxis.set_ticks(tiklist)
    for tick in ax.get_xticklabels():
        tick.set_rotation(70)
    fig.align_labels()

    return fig

def bargr(dates,data,hd):
    fig,ax = plt.subplots(figsize=(8,4.8),tight_layout=True)
    ax.bar(dates,data,color='#FF7C00') # bar graph for daily counts

    ax.set_title(hd,font='times new roman',size=20)
    ax.set_ylabel('Population affected',size=11)

    tiklist=['']*len(dates)
    for i in range(0,len(dates),len(dates)//10):
        tiklist[i]=dates[i]
    tiklist[-1]=dates[-1]

    ax.xaxis.set_ticks(tiklist)
    for tick in ax.get_xticklabels():
        tick.set_rotation(70)
    fig.align_labels()

    return fig