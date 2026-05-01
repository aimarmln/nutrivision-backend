from langgraph.checkpoint.postgres import PostgresSaver  
from app.config import Config

checkpointer_cm = PostgresSaver.from_conn_string(Config.CHECKPOINT_DB_URL)
checkpointer = checkpointer_cm.__enter__()
checkpointer.setup()