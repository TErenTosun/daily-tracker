"""Database and GUI"""
import datetime
import sqlite3 as sql
import tkinter as tk
import customtkinter as ctk

TABLE_INIT = """CREATE TABLE IF NOT EXISTS tracker(id integer primary key autoincrement, 
date, water, sleep, food, meds, headache, bodyache, notes)"""
TABLE_GET = """SELECT date, water, sleep, food, meds, headache,
bodyache, notes FROM tracker"""
TABLE_INSERT = """INSERT INTO tracker(date, water, sleep, food, meds, headache,
bodyache, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
FETCH_DATA = """SELECT id, date, water, sleep, food, meds, headache,
bodyache, notes FROM tracker ORDER BY id DESC LIMIT 7"""

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
appWidth, appHeight = 750, 600

with sql.connect("database.db", timeout=10) as con:
    cur = con.cursor()
cur.execute(TABLE_INIT)

res = cur.execute(TABLE_GET)
"""Data window initialisation"""


class dataWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{appWidth}, {appHeight}")
        self.title("Data Window")
        fetch_data = cur.execute(FETCH_DATA)
        i = 1  # Index for increment
        self.id_label = tk.Label(
            self, text="ID", fg="blue", width=20, anchor="w")
        self.id_label.grid(row=0, column=0)

        self.date_label = tk.Label(
            self, text="Date", fg="blue", width=20, anchor="w")
        self.date_label.grid(row=0, column=1)

        self.water_label = tk.Label(
            self, text="Water (L)", fg="blue", width=20, anchor="w")
        self.water_label.grid(row=0, column=2)

        self.sleep_label = tk.Label(
            self, text="Sleep (Hours)", fg="blue", width=20, anchor="w")
        self.sleep_label.grid(row=0, column=3)

        self.food_label = tk.Label(
            self, text="Food", fg="blue", width=20, anchor="w")
        self.food_label.grid(row=0, column=4)

        self.meds_label = tk.Label(
            self, text="Meds", fg="blue", width=20, anchor="w")
        self.meds_label.grid(row=0, column=5)

        self.headache_label = tk.Label(
            self, text="Headache", fg="blue", width=20, anchor="w")
        self.headache_label.grid(row=0, column=6)

        self.bodyache_label = tk.Label(
            self, text="Bodyache", fg="blue", width=20, anchor="w")
        self.bodyache_label.grid(row=0, column=7)

        self.notes_label = tk.Label(
            self, text="Notes", fg="blue", width=20, anchor="w")
        self.notes_label.grid(row=0, column=8)
        for data in fetch_data:
            for j in range(len(data)):
                data_label = tk.Label(self, width=20, fg="blue",
                                      text=data[j], anchor="w")
                if data[j] == 0:
                    data_label = tk.Label(self, width=20, fg="blue",
                                          text="No", anchor="w")
                elif j == 6 and data[j] == 1 or j == 7 and data[j] == 1:
                    data_label = tk.Label(self, width=20, bg="red",
                                          text="Yes", anchor="w")
                data_label.grid(row=i, column=j)
            i += 1


class App(ctk.CTk):
    """Initialise App"""

    def __init__(self):
        super().__init__()

        self.geometry(f"{appWidth}x{appHeight}")
        self.title("Tracker App")

        self.water_label = ctk.CTkLabel(master=self, text="Water (L)")
        self.water_label.grid(row=0, column=0, padx=20, pady=20)
        self.water = ctk.CTkEntry(master=self, placeholder_text="Water (L)")
        self.water.grid(row=0, column=1, padx=20, pady=20)

        self.sleep_label = ctk.CTkLabel(master=self, text="Sleep (hours)")
        self.sleep_label.grid(row=1, column=0, padx=20, pady=20)
        self.sleep = ctk.CTkEntry(
            master=self, placeholder_text="Sleep (hours)")
        self.sleep.grid(row=1, column=1, padx=20, pady=20)

        self.food_label = ctk.CTkLabel(master=self, text="Food")
        self.food_label.grid(row=0, column=2, padx=20, pady=20)
        self.food = ctk.CTkEntry(master=self, placeholder_text="Food")
        self.food.grid(row=0, column=3, padx=20, pady=20)

        self.meds_label = ctk.CTkLabel(master=self, text="Medications")
        self.meds_label.grid(row=1, column=2, padx=20, pady=20)
        self.meds = ctk.CTkEntry(master=self, placeholder_text="Medications")
        self.meds.grid(row=1, column=3, padx=20, pady=20)

        self.headache = ctk.BooleanVar()
        self.headache_label = ctk.CTkLabel(master=self, text="Headache")
        self.headache_label.grid(row=4, column=0, padx=20, pady=20)
        self.headache_checkbox = ctk.CTkCheckBox(
            master=self, text=None, variable=self.headache, onvalue=True, offvalue=False)
        self.headache_checkbox.grid(row=4, column=1, padx=20, pady=20)

        self.bodyache = ctk.BooleanVar()
        self.bodyache_label = ctk.CTkLabel(master=self, text="Bodyache")
        self.bodyache_label.grid(row=5, column=0, padx=20, pady=20)
        self.bodyache_checkbox = ctk.CTkCheckBox(
            master=self, text=None, variable=self.bodyache, onvalue=True, offvalue=False)
        self.bodyache_checkbox.grid(row=5, column=1, padx=20, pady=20)

        self.notes_label = ctk.CTkLabel(master=self, text="Notes")
        self.notes_label.grid(row=6, column=0, padx=20, pady=20)
        self.notes = ctk.CTkEntry(master=self, placeholder_text="Notes")
        self.notes.grid(row=6, column=1, padx=20, pady=20)

        def waterbmit():
            water = self.water.get()
            sleep = self.sleep.get()
            food = self.food.get()
            notes = self.notes.get()
            head_ache = self.headache.get()
            body_ache = self.bodyache.get()
            meds = self.meds.get()
            current_date = datetime.date.today()
            cur.execute(TABLE_INSERT, (current_date, water, sleep,
                        food, meds, head_ache, body_ache, notes))
            con.commit()
            print(f"""Date: {current_date}
Water: {water}
Sleep: {sleep}
Food: {food}
Meds: {meds}
Headache: {head_ache}
Bodyache: {body_ache}
Notes: {notes}
""")

        def open_data_window():
            data = dataWindow()
            data.resizable(False, False)
            data.mainloop()

        self.waterbmit_button = ctk.CTkButton(
            master=self, text="Send", command=waterbmit)
        self.waterbmit_button.grid(row=7, column=2, pady=20)

        self.retrieve_data_button = ctk.CTkButton(
            master=self, text="View", command=open_data_window)
        self.retrieve_data_button.grid(row=9, column=2, pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
