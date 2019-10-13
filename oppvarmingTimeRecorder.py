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

# Recipe for getting keys, one at a time as they are released
# If want to use the space bar, then be sure and disable the "default focus"

text_elem = sg.Text("", size=(18, 1))

layout = [[sg.Text("Press a key or scroll mouse")],
          [sg.Input(), sg.FileBrowse()],
          [text_elem],
          [sg.Button("OK")]]

window = sg.Window("Keyboard Test", layout,  return_keyboard_events=True, use_default_focus=False)

# ---===--- Loop taking in user input --- #
while True:
    event, value = window.Read()
    loper = getrunner(value[1])
    print(loper)
    text_elem.Update(event)
    print(value)
    print(text_elem.DisplayText)
    if text_elem.DisplayText == 'F1:112':
        now = datetime.datetime.now()
        time_string = now.strftime("%H:%M:%S")
        print(time_string)
    if event == "OK" or event is None:
        print(event, "exiting")
        break

