import cv2
# Attempt to suppress warnings if supported; otherwise, ignore.
try:
    cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)
except AttributeError:
    pass

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import csv

# Absolute paths for CSV file and dataset folder
CSV_FILE = r"D:\facetrackpro\face_details.csv"
DATASET_DIR = r"D:\facetrackpro\dataset"

# Ensure the dataset directory exists
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# Create the CSV file with headers only if it doesn't exist already.
if not os.path.exists(CSV_FILE):
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "age", "location", "country"])
    except Exception as e:
        print("Error creating CSV file:", e)

def get_next_id():
    """Determine the next available ID by reading the CSV file."""
    try:
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ids = [int(row['id']) for row in reader if row['id'].isdigit()]
            return max(ids) + 1 if ids else 1
    except Exception:
        return 1

def save_details(id, name, age, location, country):
    """Append the provided face details to the CSV file."""
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id, name, age, location, country])
            f.flush()  # Ensure the data is written immediately.
    except Exception as e:
        print("Error saving details:", e)

def capture_with_details():
    """Opens a window with live camera feed and a form to capture face details."""
    win = tk.Toplevel()
    win.title("Live Face Capture with Details")
    win.geometry("1000x600")
    win.configure(bg="#1E1E1E")

    # Left frame: Live camera feed
    left_frame = tk.Frame(win, bg="#2C2C2C", padx=10, pady=10)
    left_frame.pack(side="left", fill="both", expand=True)
    tk.Label(left_frame, text="Live Camera Feed", font=("Arial", 14, "bold"), fg="white", bg="#2C2C2C").pack(pady=5)
    camera_label = tk.Label(left_frame, bg="black")
    camera_label.pack(padx=10, pady=10)

    # Right frame: Details entry form
    right_frame = tk.Frame(win, bg="#1E1E1E", padx=20, pady=20)
    right_frame.pack(side="right", fill="y")
    tk.Label(right_frame, text="Enter Details", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E").pack(pady=10)

    fields = [("Name:", "name"), ("Age:", "age"), ("Location:", "location"), ("Country:", "country")]
    entries = {}
    for label_text, key in fields:
        tk.Label(right_frame, text=label_text, font=("Arial", 14), fg="white", bg="#1E1E1E").pack(anchor="w")
        entry = tk.Entry(right_frame, font=("Arial", 14))
        entry.pack(fill="x", padx=5, pady=5)
        entries[key] = entry

    # Open the camera
    cap = cv2.VideoCapture(0)
    current_frame = None

    def update_frame():
        nonlocal current_frame
        ret, frame = cap.read()
        if ret:
            current_frame = frame.copy()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
        win.after(10, update_frame)

    def capture_image():
        nonlocal current_frame
        if current_frame is not None:
            name = entries["name"].get().strip()
            age = entries["age"].get().strip()
            location = entries["location"].get().strip()
            country = entries["country"].get().strip()
            if not (name and age and location and country):
                messagebox.showerror("Error", "Please fill all details before capturing.")
                return

            new_id = get_next_id()
            image_filename = f"{new_id}.jpg"
            image_path = os.path.join(DATASET_DIR, image_filename)
            cv2.imwrite(image_path, current_frame)
            save_details(new_id, name, age, location, country)
            messagebox.showinfo("Success", f"Face captured and details saved!\nImage: {image_filename}")

    tk.Button(right_frame, text="Capture Image", command=capture_image,
              font=("Arial", 14), bg="#27AE60", fg="white", width=15).pack(pady=10)
    tk.Button(right_frame, text="Back", command=lambda: [cap.release(), win.destroy()],
              font=("Arial", 14), bg="#E74C3C", fg="white", width=15).pack(pady=10)

    update_frame()
    win.protocol("WM_DELETE_WINDOW", lambda: [cap.release(), win.destroy()])
    win.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    capture_with_details()
