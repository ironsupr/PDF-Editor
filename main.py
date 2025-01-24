from customtkinter import *
from pdf_manager import *

root = CTk()
root.title("PDF Manager")
root.geometry("1000x800")
root.resizable(True, True)
root.iconbitmap("pdf.ico")
set_default_color_theme("green")

#PDF Merger
def pdf_merger(path, output="merged.pdf"):
    pdf_to_png(path)
    images_to_pdf()
    

# Create a label
label = CTkLabel(root, text="PDF Manager", font=("Arial", 20))
label.place(relx=0.5, rely=0.1, anchor="center")

# Create a button
button = CTkButton(root, text="PDF to PNG", command=lambda: pdf_to_png("pdf"), width=900, height=90, corner_radius=10, hover_color="#0B6623", font=("Arial", 15)) 
button.place(relx=0.5, rely=0.3, anchor="center")

# Create a button
button = CTkButton(root, text="Images to PDF", command=lambda: images_to_pdf("Images"), width=900, height=90, corner_radius=10, hover_color="#0B6623", font=("Arial", 15))
button.place(relx=0.5, rely=0.45, anchor="center")

# Create a button
button = CTkButton(root, text="Merge PDFs", command=lambda: pdf_merger("pdf"), width=900, height=90, corner_radius=10, hover_color="#0B6623", font=("Arial", 15))
button.place(relx=0.5, rely=0.6, anchor="center")

root.mainloop()