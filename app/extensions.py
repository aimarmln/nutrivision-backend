import redis
from flask_jwt_extended import JWTManager
from app.config import Config
from app.ml.sentiment_analyzer import SentimentAnalyzer
from app.ml.yolo_detector import YOLODetector
from sentence_transformers import SentenceTransformer

# Initialize Flask JWT Manager
jwt = JWTManager()

# Initialize YOLO Detector for food detection
yolo_detector = YOLODetector(model_path="app/ml/models/food_detection_model.pt")

# Initialize Sentiment Analyzer for comment sentiment analysis
sentiment_analyzer = SentimentAnalyzer(
    model_path="app/ml/models/sentiment_analysis_model.h5",
    tokenizer_path="app/ml/tokenizers/sentiment_tokenizer.pkl",
)

# Initialize Redis client for session management
redis_client = redis.Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)

# Initialize embedding
# BAAI/bge-m3
# intfloat/multilingual-e5-base
# intfloat/multilingual-e5-small
# sentence-transformers/paraphrase-multilingual-mpnet-base-v2
# sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

embeddings = SentenceTransformer("intfloat/multilingual-e5-base", device="mps")
