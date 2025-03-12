import tkinter as tk
from tkinter import filedialog
import face_capture
import face_identification  # Ensure this module exists and contains the required functions
import upload_image        # Ensure this module exists and contains the required functions

def open_face_capture():
    print("Face Capture Button Clicked")
    face_capture.capture_with_details()

def open_face_identification():
    print("Face Identification Button Clicked")
    face_identification.identify_faces_live_with_details()

def open_video_analysis():
    print("Video Analysis Button Clicked")
    file_path = filedialog.askopenfilename(title="Select a Video", filetypes=[("Video Files", "*.mp4;*.avi")])
    if file_path:
        face_identification.identify_faces_in_video(file_path)

def open_upload_image():
    print("Upload Image Button Clicked")
    upload_image.run_upload_window()

def run_app():
    root = tk.Tk()
    root.title("Face Track Pro - Main Menu")
    root.geometry("700x400")
    root.configure(bg="black")

    tk.Label(root, text="Face Track Pro", font=("Arial", 24, "bold"), bg="black", fg="white").pack(pady=20)
    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(pady=10)

    button_style = {"width": 25, "height": 2, "font": ("Arial", 12, "bold"), "bg": "white", "fg": "black"}
    tk.Button(button_frame, text="Face Capture", command=open_face_capture, **button_style).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Face Identification", command=open_face_identification, **button_style).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(button_frame, text="Upload Image", command=open_upload_image, **button_style).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Video Analysis", command=open_video_analysis, **button_style).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Exit", command=root.quit, width=25, height=2, font=("Arial", 12, "bold"), bg="white", fg="black").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_app()
