from customtkinter import *
from pdf_manager import *  # Ensure pdf_to_png and images_to_pdf are imported here
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox

root = CTk()
root.title("PDF Manager")
root.geometry("1000x800")
root.resizable(True, True)
root.iconbitmap("pdf.ico")
set_default_color_theme("green")

# Helper function to create buttons
def create_button(root, text, command, width=900, height=90, font=("Arial", 15), hover_color="#0B6623"):
    return CTkButton(
        root,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=10,
        hover_color=hover_color,
        font=font
    )

# Function to merge PDFs
def pdf_merger(paths, output="merged.pdf"):
    try:
        # Assuming pdf_to_png and images_to_pdf are defined elsewhere
        pdf_to_png(paths)  # Ensure this function is prepared to handle paths correctly
        images_to_pdf()
        messagebox.showinfo("Success", f"PDFs merged successfully into {output}")
    except Exception as e:
        messagebox.showerror("Error", f"Error during PDF merging: {e}")

# Function to prompt user for file path to open
def select_pdf_files():
    file_paths = askdirectory()
    if file_paths:
        pdf_merger(file_paths)

# Function to prompt user for folder to select images
def select_image_folder():
    folder_path = askdirectory()
    if folder_path:
        images_to_pdf(folder_path)
        messagebox.showinfo("Success", "Images successfully converted to PDF.")

# def pdf_merger(path):
#     pdf_to_png(path)
#     images_to_pdf()

# Create a label
label = CTkLabel(root, text="PDF Manager", font=("Arial", 20))
label.place(relx=0.5, rely=0.1, anchor="center")

# Create and place buttons using the helper function
button1 = create_button(root, text="PDF to PNG", command=lambda: pdf_to_png("pdf"))
button1.place(relx=0.5, rely=0.3, anchor="center")

button2 = create_button(root, text="Images to PDF", command=select_image_folder)
button2.place(relx=0.5, rely=0.45, anchor="center")

button3 = create_button(root, text="Merge PDFs", command=select_pdf_files)
button3.place(relx=0.5, rely=0.6, anchor="center")

root.mainloop()
