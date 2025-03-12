import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Corrected file paths
GENDER_MODEL = r"D:\facetrackpro\gender_net.caffemodel"
GENDER_PROTO = r"D:\facetrackpro\gender_deploy.prototxt"

# Define class labels
GENDER_LIST = ['Male', 'Female']

def load_model():
    """Load gender detection model with error handling."""
    if not os.path.exists(GENDER_MODEL) or not os.path.exists(GENDER_PROTO):
        return None, "Gender model files are missing. Please check the paths."

    try:
        gender_net = cv2.dnn.readNetFromCaffe(GENDER_PROTO, GENDER_MODEL)
        return gender_net, None
    except cv2.error as e:
        return None, f"Failed to load gender detection model:\n{e}"

def detect_faces_and_gender(image_path):
    """Detect faces and classify gender using a deep learning model."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Invalid image file.")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        num_men, num_women = 0, 0

        for (x, y, w, h) in faces:
            face_img = image[y:y+h, x:x+w].copy()  # Extract face ROI
            blob = cv2.dnn.blobFromImage(face_img, scalefactor=1.0, size=(227, 227), 
                                         mean=(78.426, 87.768, 114.895), swapRB=False)

            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = GENDER_LIST[gender_preds[0].argmax()]

            if gender == 'Male':
                num_men += 1
            else:
                num_women += 1

        return len(faces), num_men, num_women

    except Exception as e:
        return 0, 0, 0  # Return default values

def run_upload_window():
    """Runs the image upload and analysis window."""
    global gender_net  # Ensure model is loaded in global scope

    upload_window = tk.Toplevel()
    upload_window.title("Upload Image")
    upload_window.geometry("700x500")
    upload_window.configure(bg="#1E1E1E")

    # Load model when opening the window
    gender_net, model_error = load_model()
    if model_error:
        messagebox.showerror("Error", model_error)
        upload_window.destroy()
        return

    def upload_image():
        """Uploads an image, detects faces, and classifies gender."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return  # No file selected

        try:
            img = Image.open(file_path)
            img = img.resize((250, 250))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk  # Keep reference to avoid garbage collection

            # Detect faces and update entries
            num_faces, num_men, num_women = detect_faces_and_gender(file_path)
            entry_num.delete(0, tk.END)
            entry_num.insert(0, str(num_faces))

            entry_men.delete(0, tk.END)
            entry_men.insert(0, str(num_men))

            entry_women.delete(0, tk.END)
            entry_women.insert(0, str(num_women))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image:\n{e}")

    # === Left Side (Buttons) ===
    button_frame = tk.Frame(upload_window, bg="#2C2C2C", padx=10, pady=10)
    button_frame.pack(side="left", fill="y")

    tk.Label(button_frame, text="Options", font=("Arial", 14, "bold"), fg="white", bg="#2C2C2C").pack(pady=10)
    
    btn_upload = tk.Button(button_frame, text="Choose Image", 
                           command=upload_image,
                           width=15, height=2, bg="#3498DB", fg="white", font=("Arial", 10, "bold"))
    btn_upload.pack(pady=10)

    btn_close = tk.Button(button_frame, text="Exit", 
                          command=upload_window.destroy, 
                          width=15, height=2, bg="#E74C3C", fg="white", font=("Arial", 10, "bold"))
    btn_close.pack(pady=10)

    # === Right Side (Form Fields & Image Display) ===
    form_frame = tk.Frame(upload_window, bg="#1E1E1E", padx=20, pady=20)
    form_frame.pack(side="right", fill="both", expand=True)

    tk.Label(form_frame, text="Upload Image Details", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E").pack(pady=10)

    tk.Label(form_frame, text="Total Persons:", fg="white", bg="#1E1E1E", font=("Arial", 12)).pack(anchor="w")
    entry_num = tk.Entry(form_frame, width=30)
    entry_num.pack(pady=5)

    tk.Label(form_frame, text="Number of Men:", fg="white", bg="#1E1E1E", font=("Arial", 12)).pack(anchor="w")
    entry_men = tk.Entry(form_frame, width=30)
    entry_men.pack(pady=5)

    tk.Label(form_frame, text="Number of Women:", fg="white", bg="#1E1E1E", font=("Arial", 12)).pack(anchor="w")
    entry_women = tk.Entry(form_frame, width=30)
    entry_women.pack(pady=5)

    # Image Display Label
    img_label = tk.Label(form_frame, bg="#1E1E1E")  # Light black placeholder for uploaded image
    img_label.pack(pady=10)

    upload_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    run_upload_window()  # Explicitly call function to ensure it runs
