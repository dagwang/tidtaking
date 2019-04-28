import csv
import datetime
from tkinter import *

#                          - PARAMETERE -
filename = "EksportAvOCC2017KveldenFør.csv"   # Datafil for import
nlines = 5                    # Antall løpere som skal vises
courses = ['1','2','3']       # Løype som skal vises (NB: Tekst ikke tall)
opprop = datetime.timedelta(hours=6) # Tidsforkyvning for oppropstid

#                         - DATAIMPORT -
# Hent alle løpere fra CSV fil og legg i listen alle
# CSV fil må være eksportert som med utf-8 encoding
# TODO: Les direkte fra excel
fields = ['name', 'ename', 'class', 'team', 'cource', 'gender', 'startno', 'ecard', 'starttime', 'kid', 'unknown1', 'unknown2', 'unknown3', 'unknown4', 'unknown5']
with open(filename, newline='', encoding='utf-8') as csvfile:
    etimereader = csv.DictReader(csvfile, dialect='excel', delimiter=';',  fieldnames=fields)
    alle =[]
    for row in etimereader:
     #   print(row)
        alle.append(row)

# Plukk ut løpere kun fra den eller de løypene som skal vises
list = []
for rad in alle:
    if rad['cource'] in courses:
        list.append(rad)

# Sorter på starttid
list.sort(key=lambda x: x['starttime'])

# Lag en egen liste med starttider som datetime
starttimes = [datetime.datetime.fromisoformat(datetime.date.today().__str__()+' '+rad['starttime']) for rad in list]

# Definisjon av oppdateringer som gjøres hvert sekund
# TODO: Unngå at den teller hele listen hver gang
# TODO: Lyd
def tick():
    now = datetime.datetime.now() + opprop
    ii = 0
    time_string = now.strftime("%H:%M:%S")
    clock.config(text='Oppropstid:  ' + time_string)
    while now >= (starttimes[ii]):                # Spol til riktig linje
        ii += 1
     #  print(ii ,now , starttimes[ii])

    for jj in range(nlines):
        name[jj].config(text=list[ii+jj]['name']+' '+list[ii+jj]['ename'])
        tid[jj].config(text=starttimes[ii+jj].strftime("%H:%M:%S   "))
        diff[jj].config(text=(datetime.datetime.min + (starttimes[ii+jj]-now)).strftime("%M:%S"))
    clock.after(1000, tick)


#              -    OPPSETT GUI   -
root = Tk()
clock = Label(root, font=("times", 50, "bold"), bg="white")
clock.grid(row=0, column=2)
fileinfo = Label(root, font=("times", 12, "bold"), bg="white")
fileinfo.grid(row=0, column=3)
fileinfo.config(text=filename)
courseinfo = Label(root, font=("times", 12, "bold"), bg="white")
courseinfo.grid(row=0, column=1)
courseinfo.config(text='Løype(r): '+courses.__str__())
name = [Label(root, font=("times", 50, "bold"), bg="white")]
tid = [Label(root, font=("times", 50, "bold"), bg="white")]
diff = [Label(root, font=("times", 50, "bold"), bg="white")]
for ii in range(nlines):
    if ii >= 1:
        name.append(Label(root, font=("times", 50, "bold"), bg="white"))
        tid.append(Label(root, font=("times", 50, "bold"), bg="white"))
        diff.append(Label(root, font=("times", 50, "bold"), bg="white"))
    name[ii].grid(row=ii+1, column=2)
    name[ii].config(text='Navn')
    tid[ii].grid(row=ii+1,column=1)
    tid[ii].config(text='Tid')
    diff[ii].grid(row=ii+1,column=3)
    diff[ii].config(text='diff')

#     Kjør program
tick()
root.mainloop()
