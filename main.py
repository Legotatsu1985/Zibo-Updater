import zipfile
import glob
import os
import shutil
import re
import tkinter
import tkinter.messagebox
from tkinter import filedialog

def save_xplane_path():
    if save_xplane_path_checkbox.get():
        if not xplane_path_entry.get() == '':
            xplane_path = xplane_path_entry.get()
            
            if not xplane_path.rfind('X-Plane 11') == -1:
                xplane_version = 11
            elif not xplane_path.rfind('X-Plane 12') == -1:
                xplane_version = 12
            else:
                return
            
            print("X-Plane path = " + xplane_path)
            xplane_path_save_file = 'x-plane_path.txt'
            
            print("X-Plane version = " + str(xplane_version))
            
            #with open(xplane_path_save_file, mode='w') as file:
            #    file.write(xplane_path)
        else:
            return

def select_xplane_path():
    xplane_path_entry.delete(0, tkinter.END)
    xplane_path = filedialog.askdirectory(initialdir=os.path.abspath('.'), title="Select the X-Plane root path.")
    if not xplane_path == "":
        xplane_path_entry.insert(tkinter.END, xplane_path)
        if os.path.isfile(xplane_path + r"\X-Plane.exe"):
            xplane_path_verify_text.config(text="Valid", fg="green")
        else:
            xplane_path_verify_text.config(text="Invalid", fg="red")
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('Error','"X-Plane.exe" not found. Please select the path again.')
    else:
        xplane_path_entry.delete(0, tkinter.END)
        return

def select_update_file():
    update_file_path_entry.delete(0, tkinter.END)
    update_file_path = filedialog.askopenfilename(filetypes=[('ZIP file','*.zip')], initialdir=os.path.abspath('.'), title="Select the update file for Zibo 737.")
    if not update_file_path == "":
        update_file_path_entry.insert(tkinter.END, update_file_path)
        update_file_basename = os.path.basename(update_file_path)
        update_file = re.match(r'B738X_XP(11|12)_4_[0-9]*_[0-9]*.zip', update_file_basename)
        if bool(update_file):
            update_file_verify_text.config(text="Valid", fg="green")
        else:
            update_file_verify_text.config(text="Invalid", fg="red")
            tkinter.messagebox.showerror('Error','This file is invalid.')
    else:
        update_file_path_entry.delete(0, tkinter.END)
        return

root = tkinter.Tk()
root.title("Zibo737 Easy Updater")
root.geometry("450x200")
software_version = "v0.0.1"
xplane_path_label = tkinter.Label(root, justify="right", text="X-Plane 11/12 installed path ->")
xplane_path_entry = tkinter.Entry(root, width=35)
xplane_path_select_button = tkinter.Button(root, text="...", command=select_xplane_path)
xplane_path_verify_text = tkinter.Label(root, justify="center")
save_xplane_path_checkbox = tkinter.BooleanVar()
save_xplane_path_checkbutton = tkinter.Checkbutton(root, variable=save_xplane_path_checkbox, command=save_xplane_path)
save_xplane_path_checkbutton_label = tkinter.Label(root, justify="left", text="Save the path for future updates.")
update_file_path_label = tkinter.Label(root, justify="right", text="Update file path ->")
update_file_path_entry = tkinter.Entry(root, width=35)
update_file_path_select_button = tkinter.Button(root, text="...", command=select_update_file)
update_file_verify_text = tkinter.Label(root, justify="center")
start_update_button = tkinter.Button(root, text="UPDATE")

xplane_path_label.grid(
    column=0,
    row=0,
    sticky=tkinter.E
)
xplane_path_entry.grid(
    column=1,
    row=0,
    sticky=tkinter.W
)
xplane_path_select_button.grid(
    column=2,
    row=0
)
xplane_path_verify_text.grid(
    column=3,
    row=0
)
save_xplane_path_checkbutton_label.grid(
    column=0,
    row=1,
    sticky=tkinter.E
)
save_xplane_path_checkbutton.grid(
    column=1,
    row=1,
    sticky=tkinter.W
)
update_file_path_label.grid(
    column=0,
    row=2,
    sticky=tkinter.E
)
update_file_path_entry.grid(
    column=1,
    row=2,
    sticky=tkinter.W
)
update_file_path_select_button.grid(
    column=2,
    row=2
)
update_file_verify_text.grid(
    column=3,
    row=2
)
start_update_button.grid(
    column=1,
    row=3
)
root.mainloop()