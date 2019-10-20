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

def fraction_of_day(dt):
    midnight = datetime.datetime.combine(datetime.date.today(), datetime.time(0))
    seconds_in_day = 24 * 3600
    if isinstance(dt,datetime.datetime):
        dt = dt - midnight
    return (dt.seconds+dt.microseconds*10**-6)/seconds_in_day


def get_runner(startno):
    sqlcursor.execute("SELECT name.startno, name.starttime , name.name , name.ename , name.intime FROM name WHERE name.startno =" + str(startno) )
    runner = sqlcursor.fetchall();
    return runner[0]

def set_in_time(startno,in_time):
    sqlcursor.execute(
        "UPDATE name SET intime = " + str(in_time) + "WHERE name.startno =" + str(startno))
    cnxn.commit()

# print(get_runner(45))
# test_time = (0.7726620370370371 + 0.757939814814815)/2
# set_in_time(45,test_time)

text_elem = sg.Text("", size=(18, 1))
startinput = sg.Input()
next_runner = 0
next_time = 0
highest = 0
runner_array =[]
time_array=[]
in_time_array =[]
lines_to_display = 10
for ii in range(lines_to_display):
    runner_array.append(sg.Text('',size=(18, 1)))
    time_array.append(sg.Text('',size=(10, 1)))

layout = [[sg.Text("Skriv inn startnummer   (F1 tar tiden)")],
          [startinput]]
layout += [[runner_array[ii],time_array[ii]] for ii in range(lines_to_display)]
layout += [[sg.Button("Avslutt")]]

input_window = sg.Window("Database: " + database, layout, return_keyboard_events=True, use_default_focus=True)

runner_list = []
time_list = []
# ---===--- Loop taking in user input --- #
while True:
    event, value = input_window.Read()
    # text_elem.Update(event)
    print(event, ord(event[0]) , value)
    print(text_elem.DisplayText)
    #if text_elem.DisplayText == 'F1:112':
    if event == 'F1:112':                              # A time should be recorded
        now = datetime.datetime.now()
        time_list.append(now)
        time_string = now.strftime("%H:%M:%S")
        in_time_array.append(time_string)
        print(time_string)
        if next_time < next_runner:    # Start number already entered update time
            this_runner = runner_list[next_time]
            print(this_runner)
            start_number = this_runner.startno
            if this_runner.intime is None:
                set_in_time(this_runner.startno,fraction_of_day(now))
                print('Updating: ', this_runner)
        next_time += 1
        highest = max(next_time, next_runner)-1
    elif ord(event[0]) == 13:                     # A start number has been entered
        runner = get_runner(value[0])
        runner_list.append(runner)
        if next_time > next_runner:    # Start time already recorded - update time
            this_time = time_list[next_runner]
            if runner.intime is None:
                set_in_time(runner.startno, fraction_of_day(now))
                print('updating:', runner)
        next_runner += 1
        startinput.update('')
        highest = max(next_time, next_runner)
        print(runner)
    for line_number in range(lines_to_display):
        if 0 <= highest-line_number < next_time:
            time_array[line_number].update(in_time_array[highest-line_number])
        else:
            time_array[line_number].update('')
        if 0 <= highest-line_number < next_runner:
            runner_array[line_number].update(runner_list[highest-line_number].name)
        else:
            runner_array[line_number].update('')
    if event == "Avslutt" or event is None:
        print(event, "exiting")
        break

