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


def get_runner(startno):
    sqlcursor.execute("SELECT name.starttime , name.name , name.ename , name.intime FROM name WHERE name.startno =" + str(startno) )
    runner = sqlcursor.fetchall();
    return runner

def set_in_time(startno,in_time):
    sqlcursor.execute(
        "UPDATE name SET intime = " + str(in_time) + "WHERE name.startno =" + str(startno))
    cnxn.commit()

# print(get_runner(45))
# test_time = (0.7726620370370371 + 0.757939814814815)/2
# set_in_time(45,test_time)

text_elem = sg.Text("", size=(18, 1))
startinput = sg.Input()

layout = [[sg.Text("Skriv inn startnummer   (F1 tar tiden)")],
          [startinput],
          #[text_elem],
          [sg.Button("Avslutt")]]

input_window = sg.Window("Database: " + database, layout, return_keyboard_events=True, use_default_focus=True)

highest_runner = 0
highest_time = 0
highest = 0
lines_to_display = 10

# ---===--- Loop taking in user input --- #
while True:
    event, value = input_window.Read()

    # text_elem.Update(event)
    print(event, ord(event[0]) , value)
    print(text_elem.DisplayText)
    #if text_elem.DisplayText == 'F1:112':
    if event == 'F1:112':
        now = datetime.datetime.now()
        time_string = now.strftime("%H:%M:%S")
        in_time_array[highest_time] = time_string
        highest_time += 1
        highest = max(highest_time,highest_time)
        print(time_string)
    if ord(event[0]) == 13:
        runner = get_runner(value[0])
        runner_array[highest_runner] = runner
        highest_runner += 1
        startinput.update('')
        highest = max(highest_time, highest_time)
        print(runner)
    if event == "Avslutt" or event is None:
        print(event, "exiting")
        break

