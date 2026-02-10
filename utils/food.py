from ultralytics import YOLO
from PIL import Image
from collections import Counter

model = YOLO("models_ml/food_detection_model.pt")

def predict_food(image):
    img = Image.open(image)
    results = model(img)[0]

    class_ids = results.boxes.cls.int().tolist()
    class_names = results.names
    counts = Counter(class_ids)

    # Class ID + 1 untuk menyamakan dengan id database makanan
    summary = [
        {"class_id": class_id + 1, "food_name": class_names[class_id], "count": count}
        for class_id, count in counts.items()
    ]

    return summary
