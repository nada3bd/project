import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# الحدود الطبيعية 
RANGES = {
    "HR": (60, 100),
    "SpO2": (95, 100),
    "BP_SYS": (90, 120),
    "BP_DIA": (60, 80)
}

# توليد 80% طبيعي / 20% غير طبيعي 
def generate_value(name):
    normal_min, normal_max = RANGES[name]

    if random.random() < 0.8:
        return random.randint(normal_min, normal_max), True
    else:
        
        if random.random() < 0.5:
            return random.randint(normal_min - 40, normal_min - 1), False
        else:
            return random.randint(normal_max + 1, normal_max + 40), False

#  GUI
class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vital Monitor Simulator")

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        self.data_label = tk.Label(root, text="", font=("Arial", 14))
        self.data_label.pack()

        self.alert_label = tk.Label(root, text="", font=("Arial", 16, "bold"))
        self.alert_label.pack()

       
        self.time_data = []
        self.hr_data = []
        self.spo2_data = []
        self.sys_data = []
        self.dia_data = []
        self.counter = 0

        #  HR Plot 
        self.fig_hr, self.ax_hr = plt.subplots(figsize=(5,2))
        self.canvas_hr = FigureCanvasTkAgg(self.fig_hr, master=root)
        self.canvas_hr.get_tk_widget().pack()

        #  SpO2 Plot
        self.fig_spo2, self.ax_spo2 = plt.subplots(figsize=(5,2))
        self.canvas_spo2 = FigureCanvasTkAgg(self.fig_spo2, master=root)
        self.canvas_spo2.get_tk_widget().pack()

        # BP Plot 
        self.fig_bp, self.ax_bp = plt.subplots(figsize=(5,2))
        self.canvas_bp = FigureCanvasTkAgg(self.fig_bp, master=root)
        self.canvas_bp.get_tk_widget().pack()

        self.running = False

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path)
            img = img.resize((400, 300))
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img)

            if not self.running:
                self.running = True
                self.update_values()

    def update_values(self):
        hr, hr_ok = generate_value("HR")
        spo2, spo2_ok = generate_value("SpO2")
        sys, sys_ok = generate_value("BP_SYS")
        dia, dia_ok = generate_value("BP_DIA")

        self.data_label.config(
            text=f"HR: {hr} bpm | SpO2: {spo2}% | BP: {sys}/{dia}"
        )

        if not (hr_ok and spo2_ok and sys_ok and dia_ok):
            self.alert_label.config(text="⚠ WARNING: Abnormal Reading!", fg="red")
        else:
            self.alert_label.config(text="Normal", fg="green")

      
        self.counter += 1
        self.time_data.append(self.counter)
        self.hr_data.append(hr)
        self.spo2_data.append(spo2)
        self.sys_data.append(sys)
        self.dia_data.append(dia)

      
        if len(self.time_data) > 20:
            self.time_data.pop(0)
            self.hr_data.pop(0)
            self.spo2_data.pop(0)
            self.sys_data.pop(0)
            self.dia_data.pop(0)

        #  HR 
        self.ax_hr.clear()
        self.ax_hr.plot(self.time_data, self.hr_data)
        self.ax_hr.set_title("Heart Rate (HR)")
        self.ax_hr.set_ylabel("bpm")
        self.canvas_hr.draw()

        # SpO2
        self.ax_spo2.clear()
        self.ax_spo2.plot(self.time_data, self.spo2_data)
        self.ax_spo2.set_title("SpO2")
        self.ax_spo2.set_ylabel("%")
        self.canvas_spo2.draw()

        #  BP 
        self.ax_bp.clear()
        self.ax_bp.plot(self.time_data, self.sys_data, label="SYS")
        self.ax_bp.plot(self.time_data, self.dia_data, label="DIA")
        self.ax_bp.set_title("Blood Pressure")
        self.ax_bp.legend()
        self.canvas_bp.draw()

        self.root.after(1000, self.update_values)

root = tk.Tk()
app = MonitorApp(root)
root.mainloop()
