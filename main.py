from openai import OpenAI
import ttkbootstrap as tb
from tkinter import ttk, PhotoImage, messagebox
import sqlite3

explanation_ai = "Please write a product description for the given item, ensuring it highlights its features. The description should be concise, around 250 characters, to be used for online sales."
client = OpenAI(api_key="YOUR_API_KEY_HERE")
connection = sqlite3.connect("Products.db")
cursor = connection.cursor()

def ask_questions_ai(prompt):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
                                                    messages=[{"role": "user", "content": prompt + explanation_ai}])
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

# Set window
window = tb.Window(themename='vapor')
window.title("ProductPal")
photo_path = "icon.png"
try:
    photo = PhotoImage(file=photo_path)
    window.iconphoto(True, photo)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load the icon photo. Please update the photo_path.\n\nError: {e}")

window.geometry('1080x720')
window.resizable(False, False)

def create_new_window():
    new_window = tb.Toplevel(window)
    new_window.title("Product Pal")
    new_window.geometry("800x460")
    new_window.resizable(False, False)
    exp_err = tb.Label(new_window, foreground="red", text="*Due to OpenAI error 429, we are unable to automatically generate product descriptions at the moment. Therefore, we will \nmanually enter the information and provide the ready-made description to the user. If you encounter any issues or need\nfurther assistance, please contact us.")
    exp_err.place(x=10, y=10)
    name_label_new = tb.Label(new_window, text="NAME:")
    name_label_new.place(x=10, y=105)
    name_entry_new = tb.Entry(new_window, width=30)
    name_entry_new.place(x=90, y=100)
    feat_label = tb.Label(new_window, text="FEATURES:")
    feat_label.place(x=10, y=155)
    feat_entry = tb.Entry(new_window, width=30)
    feat_entry.place(x=90, y=155)
    warranty_label = tb.Label(new_window, text="WARRANTY \nPERIOD:")
    warranty_label.place(x=10, y=210)
    warranty_entry = tb.Entry(new_window, width=30)
    warranty_entry.place(x=90, y=212)
    origin_label = tb.Label(new_window, text="ORIGIN:")
    origin_label.place(x=10, y=275)
    origin_entry = tb.Entry(new_window, width=30)
    origin_entry.place(x=90, y=270)
    use_label = tb.Label(new_window, text="AREAS OF\n USE:")
    use_label.place(x=10, y=325)
    use_entry = tb.Entry(new_window, width=30)
    use_entry.place(x=90, y=323)
    send_but_new = tb.Button(new_window, width=29, bootstyle="secondary", text="SEND", command=lambda: on_send_new_click(new_text_box, name_entry_new, feat_entry, origin_entry, use_entry, warranty_entry))
    send_but_new.place(x=90, y=370)
    new_text_box = tb.Text(new_window, width=40, height=15)
    new_text_box.place(x=400, y=100)
    copy_but = tb.Button(new_window, text="COPY", width=39, bootstyle="info", command=lambda: show_suc(new_text_box))
    copy_but.place(x=400, y=370)
    new_window.new_text_box = new_text_box

def on_send_new_click(new_text_box, name_entry_new, feat_entry, origin_entry, use_entry, warranty_entry):
    name = name_entry_new.get().strip()
    features = feat_entry.get().strip()
    warranty = warranty_entry.get().strip()
    origin = origin_entry.get().strip()
    usage = use_entry.get().strip()

    if not (name and features and warranty and origin and usage):
        messagebox.showwarning("Incomplete Information", "Please fill in all fields.")
        return

    messagebox.showinfo("Success", "SUCCEEDED")
    fallback_description = (
        f"Introducing the {name}, a top-of-the-line product designed for exceptional performance. "
        f"Key features include: {features}. With a warranty period of {warranty}, you can rest assured of its durability. "
        f"Manufactured in {origin}, this product is perfect for {usage}."
    )

    name_entry_new.delete(0, tb.END)
    feat_entry.delete(0, tb.END)
    origin_entry.delete(0, tb.END)
    warranty_entry.delete(0, tb.END)
    use_entry.delete(0, tb.END)
    
    new_text_box.delete("1.0", tb.END)
    new_text_box.insert(tb.END, fallback_description)

def on_button_click():
    user_input = text_box.get("1.0", tb.END).strip()
    text_box.delete("1.0", tb.END)
    result = ask_questions_ai(user_input)
    if result != -1:
        send_but.config(text="SUCCESS", bootstyle="success")
        window.after(2000, reset_button)
    else:
        send_but.config(text="FAILED", bootstyle="danger")
        window.after(2000, reset_button)
        create_new_window()

def reset_button():
    send_but.config(text="SEND", bootstyle="secondary")

def on_button_click_saving():
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    total = total_entry.get().strip()

    if not (name and price and total):
        messagebox.showwarning("Incomplete Information", "Please fill in all fields.")
        return

    cursor.execute("INSERT INTO Products (NAME, PRICE, TOTAL) VALUES (?, ?, ?)", (name, price, total))
    connection.commit()
    save_button.config(text="SUCCESS", bootstyle="success")
    window.after(2000, reset_button_saving)

def reset_button_saving():
    save_button.config(text="SAVE", bootstyle="warning")

def show_suc(new_text_box):
    try:
        text_to_copy = new_text_box.get("1.0", tb.END).strip()
        if text_to_copy:
            window.clipboard_clear()
            window.clipboard_append(text_to_copy)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No text to copy.")
        new_text_box.delete("1.0", tb.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy text. Error: {e}")

def list_all_products():
    for i in table.get_children():
        table.delete(i)

    cursor.execute("SELECT NAME, PRICE, TOTAL FROM Products")
    rows = cursor.fetchall()
    for row in rows:
        table.insert("", tb.END, values=row)
def delete_selected_product():
    selected_item = table.selection()
    if selected_item:
        item = table.item(selected_item)
        name = item['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            cursor.execute("DELETE FROM Products WHERE NAME=?", (name,))
            connection.commit()
            table.delete(selected_item)
            messagebox.showinfo("Success", f"Product {name} deleted successfully.")
    else:
        messagebox.showwarning("Warning", "No product selected.")

# Set widgets
text_box = tb.Text(window, height=10, width=52)
text_box.place(x=575, y=25)
sep_first = ttk.Separator(window, orient='vertical')
sep_first.place(x=540, y=25, height=200)
sep_sec = ttk.Separator(window, orient='horizontal')
sep_sec.place(x=10, y=255, width=1060)
sep_third = ttk.Separator(window, orient='vertical')
sep_third.place(x=540, y=285, height=410)
send_but = tb.Button(window, width=51, text="SEND", bootstyle="secondary", command=on_button_click)
send_but.place(x=575, y=210)
table = tb.Treeview(window, height=23, bootstyle="primary", show="headings")
table["columns"] = ("name", "price", "total")
table.column("name", width=155)
table.column("price", width=155)
table.column("total", width=155)
table.heading("name", text="NAME")
table.heading("price", text="PRICE")
table.heading("total", text="TOTAL")
table.place(x=30, y=280)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=table.yview)
scrollbar.place(x=510, y=280, height=410)
table.configure(yscrollcommand=scrollbar.set)
list_button = tb.Button(window, width=51, bootstyle="info", text="LIST ALL PRODUCTS", command=list_all_products)
list_button.place(x=575, y=600)
delete_but = tb.Button(window, width=51, bootstyle="danger", text="DELETE THE SELECTED PRODUCT", command=delete_selected_product)
delete_but.place(x=575, y=660)
name_label = tb.Label(window, text="NAME:", foreground="white")
name_label.place(x=575, y=298)
name_entry = tb.Entry(width=45)
name_entry.place(x=630, y=295)
price_label = tb.Label(window, text="PRICE:", foreground="white")
price_label.place(x=575, y=378)
price_entry = tb.Entry(width=45)
price_entry.place(x=630, y=375)
total_label = tb.Label(window, text="TOTAL:", foreground="white")
total_label.place(x=575, y=468)
total_entry = tb.Entry(width=45)
total_entry.place(x=630, y=465)
save_button = tb.Button(window, width=44, bootstyle="warning", text="SAVE", command=on_button_click_saving)
save_button.place(x=630, y=520)

# Explanation about program and set labels
explanation = tb.Label(window, text="PLEASE PROVIDE THE FOLLOWING DETAILS ABOUT THE PRODUCT:")
explanation.place(x=10, y=25)
explanation_two = tb.Label(window, text="1. Product name and model: The complete name of the product and its model number.")
explanation_two.place(x=10, y=50)
explanation_three = tb.Label(window, text="2. Key features: Main features like size, weight, material, and color options.")
explanation_three.place(x=10, y=75)
explanation_four = tb.Label(window, text="3. Usage: How and for what purposes the product is used.")
explanation_four.place(x=10, y=100)
explanation_five = tb.Label(window, text="4. Benefits and advantages: The main benefits and advantages for the user.")
explanation_five.place(x=10, y=125)
explanation_six = tb.Label(window, text="5. Warranty and customer support: Warranty period and customer support details.")
explanation_six.place(x=10, y=150)
explanation_seven = tb.Label(window, text="6. Care and usage instructions: Important maintenance and usage guidelines.")
explanation_seven.place(x=10, y=175)
explanation_eight = tb.Label(window, text="7. Extras: Additional info such as reviews, certifications, or awards.")
explanation_eight.place(x=10, y=200)

# Ensure the program closes gracefully
window.protocol("WM_DELETE_WINDOW", window.quit)
window.mainloop()
connection.close()
