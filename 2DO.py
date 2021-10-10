from tkinter import *
from tkinter import ttk
import pickle
from datetime import datetime
from tkcalendar import *
import babel.numbers
import tkcalendar.calendar_
from tkinter.font import Font
import itertools
from random import randint, seed
import smtplib
from email.message import EmailMessage
from texts import password, welcome

# -----COLORS----------------------------------------------------
main_color = '#5c454e'
light_main_color = '#8f6d7a'
secondary_color = '#d4e1e8'
secondary_dark_color = '#6d828f'


# -----MAIN WINDOW AND STYLE----------------------------------------
window = Tk()
window.title('2DO')
icon = 'C:\\Users\\Administrator\\Desktop\\ToDo projektas\\2DO.ico'
window.iconbitmap(icon)
window.geometry('950x710')
window.resizable(False, False)
window.config(bg=main_color)

style = ttk.Style()
style.theme_use('clam')

big_font = Font(
    family="Verdana",
	size=15,
	weight="bold")

mid_font = Font(
    family="Verdana",
	size=11,
	weight="bold")


# -----FRAMES-----------------------------------------------------
top = Frame(window, height=500, bg=main_color)
mid = Frame(window)
bottom = Frame(window)
top.pack(fill=BOTH)
mid.pack()
bottom.pack()


# -----FUNCTIONS---------------------------------------------------
def get_added_tasks():
    '''Opens file with static added task list'''
    try:
        with open("added_tasks.pkl", "rb") as pickle_in:
            added_tasks = pickle.load(pickle_in)
    except:
        added_tasks = []
    return added_tasks


def save_added_tasks(added_tasks):
    '''Saves static added task list to file'''
    try:
        with open("added_tasks.pkl", "wb") as pickle_out:
            pickle.dump(added_tasks, pickle_out)
    except:
        print("Failed to save!")


def get_active_tasks():
    '''Opens file with modified added task list'''
    try:
        with open("active_tasks.pkl", "rb") as pickle_in:
            active_tasks = pickle.load(pickle_in)
    except:
        active_tasks = []
    return active_tasks


def save_active_tasks(active_tasks):
    '''Saves modified added task list to file'''
    try:
        with open("active_tasks.pkl", "wb") as pickle_out:
            pickle.dump(active_tasks, pickle_out)
    except:
        print("Failed to save!")


def get_completed_tasks():
    '''Opens file with completed task list'''
    try:
        with open("completed_tasks.pkl", "rb") as pickle_in:
            completed_tasks = pickle.load(pickle_in)
    except:
        completed_tasks = []
    return completed_tasks


def save_completed_tasks(completed_tasks):
    '''Saves completed task list to file'''
    try:
        with open("completed_tasks.pkl", "wb") as pickle_out:
            pickle.dump(completed_tasks, pickle_out)
    except:
        print("Failed to save!")


def get_user_info():
    '''Opens user information file'''
    try:
        with open("user_info.pkl", "rb") as pickle_in:
            user_information = pickle.load(pickle_in)
    except:
        user_information = []
    return user_information


def save_user_info(user_information):
    '''Saves user information to file'''
    try:
        with open("user_info.pkl", "wb") as pickle_out:
            pickle.dump(user_information, pickle_out)
    except:
        print("Failed to save!")


def add_task():
    '''Adds a new task to static added task list and saves it to file.'''
    task_name = add_task_e.get()
    task_date = cal.get_date()
    task_time = add_time_e.get()
    unique_num  = create_unique_number()
    task_entry = task_name, task_date, task_time, unique_num
    added_tasks = get_added_tasks()
    added_tasks.append(list(task_entry))
    save_added_tasks(added_tasks)


def create_unique_number():
    '''Creates unique random number which is later added to an added task to make it unique'''
    number = datetime.now().microsecond
    seed(number)
    unique_number = 0
    unique_number = randint(1, 100)
    return unique_number


def task_modifier():
    '''Takes information from static added task file\
    and modifies it to create new task with countdown entry.\
    Overwrites these tasks with new countdown entries when task box is refreshed.\
    Also initiates send_email function if the time is up'''
    try:
        tasks = get_added_tasks()
        name = [n[0] for n in tasks]
        date = [d[1] for d in tasks]
        time = [t[2] for t in tasks]
        time_format = '%H:%M:%S'
        active_tasks = get_active_tasks()
        active_tasks = []
        task_num = 1
        for (n, d, t) in zip(name, date, time):
            try:
                datetime.strptime(t, time_format)
                t=t
            except ValueError:
                t = '08:00:00'
            format = '%Y-%m-%d %H:%M:%S'
            now = datetime.now().strftime(format)
            due = f'{d} {t}'
            time_left = datetime.strptime(due, format) - datetime.strptime(now, format)
            task = f'{task_num}  |  {n}   ►   Complete task in: {time_left}'
            if '-' in str(time_left):
                time_left = datetime.strptime(now, format) - datetime.strptime(due, format)
                task = f"{task_num}  |  {n}   ►   Task is overdue for: {time_left}"
            elif datetime.strptime(due, format) == datetime.strptime(now, format):
                user_information = get_user_info()
                user_name = user_information[0]
                if user_name == '':
                    user_name = 'Name not entered'
                user_email = user_information[1]
                if user_email == '':
                    user_email = '2doappteam@gmail.com'
                email=''
                send_email(user_name, email, user_email, n)
                print('email sent')
            task_num += 1
            active_tasks.append(task)
        save_active_tasks(active_tasks)
    except:
        if active_tasks == []:
            pass
   

def update_task_box():
    '''Updates task box every second to make countdown look dynamic'''
    task_modifier()
    task_box.delete(0, END)
    task_box.insert(END, *get_active_tasks())
    task_box.after(1000, update_task_box)
  

def delete_task():
    '''Deletes task entry from static added task file'''
    added_tasks = get_added_tasks()
    selection = task_to_delete_e.get()
    if selection == 'ENTER TASK NUMBER':
        pass
    elif selection == '':
        pass
    else:
        try:
            selection = abs(int(selection)) -1
        except ValueError:
            task_to_delete_e.insert(0, 'INVALID NUMBER:  ')
            pass
    for i in added_tasks:
        if added_tasks.index(i) == selection:
            if selection == -1:
                pass
            added_tasks.remove(i)
        else:
            pass
    save_added_tasks(added_tasks)


def complete_task():
    '''Moves task entry from static added task file to completed task file'''
    added_tasks = get_added_tasks()
    completed_tasks = get_completed_tasks()
    selection = task_to_complete_e.get()
    if selection == 'ENTER TASK NUMBER':
        pass
    elif selection == '':
        pass
    else:
        try:
            selection = abs(int(selection)) -1
        except ValueError:
            task_to_complete_e.insert(0, 'INVALID NUMBER:  ')
            pass
    for i in added_tasks:
        index = added_tasks.index(i)
        if added_tasks.index(i) == selection:
            if selection == -1:
                pass
            completed_tasks.append(f'    "{added_tasks[index][0]}" was due to ► {added_tasks[index][1]} | Completed on ► {datetime.date(datetime.now())}')
            save_completed_tasks(completed_tasks)
            added_tasks.remove(i)
        else:
            pass
    save_added_tasks(added_tasks)


def pop_up_info():
    '''Pops up a new window with user information'''
    u_info = Toplevel(window)
    u_info.iconbitmap(icon)
    u_info.title('User info')
    u_info.geometry('250x200')
    u_info.config(bg=secondary_dark_color)
    u_info.resizable(False, False)

    user_name_l = Label(u_info,
    bg=secondary_dark_color,
    fg=main_color,
    text='ENTER YOUR NAME:')
    user_name_l.pack(pady=5)

    user_name_e = Entry(u_info, width=30)
    user_name_e.pack()

    user_email_l = Label(u_info,
    bg=secondary_dark_color,
    fg=main_color,
    text='ENTER YOUR EMAIL:')
    user_email_l.pack(pady=10)

    user_email_e = Entry(u_info, width=30)
    user_email_e.pack()

    submit_b = Button(u_info,
    bg=secondary_color,
    width=25,
    fg=main_color,
    text='SUBMIT', command=lambda: submit_info(True))
    submit_b.pack(pady=30)
    
    user_information = get_user_info()
    if user_information != []:
        user_name_e.insert(0, '')
        user_email_e.insert(0,'')
        user_name_e.insert(0, user_information[0])
        user_email_e.insert(0, user_information[1])
    else:
        user_information = []
    
    def submit_info(is_true):
        if is_true == True:    
            user_information = []
            user_information.append(user_name_e.get())
            user_information.append(user_email_e.get())
            save_user_info(user_information)


def send_email(name, email, user_email, task):
    '''Sends email to users'''
    email = EmailMessage()
    email['from'] = '2DO APP'
    email['to'] = user_email
    email['subject'] = 'Time for your task has ended!'

    email.set_content(
        f'Hello, {name},\n\n\
        Time for "{task}" task has ended.\n\n\
        Have a nice day\n\n\
        2DO APP')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('2doappteam@gmail.com', password)
        smtp.send_message(email)


def pop_up_completed():
    '''Pops up a new window with completed tasks list'''
    global popup_completed
    popup_completed = Toplevel(window)
    popup_completed.iconbitmap(icon)
    popup_completed.title('Completed tasks')
    popup_completed.geometry('950x700')
    popup_completed.config(bg=secondary_dark_color)
    popup_completed.resizable(False, False)
    
    tasks_field = Listbox(popup_completed, bd=0, height=32, font=mid_font)
    tasks_field.pack(fill=BOTH)
    tasks_field.delete(0, END)
    tasks_field.insert(END, *get_completed_tasks())
    tasks_field.bindtags((task_box, mid, "selection"))
    tasks_field.config(bg=secondary_color, fg=main_color)
    
    clear_all = Button(popup_completed, text='CLEAR COMPLETED TASKS', bg=secondary_color, width= 100, height=5, command=lambda: clear_completed_tasks(True))
    clear_all.pack(pady=5)


def clear_completed_tasks(is_true):
    '''Clears completed task list from file'''
    if is_true == True:
        completed_tasks = get_completed_tasks()
        completed_tasks = []
        save_completed_tasks(completed_tasks)
    popup_completed.destroy()
    pop_up_completed()
    

def pop_up_readme():
    '''Pops up a new window with text about app'''
    readme = Toplevel(window)
    readme.iconbitmap(icon)
    readme.title('About 2DO')
    readme.geometry('950x700')
    readme.config(bg=secondary_dark_color)
    readme.resizable(False, False)

    about_app = Label(readme,
    bg=secondary_dark_color,
    fg=main_color, 
    font=big_font,
    text=welcome)
    about_app.pack(pady=40, fill=BOTH)


def focusin_entry_to_delete(event):
    '''Removes grey text from DELETE TASK entry when it is clicked'''
    if task_to_delete_e.get() == 'ENTER TASK NUMBER':
       task_to_delete_e.delete(0, "end")
       task_to_delete_e.insert(0, '')
       task_to_delete_e.config(fg = 'black')


def focusout_entry_to_delete(event):
    '''Refills DELETE TASK entry with default grey text'''
    if task_to_delete_e.get() == '':
        task_to_delete_e.insert(0, 'ENTER TASK NUMBER')
        task_to_delete_e.config(fg = 'grey')


def focusin_entry_to_complete(event):
    '''Removes grey text from COMPLETE TASK entry when it is clicked'''
    if task_to_complete_e.get() == 'ENTER TASK NUMBER':
       task_to_complete_e.delete(0, "end")
       task_to_complete_e.insert(0, '')
       task_to_complete_e.config(fg = 'black')


def focusout_entry_to_complete(event):
    '''Refills COMPLETE TASK entry with default grey text'''
    if task_to_complete_e.get() == '':
        task_to_complete_e.insert(0, 'ENTER TASK NUMBER')
        task_to_complete_e.config(fg = 'grey')


# -----MENU--------------------------------------------------------------
app_menu = Menu(window)
app_menu.config()
window.config(menu=app_menu)
menu = Menu(app_menu, tearoff=0)
menu.config(bg=secondary_color, fg=main_color)
app_menu.add_cascade(label='Menu', menu=menu)
menu.add_command(label='User info', command=pop_up_info)
menu.add_command(label='Show completed tasks', command=pop_up_completed)
menu.add_separator()
menu.add_command(label='About 2DO', command=pop_up_readme)


# -----CALENDAR----------------------------------------------------------
cal = Calendar(top, selectmode='day', 
                year = datetime.now().year, 
                month=datetime.now().month, 
                day=datetime.now().day, 
                date_pattern="yyyy-mm-dd",
                background=main_color,
                headersbackground=light_main_color,
                headersforeground='white',
                selectbackground=main_color,
                normalbackground=secondary_color,
                weekendbackground = secondary_dark_color,
                othermonthbackground = secondary_color,
                othermonthwebackground = secondary_dark_color)

cal.pack(fill=BOTH, expand=True)


# -----LABELS AND ENTRIES-------------------------------------------------
add_task_l = Label(top, bg=main_color, fg='white', text='ENTER TASK NAME', width=20)
add_task_l.pack(side=LEFT, pady=10, expand=True)

add_task_e = Entry(top, width=50)
add_task_e.insert(END, 'New Task')
add_task_e.config(fg=main_color)
add_task_e.pack(side=LEFT, pady=10, padx=5, expand=True)

add_time_l = Label(top, bg=main_color, fg='white', 
text='ENTER DUE TIME (HH:MM:SS)', 
width=30)
add_time_l.pack(side=LEFT, pady=10, expand=True)

add_time_e = Entry(top)
add_time_e.insert(END, '08:00:00')
add_time_e.config(fg=main_color)
add_time_e.pack(side=LEFT, pady=10, padx=5, expand=True)

task_to_delete_l = Label(bottom, bg=main_color, fg='white', text='WHICH TASK YOU WANT TO DELETE?')
task_to_delete_l.grid(row=0, column=0, sticky='nsew')

task_to_delete_e = Entry(bottom)
task_to_delete_e.grid(row=0, column=1, sticky='nsew')
task_to_delete_e.insert(0, 'ENTER TASK NUMBER')
task_to_delete_e.bind('<FocusIn>', focusin_entry_to_delete)
task_to_delete_e.bind('<FocusOut>', focusout_entry_to_delete)
task_to_delete_e.config(fg = 'grey')

task_to_complete_l = Label(bottom, bg=main_color, fg='white', text='WHICH TASK YOU WANT TO COMPLETE?')
task_to_complete_l.grid(row=1, column=0, sticky='nsew')

task_to_complete_e = Entry(bottom)
task_to_complete_e.grid(row=1, column=1, sticky='nsew')
task_to_complete_e.insert(0, 'ENTER TASK NUMBER')
task_to_complete_e.bind('<FocusIn>', focusin_entry_to_complete)
task_to_complete_e.bind('<FocusOut>', focusout_entry_to_complete)
task_to_complete_e.config(fg = 'grey')


#-----BUTTONS-----------------------------------------------------
confirm_btn = Button(bottom, text='ADD TASK', 
bg=secondary_color, 
fg=main_color, 
width=130, height=2, 
command=add_task)
confirm_btn.grid(row=2, columnspan=2, sticky='nsew')

delete_btn = Button(bottom, text='DELETE TASK', 
bg=secondary_color, 
fg=main_color, 
height=2, 
command=delete_task)
delete_btn.grid(row=3, columnspan=2, sticky='nsew')

complete_btn = Button(bottom, text='COMPLETE TASK', 
bg=secondary_color, 
fg=main_color, 
height=2, 
command=complete_task)
complete_btn.grid(row=4, columnspan=2, sticky='nsew')


# -----TASKBOX------------------------------------------------------
style.configure("Horizontal.TScrollbar", 
                gripcount=0,
                background=light_main_color, 
                darkcolor=light_main_color, 
                lightcolor=secondary_dark_color,
                troughcolor=secondary_dark_color, 
                bordercolor=secondary_dark_color, 
                arrowcolor=secondary_color)

style.configure("Vertical.TScrollbar",
                gripcount=0,
                background=light_main_color, 
                darkcolor=light_main_color, 
                lightcolor=secondary_dark_color,
                troughcolor=secondary_dark_color, 
                bordercolor=secondary_dark_color, 
                arrowcolor=secondary_color)

y_scrlbar = ttk.Scrollbar(mid)
x_scrlbar = ttk.Scrollbar(mid, orient='horizontal')

task_box = Listbox(mid, 
yscrollcommand=y_scrlbar.set,
xscrollcommand=x_scrlbar.set, 
bd=0, width=65, height = 10,
font=big_font)

y_scrlbar.config(command=task_box.yview)
y_scrlbar.pack(side=RIGHT, fill=BOTH,)
x_scrlbar.config(command=task_box.xview)
x_scrlbar.pack(side=BOTTOM, fill=BOTH,)
task_box.bindtags((task_box, mid, "selection"))
task_box.config(background=secondary_color)
task_box.config(foreground=main_color)
task_box.pack(side=LEFT)

update_task_box()
window.mainloop()
