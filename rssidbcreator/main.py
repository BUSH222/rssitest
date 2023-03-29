import tkinter as tk
from tkinter import filedialog
import json
import os
import shutil
import itertools

def openselector(usedatapath=None):
    cnt = 1
    activeelement = None
    values = {}
    def modifylist(lst, action, data=None):
        nonlocal cnt, values, activeelement
        if action == '+':
            lst.insert(tk.END, f'Place {cnt}')
            values[f'Place {cnt}'] = [0, 0, None, None, None, None, {}]
            cnt += 1
        elif action == '-':
            if lst.get(tk.ACTIVE) == '':
                return
            a1 = lst.get(tk.ACTIVE)
            if a1 == activeelement:
                activeelement = None
                namelabel.config(text='Nothing selected')
            a = lst.get(0, tk.END).index(a1)
            lst.delete(a)
            del values[a1]
        elif action == '+c':
            lst.insert(tk.END, f'Place {cnt}')
            values[f'Place {cnt}'] = [0, 0, None, None, None, None, data]
            cnt += 1


    def set_text(e, text):
        e.delete(0,tk.END)
        e.insert(0,text)
        return
    
    def save():
        try:
            values[activeelement][0] = int(xentry.get())
            values[activeelement][1] = int(yentry.get())
            bsave.config(text='Saving Successful!')
        except Exception as e:
            bsave.config(text='Saving Failed!')

    def getelement(lst):
        nonlocal activeelement
        activeelement = lst.get(tk.ACTIVE)
        if activeelement == '' or activeelement is None:
            return
        
        namelabel.config(text=f'{activeelement} selected')
        bsave.config(text='Save')
        
        if values[activeelement] != {}:
            k = values[activeelement][6]['NUM']
            numlabel.config(text=f'NUM: {k}')

        set_text(xentry, values[activeelement][0])
        set_text(yentry, values[activeelement][1])
        for i in range(len(filebuttons)):
            if values[activeelement][2+i] is None:
                filebuttons[i].config(text=f'File {i+1} not selected')
            else:
                k = values[activeelement][2+i].split('/')[-1]
                filebuttons[i].config(text=f'{k} selected')
    
    def selectfile(fileindex, filebutton):
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = [("MP3","*.mp3")])
        if filename != '' and activeelement is not None:
            k = filename.split('/')[-1]
            values[activeelement][2+fileindex] = filename
            filebutton.configure(text=f'{k} selected')
    
    def export():
        savedir = filedialog.askdirectory(title='Select directory to save results')
        if savedir != '' and savedir is not None:
            directory = savedir+'/data/'
            tocopy = []
            for s in list(itertools.chain.from_iterable(values.values())):
                if isinstance(s, str):
                    tocopy.append(s)
            
            os.makedirs(directory)
            os.makedirs(directory+'audio/')
            for s in tocopy:
                shutil.copy(s, directory+'audio/')
            
            exportdict = {}

            for k, v in values.items():
                g = []
                for i in range(len(v)):
                    if isinstance(v[i], str) and v is not None:
                        g.append(v[i].split('/')[-1])
                    else:
                        g.append(v[i])
                exportdict[k] = g

            with open(f'{directory}data.json', 'w') as f:
                json.dump(exportdict, f)
            
            shutil.make_archive(directory[:-1], 'zip', directory)
            shutil.rmtree(directory)


    def importrssis():

        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = [("TXT","*.txt")])
        with open(filename, 'r') as f:
            g = [json.loads(q) for q in [s.strip() for s in f.readlines()]]
        for k in g:
            modifylist(mylist, '+c', data=k)
            
            
    
    w = tk.Tk()
    w.title('database creator')
    w.resizable(0, 0)
    w.geometry('500x280')
    scrollbar = tk.Scrollbar(w)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    mylist = tk.Listbox(w, yscrollcommand=scrollbar.set)

    mylist.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command = mylist.yview)

    bplus = tk.Button(w, text='+', command=lambda: modifylist(mylist, '+'))
    bplus.place(x=185, y=20)
    bminus = tk.Button(w, text='-', command=lambda: modifylist(mylist, '-'))
    bminus.place(x=260, y=20)

    bget = tk.Button(w, text='Get Selection', command=lambda: getelement(mylist))
    bget.place(x=185, y=50)
    bsave = tk.Button(w, text='Save', command=lambda: save(), height=3, width=16)
    bsave.place(x=300, y=20)


    namelabel = tk.Label(w, text='Nothing selected')
    namelabel.place(x=270, y=80)

    numlabel = tk.Label(w, text='NUM: None')
    numlabel.place(x=190, y=105)

    xentry = tk.Entry(w)
    xentry.place(x=205, y=160, width=50)
    yentry = tk.Entry(w)
    yentry.place(x=205, y=190, width=50)
    xlabel = tk.Label(w, text='x:')
    xlabel.place(x=185, y=160)
    ylabel = tk.Label(w, text='y:')
    ylabel.place(x=185, y=190)

    filebutton1 = tk.Button(w, text='File 1 not selected', command=lambda:selectfile(0, filebutton1), height=1, width=20)
    #filebutton2 = tk.Button(w, text='File 2 not selected', command=lambda:selectfile(1, filebutton2), height=1, width=20)
    #filebutton3 = tk.Button(w, text='File 3 not selected', command=lambda:selectfile(2, filebutton3), height=1, width=20)
    #filebutton4 = tk.Button(w, text='File 4 not selected', command=lambda:selectfile(3, filebutton4), height=1, width=20)
    filebuttons = [filebutton1]#, filebutton2, filebutton3, filebutton4]
    filebutton1.place(x=265, y=100)
    #filebutton2.place(x=265, y=130)
    #filebutton3.place(x=265, y=160)
    #filebutton4.place(x=265, y=190)

    exportbutton = tk.Button(w, text='Export to file', command=lambda:export(), height=1, width=29)
    exportbutton.place(x=185, y=220)

    exportbutton = tk.Button(w, text='Import rssi data', command=lambda:importrssis(), height=1, width=29)
    exportbutton.place(x=185, y=250)
    w.mainloop()

openselector()