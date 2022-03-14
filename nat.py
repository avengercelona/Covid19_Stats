from tkinter import LabelFrame,Label,Frame,Canvas,Scrollbar,TOP,BOTTOM,LEFT,RIGHT,N,E,S,W,X,Y,BOTH,NW
import tkinter.font as tkf
from worldometer_nat import natone
from plotgr import linegr,bargr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def winnat(root,data): # main function
    def close_all():
        for widget in frm2.winfo_children():
            widget.destroy()
        root.quit()
        root.destroy()
        root.grab_release()
        return
    root.protocol('WM_DELETE_WINDOW', close_all)
    gr_list=natone(data[-1]) # getting list data, data[-1] is the hyperlink
    font1 = tkf.Font(family="times",size=16,weight="bold")
    #region frames
    frm1=LabelFrame(root) # country name
    frm1.grid(row=0,column=0,columnspan=2,sticky='nsew')
    Label(frm1,text=data[0],font='times 32 underline').pack()

    frm3=LabelFrame(root,bg='white')#total case
    frm3.grid(row=1,column=0,sticky='we')
    Label(frm3,text=data[1],fg='#00ECFF',bg='white',
    font=font1).pack(side=BOTTOM)
    Label(frm3,text='Total Case',font=font1,bg='white').pack(side=TOP)

    frm4=LabelFrame(root,bg='white')#total death
    frm4.grid(row=2,column=0,sticky='we')
    Label(frm4,text='{} ({}%)'.format(data[2],round(data[2]*100/data[1],2)),
    bg='white',fg='red',font=font1).pack(side=BOTTOM)
    Label(frm4,text='Total Death',
    font=font1,bg='white').pack(side=TOP)

    frm5=LabelFrame(root,bg='white')#total recovery
    frm5.grid(row=3,column=0,sticky='we')
    Label(frm5,text='{} ({}%)'.format(data[3],round(data[3]*100/data[1],2)),
    bg='white',fg='#AAE34D',font=font1).pack(side=BOTTOM)
    Label(frm5,text='Total Recovery',
    font=font1,bg='white').pack(side=TOP)

    frm6=LabelFrame(root,bg='white')#active case
    frm6.grid(row=4,column=0,sticky='we')
    Label(frm6,text='{} ({}%)'.format(data[4],round(data[4]*100/data[1],2)),
    bg='white',fg='#CDCDCD',font=font1).pack(side=BOTTOM)
    Label(frm6,text='Active Cases',
    font=font1,bg='white').pack(side=TOP)

    frm7=LabelFrame(root,bg='white')#total cases per mil
    frm7.grid(row=5,column=0,sticky='we')
    Label(frm7,text=data[5],bg='white',fg='#00ECFF',font=font1).pack(side=BOTTOM)
    Label(frm7,text='Total Cases/1M',font=font1,bg='white').pack(side=TOP)

    frm8=LabelFrame(root,bg='white')#toatl death per mil
    frm8.grid(row=6,column=0,sticky='we')
    Label(frm8,text=data[6],bg='white',fg='red',font=font1).pack(side=BOTTOM)
    Label(frm8,text='Death/1M',font=font1,bg='white').pack(side=TOP)

    frm9=LabelFrame(root,bg='white')#total tests
    frm9.grid(row=7,column=0,sticky='we')
    Label(frm9,text=data[7],bg='white',fg='#00ECFF',font=font1).pack(side=BOTTOM)
    Label(frm9,text='Total Tets',font=font1,bg='white').pack(side=TOP)

    frm10=LabelFrame(root,bg='white')#tests per mil
    frm10.grid(row=8,column=0,sticky='we')
    Label(frm10,text=data[8],bg='white',fg='#CDCDCD',font=font1).pack(side=BOTTOM)
    Label(frm10,text='Test/1M',font=font1,bg='white').pack(side=TOP)

    frm11=LabelFrame(root,bg='white')#population
    frm11.grid(row=9,column=0,sticky='we')
    Label(frm11,text=data[9],bg='white',fg='#CDCDCD',font=font1).pack(side=BOTTOM)
    Label(frm11,text='Population',font=font1,bg='white').pack(side=TOP)
    #endregion
    wrap2=LabelFrame(root,bg='white') # large container for the charts
    wrap2.grid(row=1,column=1,rowspan=9,sticky='nsew')
    cnv=Canvas(wrap2,width=1000,height=500)
    cnv.pack(side=LEFT,fill=BOTH,expand=1)
    frm2=Frame(cnv) # effective frame

    for i in gr_list:
        if 'daily' in i[0].lower():
            fig1=bargr(i[1],i[2],i[0])
        else:
            fig1=linegr(i[1],i[2],i[0])
        cnv1=FigureCanvasTkAgg(fig1, master=frm2)
        cnv1.get_tk_widget().pack(side=TOP,anchor=N)
        cnv1.draw()
    
    scrollbar=Scrollbar(wrap2,command=cnv.yview)
    scrollbar.pack(side=RIGHT,fill=Y)

    cnv.configure(bg='white',yscrollcommand=scrollbar.set) # setting the scrollbar
    cnv.bind("<Configure>",lambda e: cnv.configure(scrollregion=cnv.bbox("all")))
    cnv.create_window((0,0),window=frm2,anchor=NW)

    root.mainloop()