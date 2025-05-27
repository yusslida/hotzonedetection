# -*- coding: utf-8 -*-
"""
Thermal Simulation and Hot Zone Detection using Tkinter GUI
Author: Dr. Zuliani
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def simulate_thermal_and_display():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if not file_path:
        messagebox.showwarning("No file", "No image selected.")
        return

    image = cv2.imread(file_path)
    if image is None:
        messagebox.showerror("Error", "Unable to load image.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thermal colormap
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # Detect hot zones (threshold > 200)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    highlight = image.copy()
    highlight[mask == 255] = [0, 0, 255]  # Red overlay

    # Convert for Tkinter display
    image_disp = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 200))
    thermal_disp = Image.fromarray(cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)).resize((300, 200))
    highlight_disp = Image.fromarray(cv2.cvtColor(highlight, cv2.COLOR_BGR2RGB)).resize((300, 200))

    img1 = ImageTk.PhotoImage(image_disp)
    img2 = ImageTk.PhotoImage(thermal_disp)
    img3 = ImageTk.PhotoImage(highlight_disp)

    # Display in popup
    popup = tk.Toplevel()
    popup.title("Thermal Simulation and Hot Zones")

    lbl1 = tk.Label(popup, image=img1, text="Original", compound="top")
    lbl2 = tk.Label(popup, image=img2, text="Thermal", compound="top")
    lbl3 = tk.Label(popup, image=img3, text="Hot Zones", compound="top")

    lbl1.image = img1
    lbl2.image = img2
    lbl3.image = img3

    lbl1.grid(row=0, column=0, padx=10, pady=10)
    lbl2.grid(row=0, column=1, padx=10, pady=10)
    lbl3.grid(row=0, column=2, padx=10, pady=10)

# Main GUI
root = tk.Tk()
root.title("Thermal Detector")

tk.Label(root, text="Upload an image to simulate thermal view and detect hot zones", font=("Arial", 12)).pack(pady=20)
tk.Button(root, text="Upload Image", command=simulate_thermal_and_display, font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 12)).pack(pady=10)

root.mainloop()
