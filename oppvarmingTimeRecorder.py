import PySimpleGUI as sg
import pyodbc
import datetime

#                        SETUP database communication
database = 'SQLtest_2019'
username = 'emit'
password = 'time'
server = 'BASE'
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
sqlcursor = cnxn.cursor()



def getrunner(startno):
    sqlcursor.execute("SELECT name.starttime , name.name , name.ename , name.intime FROM name WHERE name.startno =" + str(startno) )
    runner = sqlcursor.fetchall();
    return runner

print(getrunner(48))


text_elem = sg.Text("", size=(18, 1))
startinput = sg.Input()

layout = [[sg.Text("Skriv inn startnummer   (F1 tar tid)")],
          [startinput],
          [text_elem],
          [sg.Button("Avslutt")]]

window = sg.Window("Keyboard Test", layout,  return_keyboard_events=True, use_default_focus=True)

# ---===--- Loop taking in user input --- #
while True:
    event, value = window.Read()

    text_elem.Update(event)
    print(event, ord(event[0]) , value)
    print(text_elem.DisplayText)
    #if text_elem.DisplayText == 'F1:112':
    if event == 'F1:112':
        now = datetime.datetime.now()
        time_string = now.strftime("%H:%M:%S")
        print(time_string)
    if ord(event[0]) == 13:
        loper = getrunner(value[0])
        startinput.update('')
        print(loper)
    if event == "Avslutt" or event is None:
        print(event, "exiting")
        break

