from app.database import db_session

def shutdown_session(exception=None):
    if exception:
        db_session.rollback()
    db_session.remove()

def db_commit():
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
