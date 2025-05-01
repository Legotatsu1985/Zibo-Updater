import zipfile
import glob
import os
import shutil
import re
import tkinter
import tkinter.messagebox
from tkinter import filedialog

def get_saved_xplane_path(): #Get the saved X-Plane path from the file
    xplane_path_entry.delete(0, tkinter.END)
    xplnae_path_save_file = r'x-plane_path.txt'
    if os.path.isfile(xplnae_path_save_file):
        with open(xplnae_path_save_file, mode='r') as file:
            lines = file.read()
        if re.search(r"X-Plane 12", lines):
            xplane_path = lines[7:]
            print('X-Plane 12 Path = ' + xplane_path)
            xplane_path_entry.insert(tkinter.END, xplane_path)
            save_xplane_path_checkbox.set(True)
            return xplane_path
        else:
            return
    else:
        return

def get_zibo_737_path():
    if not xplane_path_entry.get() == '': ##The entry is not empty
        xplane_path = xplane_path_entry.get()
        zibo737_path = xplane_path + r"\Aircraft\B737-800X"
        if os.path.isfile(zibo737_path + r"\b738_4k.acf"):
            print('Zibo737 Found.')
            return zibo737_path
        else:
            print('Could not find Zibo737.')
            return None
    else:
        print('Could not find X-Plane 12.')
        return None

def check_zibo_737_version():
    zibo737_path = get_zibo_737_path()
    if not zibo737_path == None:
        zibo737_version_file = zibo737_path + r"\version.txt"
        with open(zibo737_version_file, mode='r') as file:
            zibo737_version_int = file.read()
            print("Zibo737 Version = " + zibo737_version_int)
            zibo_737_version_number.config(text=zibo737_version_int)
    else:
        return

def save_xplane_path(): #Save the X-Plane path to a file
    if save_xplane_path_checkbox.get() == True: #The checkbox is checked
        if not xplane_path_entry.get() == '': #The entry is not empty
            xplane_path = xplane_path_entry.get() 
            
            print("X-Plane Path = " + xplane_path)
            xplane_path_save_file = r'x-plane_path.txt'
            
            with open(xplane_path_save_file, mode='w') as file:
                file.write('Path = ' + xplane_path)
        else:
            return
    elif save_xplane_path_checkbox.get() == False: #The checkbox is unchecked
        if os.path.isfile(r'x-plane_path.txt'): #The file exists
            os.remove(r'x-plane_path.txt') #then delete the file
        return

def select_xplane_path(): #Select the X-Plane path
    xplane_path_entry.delete(0, tkinter.END)
    xplane_path = filedialog.askdirectory(initialdir=os.path.abspath('.'), title="Select the X-Plane root path.")
    if not xplane_path == "":
        xplane_path_entry.insert(tkinter.END, xplane_path)
        if os.path.isfile(xplane_path + r"\X-Plane.exe"):
            print('X-Plane 12 path = ' + xplane_path)
            xplane_path_verify_text.config(text="Valid", fg="green")
            check_zibo_737_version()
            return
        else:
            print('Invalid X-Plane 12 Path.')
            xplane_path_verify_text.config(text="Invalid", fg="red")
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('Error','"X-Plane.exe" not found. Please select the path again.')
            return
    else:
        xplane_path_entry.delete(0, tkinter.END)
        return

def update_file_verify(update_file_path):
    update_file_basename = os.path.basename(update_file_path)
    update_file = re.match(r'B738X_XP12_4_[0-9]{2}_[0-9]{2}.zip', update_file_basename)
    if bool(update_file): #The file name is valid
        return True
    else: #The file name is invalid
        return False


def select_update_file(): #Select the update file
    update_file_path_entry.delete(0, tkinter.END)
    update_file_path = filedialog.askopenfilename(filetypes=[('ZIP file','*.zip')], initialdir=os.path.abspath('.'), title="Select the update file for Zibo 737.")
    if not update_file_path == "":
        update_file_path_entry.insert(tkinter.END, update_file_path)
        if update_file_verify(update_file_path) == True:
            update_file_verify_text.config(text="Valid", fg="green")
        else:
            update_file_verify_text.config(text="Invalid", fg="red")
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('Error','This file is invalid.')
    else:
        update_file_path_entry.delete(0, tkinter.END)
        return

def update_zibo_737():
    zibo_737_path = get_zibo_737_path()
    if not zibo_737_path == None:
        print('(Test log: Zibo737 path found)')
        if not update_file_path_entry.get() == None:
            update_file_path = update_file_path_entry.get()
            if update_file_verify(update_file_path) == True:
                print()
            else:
                tkinter.Tk().withdraw()
                tkinter.messagebox.showerror('Error', 'Invalid update file.')
                return
    else:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showerror('Error', 'X-Plane 12 path or Zibo737 not found. Please re-select the path.')
        print('Path error ocurred.')
        return

root = tkinter.Tk()
root.title("Zibo737 Easy Updater")
root.geometry("450x200")
software_version = "v0.0.1"
xplane_path_label = tkinter.Label(root, justify="right", text="X-Plane 12 installed path ->")
xplane_path_entry = tkinter.Entry(root, width=35)
xplane_path_select_button = tkinter.Button(root, text="...", command=select_xplane_path)
xplane_path_verify_text = tkinter.Label(root, justify="center")
save_xplane_path_checkbox = tkinter.BooleanVar()
save_xplane_path_checkbutton = tkinter.Checkbutton(root, variable=save_xplane_path_checkbox, command=save_xplane_path)
save_xplane_path_checkbutton_label = tkinter.Label(root, justify="left", text="Save the path for future updates.")
update_file_path_label = tkinter.Label(root, justify="right", text="Update file path ->")
update_file_path_entry = tkinter.Entry(root, width=35)
zibo_737_version_label = tkinter.Label(root, justify="right", text="Current Zibo Version Installed =")
zibo_737_version_number = tkinter.Label(root, justify="left")
update_file_path_select_button = tkinter.Button(root, text="...", command=select_update_file)
update_file_verify_text = tkinter.Label(root, justify="center")
start_update_button = tkinter.Button(root, text="UPDATE", command=update_zibo_737)
exit_button = tkinter.Button(root, text="EXIT", command=root.quit)
get_saved_xplane_path()
check_zibo_737_version()

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
zibo_737_version_label.grid(
    column=0,
    row=3,
    sticky=tkinter.E
)
zibo_737_version_number.grid(
    column=1,
    row=3,
    sticky=tkinter.W
)
start_update_button.grid(
    column=1,
    row=4
)
exit_button.grid(
    column=1,
    row=5
)
root.mainloop()