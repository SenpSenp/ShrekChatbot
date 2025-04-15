import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

from chat import MovieChatbot

bot = MovieChatbot()
bot.load_script("Shrek", "data/scripts/shrek_wikipedia.txt")

def send_message(event=None):
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_area.insert(tk.END, "Você: " + user_input + "\n", "user")
    entry.delete(0, tk.END)

    try:
        response = bot.respond(user_input)
    except Exception as e:
        response = f"Ocorreu um erro: {e}"

    chat_area.insert(tk.END, response + "\n", "bot")
    chat_area.see(tk.END)

def load_fixed_image(url):
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    im = im.resize((200, 200))
    return ImageTk.PhotoImage(im)

root = tk.Tk()
root.title("ShrekBot >:)")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
chat_area.pack(padx=10, pady=10)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="green")

entry = tk.Entry(root, width=50)
entry.pack(padx=10, side=tk.LEFT, expand=True, fill=tk.X)

send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(padx=10, side=tk.LEFT)

entry.bind("<Return>", send_message)

image_url = "https://live.staticflickr.com/2099/1490989031_e874d5f681_z.jpg"
image = load_fixed_image(image_url)

image_label = tk.Label(root, image=image)
image_label.image = image
image_label.pack(pady=10)

root.mainloop()
