import cv2
import os
import numpy as np
import csv
import glob
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

# File paths and directories
CSV_FILE = "face_details.csv"
DATASET_DIR = "dataset"
OUTPUT_DIR = "recognized_faces"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

THRESHOLD = 100  # Adjusted threshold; increase if needed
PERSISTENCE_TIME = 2  # Seconds to keep details displayed after last match

def load_database():
    database = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    database[int(row["id"])] = row
                except ValueError:
                    pass
    return database

def train_identifier():
    database = load_database()
    images, labels = [], []
    for id in database:
        pattern = os.path.join(DATASET_DIR, f"{id}*.jpg")
        files = glob.glob(pattern)
        if not files:
            single_path = os.path.join(DATASET_DIR, f"{id}.jpg")
            if os.path.exists(single_path):
                files = [single_path]
        for file in files:
            img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            # Resize image to a consistent size for training
            img = cv2.resize(img, (200, 200))
            images.append(img)
            labels.append(id)
    if len(images) == 0:
        return None, database
    identifier = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
    identifier.train(images, np.array(labels))
    return identifier, database

def identify_faces_live_with_details():
    win = tk.Toplevel()
    win.title("Live Face Identification")
    win.geometry("1200x600")
    win.configure(bg="#1E1E1E")
    
    # Left frame: Live camera feed
    left_frame = tk.Frame(win, bg="#333333", padx=10, pady=10)
    left_frame.pack(side="left", fill="both", expand=True)
    tk.Label(left_frame, text="Live Camera Feed", font=("Arial", 14, "bold"), fg="white", bg="#333333").pack(pady=5)
    camera_label = tk.Label(left_frame, bg="black")
    camera_label.pack(padx=10, pady=10)
    
    # Right frame: Identified details
    right_frame = tk.Frame(win, bg="#444444", padx=20, pady=20)
    right_frame.pack(side="right", fill="y")
    tk.Label(right_frame, text="Identified Details", font=("Arial", 16, "bold"), fg="white", bg="#444444").pack(pady=10)
    
    # Create labels to display details
    detail_labels = {}
    for field in ["Name", "Age", "Location", "Country"]:
        lbl = tk.Label(right_frame, text=f"{field}: ", font=("Arial", 14), fg="white", bg="#444444")
        lbl.pack(anchor="w", pady=5)
        detail_labels[field.lower()] = lbl

    def go_back():
        cap.release()
        win.destroy()
    tk.Button(right_frame, text="Back", command=go_back, font=("Arial", 14),
              bg="#E74C3C", fg="white", width=15).pack(pady=10)

    # Train the recognizer
    identifier, database = train_identifier()
    if identifier is None:
        messagebox.showerror("Error", "No trained data available. Please add at least one face to the dataset.")
        win.destroy()
        return

    # Initialize Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Use DirectShow backend (cv2.CAP_DSHOW) to attempt to avoid MSMF issues
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to access the camera.")
        win.destroy()
        return

    last_identified_record = None
    last_identified_time = 0

    def update_frame():
        nonlocal last_identified_record, last_identified_time
        ret, frame = cap.read()
        if not ret:
            win.after(10, update_frame)
            return
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        current_identified = None

        for (x, y, w, h) in faces:
            color, text = (0, 0, 255), "Unknown"
            if identifier is not None:
                face_roi = gray[y:y+h, x:x+w]
                try:
                    face_roi = cv2.resize(face_roi, (200, 200))
                except Exception:
                    continue
                label, confidence = identifier.predict(face_roi)
                # Optionally, print debug info:
                # print(f"Predicted Label: {label}, Confidence: {confidence}")
                if confidence < THRESHOLD:
                    record = database.get(label, {})
                    text = f"{record.get('name', 'Unknown')}"
                    color = (255, 0, 0)
                    current_identified = record
                    last_identified_record, last_identified_time = record, time.time()
                    for key in detail_labels:
                        detail_labels[key].config(text=f"{key.capitalize()}: {record.get(key, 'N/A')}")
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        if not current_identified and last_identified_record and (time.time() - last_identified_time) < PERSISTENCE_TIME:
            for key in detail_labels:
                detail_labels[key].config(text=f"{key.capitalize()}: {last_identified_record.get(key, 'N/A')}")
        elif not current_identified:
            for key in detail_labels:
                detail_labels[key].config(text=f"{key.capitalize()}: ")
            last_identified_record = None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.config(image=imgtk)
        camera_label.image = imgtk

        win.after(10, update_frame)

    update_frame()

    def on_closing():
        cap.release()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    identify_faces_live_with_details()
