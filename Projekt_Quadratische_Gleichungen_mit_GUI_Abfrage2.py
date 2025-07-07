import math
import re
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox
import time

def parse_pq(gleichung):
    match = re.search(r'x²([+-]?\d*)x([+-]?\d+)=0', gleichung.replace(' ', ''))
    if match:
        p_str = match.group(1)
        q_str = match.group(2)
        if p_str == '':
            p = 1
        elif p_str == '+':
            p = 1
        elif p_str == '-':
            p = -1
        else:
            p = int(p_str)
        q = int(q_str)
        return p, q
    else:
        raise ValueError(f"Ungültige Gleichung: {gleichung}")

def teiler_analyse(n):
    liste_t = []
    liste_k = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            teiler = i
            komplementaer_teiler = n // i
            liste_t.append(teiler)
            liste_k.append(komplementaer_teiler)
    return liste_t, liste_k

def vorzeichen_analyse(a):
    if a == 0:
        return 0
    return abs(a) / a

def summen_analyse(p, q, listA, listB):
    for i in range(len(listA)):
        if abs(p) == listB[i] + vorzeichen_analyse(q) * listA[i]:
            zwischenloesung_1 = listB[i]
            zwischenloesung_2 = listA[i]
            return zwischenloesung_1, zwischenloesung_2
    return None, None

def loesung_bestimmen(p, q, zwischenloesung_1, zwischenloesung_2):
    if vorzeichen_analyse(q) == -1:
        if vorzeichen_analyse(p) == -1:
            loesung_1 = zwischenloesung_1
            loesung_2 = -zwischenloesung_2
        else:
            loesung_1 = -zwischenloesung_1
            loesung_2 = zwischenloesung_2
    else:
        if vorzeichen_analyse(p) == -1:
            loesung_1 = zwischenloesung_1
            loesung_2 = zwischenloesung_2
        else:
            loesung_1 = -zwischenloesung_1
            loesung_2 = -zwischenloesung_2
    return loesung_1, loesung_2

def loesung_schreiben(loesung_1, loesung_2):
    return f"Die erste Lösung ist: {loesung_1}\nDie zweite Lösung ist: {loesung_2}\n"

def loesung_mit_weg_berechnen(p, q):
    output = []
    output.append("Lösungsweg für die quadratische Gleichung x² + px + q = 0\n")
    output.append(f"Mit p = {p} und q = {q}\n")
    output.append("Schritt 1: Berechne -p/2\n")
    minus_p_halbe = -p / 2
    output.append(f"-p/2 = -({p})/2 = {minus_p_halbe}\n")
    output.append("Schritt 2: Berechne (p/2)²\n")
    p_halbe_quadr = (p / 2) ** 2
    output.append(f"(p/2)² = ({p}/2)² = {p_halbe_quadr}\n")
    output.append("Schritt 3: Berechne (p/2)² - q\n")
    diskriminante = p_halbe_quadr - q
    output.append(f"(p/2)² - q = {p_halbe_quadr} - ({q}) = {diskriminante}\n")
    output.append("Schritt 4: Berechne die Wurzel von (p/2)² - q\n")
    wurzel_diskriminante = math.sqrt(diskriminante)
    output.append(f"√({diskriminante}) = {wurzel_diskriminante}\n")
    output.append("Schritt 5: Berechne die Lösungen x₁ und x₂:\n")
    loesung_eins = minus_p_halbe + wurzel_diskriminante
    loesung_zwei = minus_p_halbe - wurzel_diskriminante
    output.append(f"x₁ = -p/2 + √((p/2)² - q) = {minus_p_halbe} + {wurzel_diskriminante} = {loesung_eins}\n")
    output.append(f"x₂ = -p/2 - √((p/2)² - q) = {minus_p_halbe} - {wurzel_diskriminante} = {loesung_zwei}\n")
    return "".join(output), loesung_eins, loesung_zwei

def berechne_note(punkte):
    if punkte >= 9:
        return "1 (Sehr gut)"
    elif punkte >= 7:
        return "2 (Gut)"
    elif punkte >= 5:
        return "3 (Befriedigend)"
    elif punkte >= 3:
        return "4 (Ausreichend)"
    elif punkte >= 1:
        return "5 (Mangelhaft)"
    else:
        return "6 (Ungenügend)"

def format_zeit(sekunden):
    minuten = int(sekunden // 60)
    sekunden = int(sekunden % 60)
    return f"{minuten:02d}:{sekunden:02d} Minuten"

class QuadraticEquationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadratische Gleichungen")
        self.gleichungen = []
        self.current_equation = None
        self.p = None
        self.q = None
        self.correct_solutions = None
        self.correct_count = 0
        self.task_count = 0
        self.max_tasks = 10
        self.start_zeit = time.time()  # Timer starten

        # Lade Gleichungen aus der Datei
        try:
            with open('output_1.txt', 'r', encoding="utf-8") as file:
                self.gleichungen = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.gleichungen = ["x²+2x+1=0"]  # Fallback-Gleichung

        # GUI-Elemente
        self.label = tk.Label(root, text="Gib die Lösungen ein!", font=("Arial", 18))
        self.label.pack(pady=12)

        self.text_area = scrolledtext.ScrolledText(root, width=50, height=15, font=("Arial", 16))
        self.text_area.pack(pady=12)
        self.text_area.config(state='disabled')

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=12)

        tk.Label(self.input_frame, text="x₁ =", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        self.entry_x1 = tk.Entry(self.input_frame, width=10, font=("Arial", 14))
        self.entry_x1.grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="x₂ =", font=("Arial", 14)).grid(row=0, column=2, padx=5)
        self.entry_x2 = tk.Entry(self.input_frame, width=10, font=("Arial", 14))
        self.entry_x2.grid(row=0, column=3, padx=5)

        self.submit_button = tk.Button(root, text="Lösung prüfen", command=self.check_solution)
        self.submit_button.pack(pady=12)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=12)

        self.next_button = tk.Button(root, text="Nächste Aufgabe", command=self.next_equation, state='disabled')
        self.next_button.pack(pady=12)

        self.new_equation()

    def new_equation(self):
        if self.task_count >= self.max_tasks:
            self.show_evaluation()
            return

        self.task_count += 1
        self.current_equation = random.choice(self.gleichungen)
        try:
            self.p, self.q = parse_pq(self.current_equation)
            _, sol1, sol2 = loesung_mit_weg_berechnen(self.p, self.q)
            self.correct_solutions = {float(sol1), float(sol2)}
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Aufgabe {self.task_count}/{self.max_tasks}:\n{self.current_equation}\n")
            self.text_area.config(state='disabled')
            self.label.config(text=f"Gib die Lösungen für Aufgabe {self.task_count} ein!")
            self.result_label.config(text="")
            self.entry_x1.delete(0, tk.END)
            self.entry_x2.delete(0, tk.END)
            self.submit_button.config(state='normal')
            self.next_button.config(state='disabled')
        except ValueError as e:
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Fehler: {e}\n")
            self.text_area.config(state='disabled')

    def check_solution(self):
        try:
            x1 = float(self.entry_x1.get())
            x2 = float(self.entry_x2.get())
            user_solutions = {x1, x2}
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Aufgabe {self.task_count}/{self.max_tasks}:\n{self.current_equation}\n")
            if user_solutions == self.correct_solutions:
                self.correct_count += 1
                self.result_label.config(text="Richtig!", fg="green")
                self.text_area.insert(tk.END, "\nDeine Lösung ist korrekt!\n")
            else:
                self.result_label.config(text=f"Falsch! Korrekte Lösungen: {self.correct_solutions}", fg="red")
                self.text_area.insert(tk.END, f"\nDeine Lösung ist falsch. Hier ist der Lösungsweg:\n\n")
                lösungsweg, _, _ = loesung_mit_weg_berechnen(self.p, self.q)
                self.text_area.insert(tk.END, lösungsweg)
            self.text_area.config(state='disabled')
            self.submit_button.config(state='disabled')
            self.next_button.config(state='normal')
        except ValueError:
            self.result_label.config(text="Bitte gültige Zahlen eingeben!", fg="red")

    def next_equation(self):
        self.new_equation()

    def show_evaluation(self):
        end_zeit = time.time()
        gesamt_zeit = end_zeit - self.start_zeit
        note = berechne_note(self.correct_count)
        messagebox.showinfo(
            "Auswertung",
            f"Du hast {self.correct_count} von {self.max_tasks} Aufgaben richtig gelöst.\n"
            f"Deine Note: {note}\n"
            f"Benötigte Zeit: {format_zeit(gesamt_zeit)}"
        )
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticEquationGUI(root)
    root.mainloop()