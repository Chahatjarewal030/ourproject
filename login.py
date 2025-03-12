import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    # Get trimmed values from the entries
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    # Check credentials (update these as needed)
    if username == "chahataankita" and password == "5687":
        messagebox.showinfo("Login Success", "Welcome!")
        login_window.destroy()  # Close the login window
        
        # Import main locally to avoid circular dependency issues
        import main  
        main.run_app()  # Launch the main menu (starting window)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Create the main login window
login_window = tk.Tk()
login_window.title("Login - Face Track Pro")
login_window.geometry("400x600")
login_window.configure(bg="#f0f0f0")

# Create a frame for the login contents
login_frame = tk.Frame(login_window, bg="#f0f0f0")
login_frame.pack(expand=True)

# Try to load and display a logo image
try:
    logo_path = r"C:\Users\91750\OneDrive\Desktop\major project\logo.png.png"
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((250, 250))
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(login_frame, image=logo_photo, bg="#f0f0f0")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=(20, 10))
except Exception as e:
    print("Error loading logo:", e)
    tk.Label(login_frame, text="Face Track Pro", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=(20, 10))

# Display a welcome message
tk.Label(login_frame, text="Welcome Face Track Pro", font=("Arial", 20, "bold"), bg="#f0f0f0")\
    .pack(pady=(10, 20))

# Create a frame for credentials (username and password)
credentials_frame = tk.Frame(login_frame, bg="#f0f0f0")
credentials_frame.pack(pady=(10, 20))

tk.Label(credentials_frame, text="Username:", font=("Arial", 14), bg="#f0f0f0")\
    .grid(row=0, column=0, sticky="e", padx=10, pady=10)
username_entry = tk.Entry(credentials_frame, font=("Arial", 14), width=20)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(credentials_frame, text="Password:", font=("Arial", 14), bg="#f0f0f0")\
    .grid(row=1, column=0, sticky="e", padx=10, pady=10)
password_entry = tk.Entry(credentials_frame, font=("Arial", 14), show="*", width=20)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Login button
tk.Button(login_frame, text="Login", command=login, font=("Arial", 14),
          width=15, height=2, bg="#4CAF50", fg="white")\
    .pack(pady=20)

login_window.mainloop()
