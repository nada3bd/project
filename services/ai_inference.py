from ultralytics import YOLO

doctor_patient_model = YOLO("models/detect_doctor_patient.pt")
eye_model = YOLO("models/eye_close_open.pt")
body_model = YOLO("models/body_dedtction.pt")


def run_inference(image_path: str):
    results = {}

    dp_results = doctor_patient_model(image_path)[0]
    eye_results = eye_model(image_path)[0]
    body_results = body_model(image_path)[0]

    results["doctor_patient"] = extract(dp_results)
    results["eyes"] = extract(eye_results)
    results["body"] = extract(body_results)

    return results


def extract(result):
    detections = []
    for box in result.boxes:
        detections.append({
            "class": result.names[int(box.cls)],
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist()
        })
    return detections


if __name__ == "__main__":
    image_path = "test_images/test2.jpeg"
    results = run_inference(image_path)
    print(results)
