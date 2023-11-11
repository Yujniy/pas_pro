import random
import string
import customtkinter as ctk
import datetime
import pandas as pd
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def generate_password():
    length = int(length_slider.get())
    characters = ""
    if include_symbols.get():
        characters += string.punctuation
    if include_uppercase.get():
        characters += string.ascii_uppercase
    if include_lowercase.get():
        characters += string.ascii_lowercase
    if include_digits.get():
        characters += string.digits
    forbidden_characters = forbidden_entry.get().strip()
    if forbidden_characters:
        characters = characters.translate(str.maketrans("", "", forbidden_characters))
    required_characters = required_entry.get().strip()
    if required_characters:
        characters += required_characters
    if not (include_symbols.get() or include_uppercase.get() or include_lowercase.get() or include_digits.get()):
        ctk.messagebox.showerror("Ошибка", "Необходимо выбрать хотя бы один тип символов")
        required_entry.configure(state=ctk.DISABLED)
        forbidden_entry.configure(state=ctk.DISABLED)
        return
    password = ''.join(random.choice(characters) for _ in range(length))
    if required_characters:
        password = insert_required_characters(password, required_characters)
    save_password(password)
    password_entry.delete(0, ctk.END)
    password_entry.insert(0, password)

def insert_required_characters(password, required_characters):
    required_characters = required_characters.split(',')
    for char in required_characters:
        if char not in password:
            password += char
    return password

def save_password(password):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("passwords.txt", "a") as file:
        file.write(f"{password} ({date})\n")

def convert_to_excel():
    df = pd.read_csv("passwords.txt", delimiter="(", header=None, names=["Пароль", "Дата генерации"])
    df["Дата генерации"] = df["Дата генерации"].str.replace(")", "")
    df.to_excel("passwords.xlsx", index=False)

def update_length_counter(value):
    length_counter.configure(text=f"Длина пароля: {int(value)}")

def update_required_entry_state():
    if include_symbols.get() or include_uppercase.get() or include_lowercase.get() or include_digits.get():
        required_entry.configure(state=ctk.NORMAL)
        forbidden_entry.configure(state=ctk.NORMAL)
    else:
        required_entry.configure(state=ctk.DISABLED)
        forbidden_entry.configure(state=ctk.DISABLED)

window = ctk.CTk()
window.title("Генератор паролей")

# Загрузка изображения
image = Image.open("Pasgen/logo.png")
photo = ImageTk.PhotoImage(image)
logo_label = ctk.CTkLabel(window, image=photo)
logo_label.pack()

# Удаление надписи CTkLabel
logo_label.configure(text="")

length_label = ctk.CTkLabel(window, text="Длина пароля:")
length_label.pack()

length_counter = ctk.CTkLabel(window, text="Длина пароля: 5")
length_counter.pack()

length_slider = ctk.CTkSlider(window, from_=1, to=50, number_of_steps=50, command=update_length_counter)
length_slider.pack()
length_slider.set(5)

include_symbols = ctk.CTkCheckBox(window, text="Символы", command=update_required_entry_state)
include_symbols.pack()

include_uppercase = ctk.CTkCheckBox(window, text="Заглавные буквы", command=update_required_entry_state)
include_uppercase.pack()

include_lowercase = ctk.CTkCheckBox(window, text="Строчные буквы", command=update_required_entry_state)
include_lowercase.pack()

include_digits = ctk.CTkCheckBox(window, text="Цифры", command=update_required_entry_state)
include_digits.pack()

required_label = ctk.CTkLabel(window, text="Обязательные символы (через запятую):")
required_label.pack()

required_entry = ctk.CTkEntry(window, state=ctk.DISABLED)
required_entry.pack()

forbidden_label = ctk.CTkLabel(window, text="Запрещенные символы (через запятую):")
forbidden_label.pack()

forbidden_entry = ctk.CTkEntry(window, state=ctk.DISABLED)
forbidden_entry.pack()

generate_button = ctk.CTkButton(window, text="Сгенерировать пароль", command=generate_password)
generate_button.pack()

convert_button = ctk.CTkButton(window, text="Конвертировать в Excel", command=convert_to_excel)
convert_button.pack()

password_label = ctk.CTkLabel(window, text="Пароль:")
password_label.pack()

password_entry = ctk.CTkEntry(window)
password_entry.pack()

window.mainloop()
