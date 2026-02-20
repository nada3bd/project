import requests
import time
import random

BASE_URL = "http://127.0.0.1:8000"

def simulate():
    p_id = 1 
    
    while True:
        # بيانات الكاميرا
        vision = {
            "patient_id": p_id,
            "eye_state": random.choice(["Open", "Closed"]),
            "posture": random.choice(["Standing", "Lying", "Falling", "Sitting"]),
            "people_count": random.randint(0, 3),
            "person_type": random.choice(["Doctor", "Nurse", "Visitor"])
        }
        requests.post(f"{BASE_URL}/ingest/vision", json=vision)

        # بيانات الأجهزة
        vitals = {
            "patient_id": p_id,
            "heart_rate": random.randint(60, 100),
            "blood_pressure": "120/80",
            "oxygen_level": random.randint(95, 99)
        }
        requests.post(f"{BASE_URL}/ingest/vitals", json=vitals)
        
        time.sleep(5)

if __name__ == "__main__":
    simulate()