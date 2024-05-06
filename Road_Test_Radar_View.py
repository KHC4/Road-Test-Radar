import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import Calendar
import threading

import Road_Test_Radar
from Road_Test_Radar import *

check_next_month = False

loc = ["Brampton", "Guelph", "Mississauga", "Orangeville", "Hamilton", "Brantford", "Kitchener"]
loc_id = {'Brampton': 'targetLoc2', 'Guelph': 'targetLoc7', 'Mississauga': 'targetLoc12', 'Orangeville': 'targetLoc15',
          'Hamilton': 'targetLoc8', 'Brantford': 'targetLoc3', 'Kitchener': 'targetLoc9'}

month1 = int(str(datetime.date.today())[5:7])
month2 = int(str(datetime.date.today())[5:7]) + 1
selected_dates_month1 = {}
selected_dates_month2 = {}

# setup date dictionaries, make key for each date in the month and value is a tuple of true/false and ignored times and loc
# example {14: (True, [(location, [time1, time2]), (location, [time1, time2])]}
for i in range(calendar.monthrange(2024, month1)[1] + 1):
    selected_dates_month1[i] = (False, {})

for j in range(calendar.monthrange(2024, month2)[1] + 1):
    selected_dates_month2[j] = (False, {})


# first button set email
def set_email():
    email = simpledialog.askstring("Set Email", "Enter your email:")
    if email:
        with open("data/email.txt", "w") as file:
            file.write(email)
            messagebox.showinfo("Success", "Email has been set!")


# Second Button Select Student
def select_student():
    students = read_students_from_file()

    if not students:
        messagebox.showwarning("No Students Found", "No students found in the record.")
        add_student_button = tk.Button(window, text="Add Student", command=add_student)
        add_student_button.pack()
        return

    selected_student = tk.StringVar()
    student_menu = ttk.OptionMenu(window, selected_student, "", *students)
    student_menu.pack()

    def save_selected_student():
        student_info = selected_student.get()
        if student_info:
            with open("data/Current Student.txt", "w") as file:
                file.write(student_info)
                messagebox.showinfo("Success", "Selected student has been saved!")
                window.destroy()

    save_button = tk.Button(window, text="Save", command=save_selected_student)
    save_button.pack()


# def add_student():
#     name = simpledialog.askstring("Add Student", "Enter student's name:")
#     license_number = simpledialog.askstring("Add Student", "Enter student's license number:")
#     expiry_date = simpledialog.askstring("Add Student", "Enter student's expiry date:")
#     class_name = simpledialog.askstring("Add Student", "Enter student's class:")
#
#     if name and license_number and expiry_date and class_name:
#         student_info = f"{name}, {license_number}, {expiry_date}, {class_name}\n"
#         with open("data/All Students.txt", "a") as file:
#             file.write(student_info)
#         messagebox.showinfo("Success", "Student has been added!")
#         window.destroy()

def add_student():
    dialog = tk.Toplevel()
    dialog.title("Add Student")

    tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(dialog, text="License #:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Label(dialog, text="Expiry:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Label(dialog, text="Class:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

    name_entry = tk.Entry(dialog)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    license_frame = tk.Frame(dialog)
    license_frame.grid(row=1, column=1, padx=5, pady=5)
    license_entry1 = tk.Entry(license_frame, width=5, validate="key")
    license_entry1.pack(side=tk.LEFT)
    license_entry1.config(validatecommand=(license_entry1.register(lambda s: len(s) <= 5), '%P'))
    tk.Label(license_frame, text="-").pack(side=tk.LEFT)
    license_entry2 = tk.Entry(license_frame, width=5, validate="key")
    license_entry2.pack(side=tk.LEFT)
    license_entry2.config(validatecommand=(license_entry1.register(lambda s: len(s) <= 5), '%P'))
    tk.Label(license_frame, text="-").pack(side=tk.LEFT)
    license_entry3 = tk.Entry(license_frame, width=5, validate="key")
    license_entry3.pack(side=tk.LEFT)
    license_entry3.config(validatecommand=(license_entry1.register(lambda s: len(s) <= 5), '%P'))

    expiry_frame = tk.Frame(dialog)
    expiry_frame.grid(row=2, column=1, padx=5, pady=5)
    expiry_entry1 = tk.Entry(expiry_frame, width=5, validate="key")
    expiry_entry1.pack(side=tk.LEFT)
    expiry_entry1.config(validatecommand=(expiry_entry1.register(lambda s: len(s) <= 4), '%P'))
    tk.Label(expiry_frame, text="/").pack(side=tk.LEFT)
    expiry_entry2 = tk.Entry(expiry_frame, width=5, validate="key")
    expiry_entry2.pack(side=tk.LEFT)
    tk.Label(expiry_frame, text="/").pack(side=tk.LEFT)
    expiry_entry2.config(validatecommand=(expiry_entry2.register(lambda s: len(s) <= 2), '%P'))
    expiry_entry3 = tk.Entry(expiry_frame, width=5, validate="key")
    expiry_entry3.config(validatecommand=(expiry_entry3.register(lambda s: len(s) <= 2), '%P'))
    expiry_entry3.pack(side=tk.LEFT)

    class_var = tk.StringVar()
    class_frame = tk.Frame(dialog)
    class_frame.grid(row=3, column=1, padx=5, pady=5)
    tk.Radiobutton(class_frame, text="G", variable=class_var, value="G").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(class_frame, text="G2", variable=class_var, value="G2").pack(side=tk.LEFT, padx=5)

    def save_student():
        name = name_entry.get().strip()
        license_number = "-".join([license_entry1.get(), license_entry2.get(), license_entry3.get()]).strip()
        expiry_date = "/".join([expiry_entry1.get(), expiry_entry2.get(), expiry_entry3.get()]).strip()
        class_name = class_var.get()

        if name and license_number and expiry_date and class_name:
            student_info = f"{name}, {license_number}, {expiry_date}, {class_name}\n"
            with open("data/All Students.txt", "a") as file:
                file.write(student_info)
            messagebox.showinfo("Success", "Student has been added!")
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    save_button = tk.Button(dialog, text="Save", command=save_student)
    save_button.grid(row=4, columnspan=2, padx=5, pady=10)


def remove_student():
    students = read_students_from_file()

    if not students:
        messagebox.showwarning("No Students Found", "No students found in the record.")
        return

    selected_student = tk.StringVar()
    student_menu = ttk.OptionMenu(window, selected_student, "", *students)
    student_menu.pack()

    def remove_selected_student():
        student = selected_student.get()
        if student:
            students.remove(student)
            with open("data/All Students.txt", "w") as file:
                for student in students:
                    file.write(student + "\n")
            messagebox.showinfo("Success", "Selected student has been removed!")
            window.destroy()

    remove_button = tk.Button(window, text="Remove", command=remove_selected_student)
    remove_button.pack()


def read_students_from_file():
    students = []
    with open("data/All Students.txt", "r") as file:
        for line in file:
            students.append(line.strip())
    return students


# Select Test Centers
selected_test_centers = []  # Global variable to store selected test centers


def open_test_centers_window():
    test_centers = ["Brampton", "Guelph", "Mississauga", "Orangeville", "Hamilton", "Brantford", "Kitchener"]

    def save_test_centers():
        global selected_test_centers
        selected_test_centers = [test_centers[i] for i in range(len(test_centers)) if checkbox_vars[i].get() == 1]
        with open("data/selected_locations.txt", "w") as file:
            file.write("\n".join(selected_test_centers))
        window.destroy()  # Close the window after saving the selections

    window = tk.Toplevel(root)
    window.title("Select Test Centers")

    checkbox_vars = []
    checkboxes = []

    for center in test_centers:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(window, text=center, variable=var)
        checkbox.pack()
        checkbox_vars.append(var)
        checkboxes.append(checkbox)

    save_button = tk.Button(window, text="Save", command=save_test_centers)
    save_button.pack()


# Login button
def call_login_function():
    if threading.active_count() > 1:
        print("Currently Running")
    else:
        x = threading.Thread(target=login)
        x.start()


# Check Dates button
def call_check_function():
    if threading.active_count() > 1:
        print("Currently Running")
    else:
        y = threading.Thread(target=date_available, args=(selected_dates_month1, selected_dates_month2))
        y.start()


def call_restart_function():
    if threading.active_count() > 1:
        print("Currently Running")
    else:
        x = threading.Thread(target=restart)
        x.start()


def select_dates():
    def on_date_selected():
        selected_date = cal.selection_get()
        dt = Calendar.datetime.strptime(str(selected_date), "%Y-%m-%d").date()
        month = int(str(selected_date)[5:7])
        if month == month1:
            if selected_dates_month1[int(str(selected_date)[8:])][0]:
                selected_dates_month1[int(str(selected_date)[8:])] = (False, {})
                cal.calevent_create(date=dt, text='Deselected', tags="deselected")
                cal.tag_config("deselected", background='red')
            else:
                selected_dates_month1[int(str(selected_date)[8:])] = (True, {})
                cal.calevent_create(date=dt, text='Selected', tags="selected")
                cal.tag_config("selected", background='green')
        elif month == month2:
            global check_next_month
            check_next_month = True
            if selected_dates_month2[int(str(selected_date)[8:])][0]:
                selected_dates_month2[int(str(selected_date)[8:])] = (False, {})
                cal.calevent_create(date=dt, text='Deselected', tags="deselected")
                cal.tag_config("deselected", background='red')
            else:
                selected_dates_month2[int(str(selected_date)[8:])] = (True, {})
                cal.calevent_create(date=dt, text='Selected', tags="selected")
                cal.tag_config("selected", background='green')

    def done_selection():
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Select Dates")
    next_month = datetime.datetime.now() + datetime.timedelta(days=30)

    cal = Calendar(window, selectmode="day", date_pattern="yyyy-mm-dd",
                   mindate=datetime.datetime.now() + datetime.timedelta(days=1), maxdate=next_month)
    cal.pack(padx=10, pady=10)

    select_button = ttk.Button(window, text="Select", command=on_date_selected)
    select_button.pack(pady=5)

    done_button = ttk.Button(window, text="Done", command=done_selection)
    done_button.pack(pady=5)


# Main Interface
root = tk.Tk()
root.title("Road Test Date Checker")
style = ttk.Style()
style.theme_use('clam')
root.iconbitmap('assets/icon.ico')


def open_select_window():
    global window
    window = tk.Toplevel(root)
    window.title("Select Student")
    select_student()
    add_student_button = tk.Button(window, text="Add Student", command=add_student)
    add_student_button.pack(pady=10)
    remove_student_button = tk.Button(window, text="Remove Student", command=remove_student)
    remove_student_button.pack(pady=10)


# Create a frame to hold the buttons
button_frame = ttk.Frame(root, padding=20)
button_frame.grid(row=0, column=0, sticky='nsew')

# Create buttons with grid layout
set_email_button = ttk.Button(button_frame, text="Set Email", command=set_email)
set_email_button.grid(row=0, column=0, pady=10)

select_student_button = ttk.Button(button_frame, text="Select Student", command=open_select_window)
select_student_button.grid(row=1, column=0, pady=10)

select_test_centers_button = ttk.Button(button_frame, text="Select Test Centers", command=open_test_centers_window)
select_test_centers_button.grid(row=2, column=0, pady=10)

login_button = ttk.Button(button_frame, text="Login", command=call_login_function)
login_button.grid(row=3, column=0, pady=10)

check_button = ttk.Button(button_frame, text="Select Dates", command=select_dates)
check_button.grid(row=4, column=0, pady=10)

check_button = ttk.Button(button_frame, text="Check Dates", command=call_check_function)
check_button.grid(row=5, column=0, pady=10)

check_button = ttk.Button(button_frame, text="Restart", command=call_restart_function)
check_button.grid(row=6, column=0, pady=10)

# Configure grid weights to center the frame
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
button_frame.columnconfigure(0, weight=1)

root.mainloop()
