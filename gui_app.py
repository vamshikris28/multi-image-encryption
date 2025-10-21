import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from encryption_module import modified_encryption, modified_decryption
from utils.image_utils import load_images, save_images
import os
import threading

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MD5 + SHA256 Image Encryption")
        self.root.geometry("500x300")
        
        # Increase PIL limit for large images
        Image.MAX_IMAGE_PIXELS = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Password Entry
        tk.Label(self.root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
        self.password_entry = tk.Entry(self.root, show='*', width=30)
        self.password_entry.pack(pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate')
        self.progress.pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Encrypt Images", 
                 command=self.start_encryption,
                 bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Decrypt Images",
                 command=self.start_decryption,
                 bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
    
    def update_status(self, message, is_error=False):
        color = "red" if is_error else "black"
        self.status_label.config(text=message, fg=color)
        self.root.update()
    
    def start_encryption(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return
            
        try:
            self.progress['value'] = 0
            self.update_status("Loading images...")
            
            # Run encryption in separate thread
            thread = threading.Thread(target=self.run_encryption, args=(password,))
            thread.start()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", True)
            
    def run_encryption(self, password):
        try:
            # Load images
            images = load_images("input_images")
            if not images:
                self.update_status("No images found in input folder!", True)
                return
                
            self.progress['value'] = 30
            self.update_status("Encrypting images...")
            
            # Encrypt
            encrypted_images, keys = modified_encryption(images, password)
            self.progress['value'] = 60
            
            # Save results
            self.update_status("Saving encrypted images...")
            save_images(encrypted_images, "output_encrypted", "encrypted")
            self.progress['value'] = 100
            
            self.update_status("✅ Encryption completed successfully!")
            messagebox.showinfo("Success", "Images encrypted successfully!")
            
        except PIL.Image.DecompressionBombError:
            self.update_status("Image too large! Please use smaller images.", True)
        except Exception as e:
            self.update_status(f"Error during encryption: {str(e)}", True)
    
    def start_decryption(self):
        # Similar implementation for decryption
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
