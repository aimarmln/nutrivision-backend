from ultralytics import YOLO
from ultralytics.engine.results import Results
from collections import Counter
from werkzeug.datastructures import FileStorage
from PIL import Image

class YOLODetector:
    def __init__(self, model_path: str):
        self.model = self._load_model(model_path)

    def _load_model(self, model_path: str) -> YOLO:
        return YOLO(model_path)

    def detect(self, image: FileStorage) -> list[dict]:
        # Convert FileStorage to PIL Image
        img = Image.open(image.stream)

        # Run YOLO inference
        results: Results = self.model(img)[0]

        # If no boxes are detected, return an empty list
        if not results.boxes:
            return []
        
        # Extract class IDs and count occurrences
        class_ids = results.boxes.cls.int().tolist()
        class_names = results.names
        counts = Counter(class_ids)

        results = [
            {
                "label": class_names[class_id],
                "count": count
            }
            for class_id, count in counts.items()
        ]

        return results
