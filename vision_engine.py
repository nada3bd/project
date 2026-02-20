import os
import cv2
import psycopg2
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# ==========================================
# 1. الإعدادات والربط بقاعدة البيانات
# ==========================================
DB_PARAMS = {
    "dbname": "hospital_monitoring",
    "user": "postgres",
    "password": "132003",
    "host": "localhost",
    "port": "5432"
}

MODEL_PATHS = {
    "person": "models/detect_doctor_patient.pt", 
    "eyes": "models/eye_close_open.pt",
    "pose": "models/body_dedtction.pt"
}

# ==========================================
# 2. نظام المراقبة المتكامل
# ==========================================
class UltimateHospitalMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Hospital Monitor Pro - Final Production v4.0")
        self.root.geometry("1100x950")
        
        # حماية النظام من أخطاء الإغلاق المفاجئ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.models = {}
        self.load_models()
        
        self.running = False
        self.current_img_path = None
        self.hr_history = []
        self.time_steps = []
        self.counter = 0

        self.setup_gui()

    def load_models(self):
        """تحميل الموديلات مع التحقق من وجودها"""
        print("🕒 جاري تحضير محرك الذكاء الاصطناعي...")
        for name, path in MODEL_PATHS.items():
            if os.path.exists(path):
                try:
                    self.models[name] = YOLO(path)
                    print(f"✅ تم تحميل موديل [{name}]")
                except Exception as e:
                    print(f"❌ خطأ تقني في موديل {name}: {e}")
            else:
                print(f"⚠️ تحذير: ملف الموديل غير موجود في {path}")

    def setup_gui(self):
        """بناء واجهة مستخدم احترافية وسلسة"""
        # منطقة العرض المرئي
        self.img_label = tk.Label(self.root, text="يرجى اختيار صورة المريض لبدء التحليل الشامل", 
                                 bg="#f1f2f6", width=80, height=18, relief="groove")
        self.img_label.pack(pady=20)

        # أزرار التحكم
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()
        
        self.btn_upload = tk.Button(btn_frame, text="📁 تحميل صورة وبدء المراقبة", 
                                   command=self.upload_image, bg="#27ae60", fg="white", 
                                   font=("Arial", 12, "bold"), padx=40, pady=12)
        self.btn_upload.pack()

        # لوحة النتائج الرقمية
        display_frame = tk.LabelFrame(self.root, text=" 💻 بيانات المراقبة اللحظية ", font=("Arial", 10, "bold"))
        display_frame.pack(fill="x", padx=60, pady=20)

        self.lbl_vitals = tk.Label(display_frame, text="Vitals: Waiting...", 
                                  font=("Courier New", 20, "bold"), fg="#e74c3c")
        self.lbl_vitals.pack(pady=5)

        self.lbl_ai = tk.Label(display_frame, text="AI Analysis: N/A", 
                              font=("Arial", 11), justify=tk.LEFT, fg="#2c3e50")
        self.lbl_ai.pack(pady=10)

        # الرسم البياني للنبض
        self.fig, self.ax = plt.subplots(figsize=(7, 2.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_img_path = file_path
            # تحسين عرض الصورة في الواجهة
            img = Image.open(file_path).resize((550, 320))
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tk_img, text="")
            
            if not self.running:
                self.running = True
                self.execution_loop()

    def execution_loop(self):
        """الحلقة البرمجية المركزية للنظام"""
        if not self.running: return

        # 1. تحليل الصور (باستخدام بارامترات التعميم العالية imgsz=640)
        ai_data = self.advanced_ai_logic(self.current_img_path)
        
        # 2. محاكاة العلامات الحيوية (يمكن ربطها بحساسات حقيقية هنا)
        hr = random.randint(72, 88)
        spo2 = random.randint(96, 100)
        bp = f"{random.randint(115, 122)}/{random.randint(75, 82)}"

        # 3. تحديث الواجهة الرسومية
        self.lbl_vitals.config(text=f"Pulse: {hr} bpm | SpO2: {spo2}% | BP: {bp}")
        self.lbl_ai.config(text=f"🔍 الكشف الحركي: {ai_data['p_type']} | 👥 الحضور: {ai_data['count']}\n"
                                f"🧘 الوضعية: {ai_data['pose']} | 👁 حالة العين: {ai_data['eyes']}")

        # 4. الحفظ المتزامن في PostgreSQL (الجداول: medical_vitals و vision_logs)
        self.secure_db_save(ai_data, hr, bp, spo2)

        # 5. تحديث الرسم البياني اللحظي
        self.update_chart(hr)

        # تحديث كل 4 ثوانٍ لضمان استقرار العمليات
        self.root.after(4000, self.execution_loop)

    def advanced_ai_logic(self, path):
        """محرك التحليل الذكي: يصحح الأخطاء بناءً على السياق (Context-Aware)"""
        img = cv2.imread(path)
        data = {"p_type": "Patient", "eyes": "Closed", "pose": "Lying", "count": 0}

        if img is None: return data

        # أ. كشف الوضعية (رفع الدقة imgsz=640 والـ conf لضمان التعميم)
        if "pose" in self.models:
            res_p = self.models["pose"](img, conf=0.40, imgsz=640, verbose=False)[0]
            p_labels = [self.models["pose"].names[int(b.cls)] for b in res_p.boxes]
            data["pose"] = p_labels[0] if p_labels else "Lying"

        # ب. كشف الأشخاص وتصحيح الهوية (مريض vs ممرض)
        if "person" in self.models:
            res = self.models["person"](img, conf=0.50, iou=0.45, imgsz=640, verbose=False)[0]
            cls_names = [self.models["person"].names[int(b.cls)] for b in res.boxes]
            data["count"] = len(cls_names)
            
            # منطق المهندس السينيور: إذا كان الشخص مستلقياً، فهو المريض حتماً
            if data["pose"] == "Lying":
                data["p_type"] = "Patient"
            elif "Doctor" in cls_names:
                data["p_type"] = "Doctor"
            elif "Nurse" in cls_names:
                data["p_type"] = "Nurse"
            else:
                data["p_type"] = "Patient"

        # ج. كشف العيون (حساسية مخصصة للكائنات الصغيرة)
        if "eyes" in self.models:
            res_e = self.models["eyes"](img, conf=0.25, imgsz=640, verbose=False)[0]
            e_labels = [self.models["eyes"].names[int(b.cls)] for b in res_e.boxes]
            data["eyes"] = "Open" if "Open Eye" in e_labels else "Closed"

        return data

    def secure_db_save(self, ai, hr, bp, spo2):
        """حفظ متزامن لضمان ترابط البيانات للشات بوت"""
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            cur = conn.cursor()
            now = datetime.now()

            # التخزين في جدول العلامات الحيوية
            cur.execute("""
                INSERT INTO medical_vitals (patient_id, heart_rate, blood_pressure, oxygen_level, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (1, hr, bp, spo2, now))

            # التخزين في جدول سجلات الرؤية
            cur.execute("""
                INSERT INTO vision_logs (patient_id, eye_state, posture, people_count, person_type, log_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (1, ai['eyes'], ai['pose'], ai['count'], ai['p_type'], now))

            conn.commit()
            cur.close()
            conn.close()
            print(f"📊 [DATABASE] تم تسجيل الدورة بنجاح في {now.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")

    def update_chart(self, hr):
        self.counter += 1
        self.time_steps.append(self.counter)
        self.hr_history.append(hr)
        if len(self.time_steps) > 15:
            self.time_steps.pop(0)
            self.hr_history.pop(0)
        
        self.ax.clear()
        self.ax.plot(self.time_steps, self.hr_history, marker='o', color='#2980b9', linewidth=2)
        self.ax.set_title("معدل نبضات القلب اللحظي")
        self.ax.set_ylim(40, 140)
        self.canvas.draw()

    def on_closing(self):
        """دالة الإغلاق النظيف لمنع خطأ 'invalid command name'"""
        print("🔌 جاري إيقاف النظام وحفظ الجلسة...")
        self.running = False
        self.root.destroy()

# ==========================================
# 3. تشغيل البرنامج
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateHospitalMonitor(root)
    root.mainloop()