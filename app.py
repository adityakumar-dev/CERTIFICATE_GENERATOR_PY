import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pandas as pd
from mailapi import sendMail
path_template = ''
path_excel = ''
text_position = (0, 0)  

def generate_certificate(name, template_path, position):
    template = Image.open(template_path)
    
    draw = ImageDraw.Draw(template)

    font = ImageFont.truetype("arial.ttf", 50)

    draw.text(position, name, font=font, fill="black")
    
    output_path = f'/home/linmar/Desktop/project/certificate_generator_py/{name}_certificate.png'
    template.save(output_path)
    print(f"Certificate saved to {output_path} at position {position}")
    return output_path
def execel_sheet_btn_command():
    global path_excel
    file = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx"), ("All files", "*")])
    if file:
        path_excel = file
        execel_sheet.config(text=f"Selected file: {file}", fg="#fff")

def select_template():
    global path_template
    file = filedialog.askopenfilename(filetypes=[("Image File", ".png"), ("All files", "*")])
    if file:
        path_template = file
        templateLabel.config(text=f"Selected template: {file}", fg="#fff")

def select_position():
    global text_position
    if not path_template:
        print("Please select a template first.")
        return

    img = Image.open(path_template)
    original_width, original_height = img.size 
    display_width = 600
    display_height = int((original_height / original_width) * display_width)

    position_window = tk.Toplevel(root)
    position_window.title("Select Text Position")
    position_window.geometry(f"{display_width}x{display_height}")

    resized_img = img.resize((display_width, display_height), Image.LANCZOS)
    
    img_tk = ImageTk.PhotoImage(resized_img)

    canvas = tk.Canvas(position_window, width=display_width, height=display_height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    
    def on_click(event):
        global text_position
        
        scale_x = original_width / display_width
        scale_y = original_height / display_height

        text_position = (int(event.x * scale_x), int(event.y * scale_y))
        
        print(f"Selected position: {text_position} (original image coordinates)")
        position_window.destroy()  

    canvas.bind("<Button-1>", on_click)
    
    canvas.image = img_tk
    
    position_window.mainloop()

def generate_certificates():
    if not path_excel or not path_template:
        print("Please select both an Excel file and a template image.")
        return

    df = pd.read_excel(path_excel)
    
    if text_position:
        for index, row in df.iterrows():
            name = row['name'] 
            email = row['email']
            print(f"Generating certificate for: {name} at position {text_position}")
            path = generate_certificate(name, path_template, text_position)
            print(f"sending certificate to {email}")
            sendMail(file_path=path,to=email,name=name)
    else:
        print('Text position not found.')

root = tk.Tk()
root.title("Certificate Generator")
root.geometry("500x400")
root.config(bg="#000")

root.grid_columnconfigure(0, weight=1) 
root.grid_rowconfigure(0, weight=1)    
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

label = tk.Label(root, text="Certificate Generator", fg="#fff", bg="#000")
label.grid(row=0, column=0, sticky='n')

execel_sheet = tk.Label(root, text="Select your Excel file", padx=10, pady=10, bg="#000", fg="#fff")
execel_sheet.grid(row=1, column=0, sticky='n')

execel_sheet_btn = tk.Button(root, text="Select File", command=execel_sheet_btn_command)
execel_sheet_btn.grid(row=2, column=0)

templateLabel = tk.Label(root, text="Select Template", padx=10, pady=10, bg="#000", fg="#fff")
templateLabel.grid(row=3, column=0)

templateSelectBtn = tk.Button(root, text="Open Template", command=select_template)
templateSelectBtn.grid(row=4, column=0)

positionSelectBtn = tk.Button(root, text="Select Text Position", command=select_position)
positionSelectBtn.grid(row=5, column=0)

generate_template = tk.Button(root, text="Generate Certificates", command=generate_certificates)
generate_template.grid(row=6, column=0)

root.mainloop()
