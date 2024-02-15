import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter import filedialog

import Road_Test_Radar
from Road_Test_Radar import *

today = str(datetime.date.today())[8:]
next_month = False
if int(today) > 25:
    next_month = True

loc = ["Brampton", "Guelph", "Mississauga", "Orangeville", "Hamilton", "Brantford", "Kitchener"]
loc_id = {'Brampton': 'targetLoc2', 'Guelph': 'targetLoc7', 'Mississauga': 'targetLoc12', 'Orangeville': 'targetLoc15',
          'Hamilton': 'targetLoc8', 'Brantford': 'targetLoc3', 'Kitchener': 'targetLoc9'}
ignored = [[]]


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


def add_student():
    name = simpledialog.askstring("Add Student", "Enter student's name:")
    license_number = simpledialog.askstring("Add Student", "Enter student's license number:")
    expiry_date = simpledialog.askstring("Add Student", "Enter student's expiry date:")
    class_name = simpledialog.askstring("Add Student", "Enter student's class:")

    if name and license_number and expiry_date and class_name:
        student_info = f"{name}, {license_number}, {expiry_date}, {class_name}\n"
        with open("data/All Students.txt", "a") as file:
            file.write(student_info)
        messagebox.showinfo("Success", "Student has been added!")
        window.destroy()


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
    login()


# Check Dates button
def call_check_function():
    date_available(ignored)


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

check_button = ttk.Button(button_frame, text="Check Dates", command=call_check_function)
check_button.grid(row=4, column=0, pady=10)

# Configure grid weights to center the frame
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
button_frame.columnconfigure(0, weight=1)

root.mainloop()
