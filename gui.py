from tkinter import *
from tkinter import ttk
import time as t
from worldometer_nat import *
from plotgr import *
from nat import winnat
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def loadata():
    print("Loading data...")
    st=t.time()#time stamp
    global Name,Tot_Cases,New_Cases,Tot_Death,New_Death,Tot_Recov,Actv_Cases
    Name,Tot_Cases,New_Cases,Tot_Death,New_Death,Tot_Recov,Actv_Cases=extract_wr()#importing variables(continents)
    print('continental data loaded in: ',t.time()-st,'sec')#time stamp
    st=t.time()
    global name_list,tcase,tdeath,trecov,acases,tcasepm,deathpm,ttest,testpm,pop,hypr
    name_list,tcase,tdeath,trecov,acases,tcasepm,deathpm,ttest,testpm,pop,hypr=extract_nat()#importing variables(countries)
    print('international data loaded in: ',t.time()-st,'sec')#time stamps
loadata()
#========================functions========================
def view_tab(ref=Tot_Cases,s='Total Cases'):
    tv.delete(*tv.get_children())
    lb1.configure(text='Sorting by: {}'.format(s))
    c=0
    for i in sorted(ref.items(),key = lambda kv:(kv[1], kv[0]),reverse=True):
        key=i[0]
        if c%2==0:
            t='e'
        else:
            t='o'
        tup=(key,Tot_Cases[key],New_Cases[key],Tot_Death[key],New_Death[key],Tot_Recov[key],Actv_Cases[key])
        tv.insert('','end',values=tup,tags=(t,))
        c+=1
def view_tab2(ref=tcase,s='Total Cases'):
    tv2.delete(*tv2.get_children())
    lb2.configure(text='Sorting by: {}'.format(s))
    global canframe2
    for widget in canframe2.winfo_children():
        widget.destroy()
    c=0
    for i in sorted(ref.items(),key = lambda kv:(kv[1], kv[0]),reverse=True):
        key=i[0]
        if c%2==0:
            t='e'
        else:
            t='o'
        tup=(c+1,key,tcase[key],tdeath[key],trecov[key],acases[key],tcasepm[key],deathpm[key],ttest[key],testpm[key],pop[key])
        tv2.insert('','end',values=tup,tags=(t,))
        c+=1
    barfig=barhorz(ref)
    canvas2 = FigureCanvasTkAgg(barfig, master=canframe2)
    canvas2.get_tk_widget().pack()
    canvas2.draw()
def refr():
    loadata()
    view_tab()
    view_tab2()
def close_all():
    scrn1.quit()
    scrn1.destroy()
def OnDoubleClick(event):
    key = tv2.item(tv2.focus())['values'][1]
    tp=(key,tcase[key],tdeath[key],trecov[key],acases[key],
    tcasepm[key],deathpm[key],ttest[key],testpm[key],pop[key],hypr[key])
    print("you clicked on", key)
    scrn2=Toplevel(scrn1)
    scrn2.grab_set() # when you show the popup
    winnat(scrn2,tp)
    #scrn2.grab_release() # to return to normal
#========================screens==========================
scrn1=Tk()
scrn1.title('Covid 19 Continental Live Stats')
scrn1.state('zoomed')
scrn1.resizable(False, False)
scrn1.protocol('WM_DELETE_WINDOW', close_all)

bgimg=PhotoImage(file='take2.2.png')#backgrd
Label(scrn1,image=bgimg).place(relwidth=1,relheight=1)

style = ttk.Style()#treeview styles
style.configure("mystyle.Treeview.Heading",font=('times new roman', 12,'bold','italic','underline'))
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
#region==================1st frames=======================
frm1=LabelFrame(scrn1)
frm1.place(x=20,y = 100,width=1330,height=310)

canframe1=LabelFrame(frm1)#frame for chart canvas
canframe1.pack(side=RIGHT,anchor=SE)
canframe1.configure(bd=0,cursor='dot',relief=RIDGE)

#canvas for pie
piefig=pie1(list(Tot_Cases.values())[1:],list(Tot_Death.values())[1:],list(Tot_Cases.keys())[1:])
canvas1 = FigureCanvasTkAgg(piefig, master=canframe1)
canvas1.get_tk_widget().pack(side=RIGHT)
canvas1.draw()
#========================widgets==========================
hd1=Label(frm1,text='Continents',font='times 30 underline')#heading
lb1=Label(frm1,text='Sorting by: Total Cases',bg='white')#sorting field
bt_refr=Button(frm1,text='Refresh',command=refr)#refresh button
#region table1
tv=ttk.Treeview(frm1, columns=(1,2,3,4,5,6,7),show='headings',style="mystyle.Treeview")
tv.heading(1,text='Name',anchor='w')
tv.column(1,width=100,minwidth=100)
tv.heading(2,text='Total Cases',anchor='e',command=lambda:view_tab(Tot_Cases,'Total Cases'))
tv.column(2,width=100,anchor='e',minwidth=100,stretch=NO)
tv.heading(3,text='New Cases',anchor='e',command=lambda:view_tab(New_Cases,'New Cases'))
tv.column(3,width=100,anchor='e',minwidth=100,stretch=NO)
tv.heading(4,text='Total Deaths',anchor='e',command=lambda:view_tab(Tot_Death,'Total Deaths'))
tv.column(4,width=100,anchor='e',minwidth=100,stretch=NO)
tv.heading(5,text='New deaths',anchor='e',command=lambda:view_tab(New_Death,'New Deaths'))
tv.column(5,width=100,anchor='e',minwidth=100,stretch=NO)
tv.heading(6,text='Total recovery',anchor='e',command=lambda:view_tab(Tot_Recov,'Total Recovery'))
tv.column(6,width=100,anchor='e',minwidth=100,stretch=NO)
tv.heading(7,text='Active cases',anchor='e',command=lambda:view_tab(Actv_Cases,'Active Cases'))
tv.column(7,width=100,anchor='e',minwidth=100,stretch=NO)
view_tab(Tot_Cases)
tv.tag_configure('o', background='#EEEEEE')
tv.tag_configure('e', background='#BAFFFF')
#endregion
#========================placing of widgets===============
hd1.place(x=665,y=0,anchor=N)
bt_refr.place(x=240,y=20+30,anchor=W)
lb1.place(x=5,y=20+30,anchor=W)
tv.pack(side=LEFT,anchor=SW,expand=True,fill=X,padx=5,pady=5)
#endregion
#region==================2nd frames=======================
wrap2=LabelFrame(scrn1,width=1330,height=325)
wrap2.place(x=20,y = 415)

tree_scroll=Scrollbar(wrap2,orient=HORIZONTAL)#horz scroll bar for treeview
tree_scroll.pack(side=BOTTOM,fill=X)

cnv=Canvas(wrap2,width=1322-16,height=320-16)
cnv.pack(side=LEFT,fill=BOTH,expand=1)
frm2=Frame(cnv)#effective frame(2nd)

scrollbar=Scrollbar(wrap2,command=cnv.yview)#vertical scrolbar for entire frame2
scrollbar.pack(side=RIGHT,fill=Y)

cnv.configure(bg='white',yscrollcommand=scrollbar.set)
cnv.bind("<Configure>",lambda e: cnv.configure(scrollregion=cnv.bbox("all")))
cnv.create_window((0,0),window=frm2,anchor=NW)

hd2=Label(frm2,text='Countries',font='times 30 underline')#heading
hd2.grid(row=0,column=0,columnspan=2)

lb2=Label(frm2,text='Sorting by: Total Cases',bg='white')#sorting field
lb2.place(x=1,y=30,anchor=W)

tabfrm=LabelFrame(frm2,height=500,width=772,bd=0)#frame for treeview
tabfrm.grid(row=1,column=0,sticky='n')

canframe2=LabelFrame(frm2,bd=0)#frame for canvas
barfig=barhorz(tcase)#chart figure
canvas2 = FigureCanvasTkAgg(barfig, master=canframe2)
canvas2.get_tk_widget().pack()
canvas2.draw()
canframe2.grid(row=1,column=1,sticky='nw')
#region table2
tv2=ttk.Treeview(tabfrm,height=21,xscrollcommand=tree_scroll.set,
columns=(0,1,2,3,4,5,6,7,8,9,10),show='headings',style="mystyle.Treeview")
tv2.heading(0,text='#',anchor='w')
tv2.column(0,width=15)
tv2.heading(1,text='Name',anchor='w')
tv2.column(1,width=100)
tv2.heading(2,text='Total Cases',anchor='e',command=lambda:view_tab2(tcase,'Total Cases'))
tv2.column(2,width=100,anchor='e')
tv2.heading(3,text='Total Death',anchor='e',command=lambda:view_tab2(tdeath,'Total Deaths'))
tv2.column(3,width=100,anchor='e')
tv2.heading(4,text='Total Recovered',anchor='e',command=lambda:view_tab2(trecov,'Total Recovered'))
tv2.column(4,width=100,anchor='e')
tv2.heading(5,text='Active Cases',anchor='e',command=lambda:view_tab2(acases,'Active Cases'))
tv2.column(5,width=100,anchor='e')
tv2.heading(6,text='Cases/ 1M',anchor='e',command=lambda:view_tab2(tcasepm,'Cases/1M'))
tv2.column(6,width=100,anchor='e')
tv2.heading(7,text='Deaths/ 1M',anchor='e',command=lambda:view_tab2(deathpm,'Deaths/1M'))
tv2.column(7,width=100,anchor='e')
tv2.heading(8,text='Total Tests',anchor='e',command=lambda:view_tab2(ttest,'Total Tests'))
tv2.column(8,width=100,anchor='e')
tv2.heading(9,text='Tests/ 1M',anchor='e',command=lambda:view_tab2(testpm,'Tests/1M'))
tv2.column(9,width=100,anchor='e')
tv2.heading(10,text='Population',anchor='e',command=lambda:view_tab2(pop,'Population'))
tv2.column(10,width=100,anchor='e')
tree_scroll.config(command=tv2.xview)
view_tab2()
tv2.bind("<Double-1>", OnDoubleClick) # double click
tv2.tag_configure('o', background='#EEEEEE')
tv2.tag_configure('e', background='#BAFFFF')
#endregion
tv2.place(x=0,y=0,height=480,width=770)
#endregion
scrn1.mainloop()