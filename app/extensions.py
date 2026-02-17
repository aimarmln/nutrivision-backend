from flask_jwt_extended import JWTManager
from app.ml.sentiment_analyzer import SentimentAnalyzer
from app.ml.yolo_detector import YOLODetector

# Initialize Flask JWT Manager
jwt = JWTManager()

# Initialize YOLO Detector for food detection
yolo_detector = YOLODetector(
    model_path="app/ml/models/food_detection_model.pt"
)

# Initialize Sentiment Analyzer for comment sentiment analysis
sentiment_analyzer = SentimentAnalyzer(
    model_path="app/ml/models/sentiment_analysis_model.h5", 
    tokenizer_path="app/ml/tokenizers/sentiment_tokenizer.pkl"
)
