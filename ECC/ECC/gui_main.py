import tkinter as tk
from tkinter import filedialog, messagebox
from ecc_utils import encrypt_ECC, decrypt_ECC, curve
from steg_utils import encode_text_to_image, decode_text_from_image
import base64
from PIL import Image, ImageTk

privKey = 987654321
pubKey = privKey * curve.g

def embed_message():
    message = entry.get()
    if not message:
        messagebox.showerror("Error", "Message is empty!")
        return
    # Clean input to ASCII only
    message = message.encode("ascii", "ignore").decode()

    image_path = filedialog.askopenfilename(title="Select Cover Image")
    if not image_path:
        return

    cipher_point, cipher_text = encrypt_ECC(message, pubKey)
    # Safely decode to ASCII, ignoring non-ASCII bytes
    encoded = base64.b64encode(cipher_text).decode('ascii', errors='ignore')
    encode_text_to_image(image_path, encoded, "stego_image.png")
    messagebox.showinfo("Success", "Message embedded and image saved as 'stego_image.png'")
    global saved_cipher_point
    saved_cipher_point = cipher_point

def extract_message():
    image_path = filedialog.askopenfilename(title="Select Stego Image")
    if not image_path:
        return
    try:
        length = int(entry_len.get())
        extracted = decode_text_from_image(image_path, length)
        cipher_bytes = base64.b64decode(extracted)
        decrypted = decrypt_ECC((saved_cipher_point, cipher_bytes), privKey)
        result.config(text=f"Decrypted: {decrypted}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("ECC Image Steganography")
app.geometry("500x300")

tk.Label(app, text="Enter message to hide:").pack()
entry = tk.Entry(app, width=50)
entry.pack(pady=5)

tk.Button(app, text="Encrypt & Embed", command=embed_message).pack(pady=10)

tk.Label(app, text="Enter cipher length (approx):").pack()
entry_len = tk.Entry(app, width=10)
entry_len.pack(pady=5)

tk.Button(app, text="Extract & Decrypt", command=extract_message).pack(pady=10)

result = tk.Label(app, text="", wraplength=400)
result.pack(pady=10)

app.mainloop()