from datetime import datetime
from sqlalchemy import func, and_, or_
from sqlalchemy.engine import Row
from app.constants.chat import ChatMessageRole
from app.database import db_session
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


class ChatRepository:

    @staticmethod
    def count_sessions(user_id: int) -> int:
        query = db_session.query(func.count(ChatSession.id)).filter(
            ChatSession.user_id == user_id,
            ChatSession.is_deleted == False
        )

        return query.scalar()

    @staticmethod
    def save_chat_session(chat_session: ChatSession):
        db_session.add(chat_session)
        db_session.flush()
        
    @staticmethod
    def save_chat_message(chat_message: ChatMessage):
        db_session.add(chat_message)
        db_session.flush()
        
    @staticmethod
    def find_session_by_id(session_id: int) -> ChatSession | None:
        query = db_session.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.is_deleted == False
        )

        return query.first()
    
    @staticmethod
    def find_messages_by_session_id_paginated(
        session_id: int,
        cursor_created_at: datetime | None = None,
        cursor_id: int | None = None,
        limit: int = 20
    ) -> list[ChatMessage]:
        
        query = db_session.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        )

        # cursor logic
        if cursor_created_at:
            if cursor_id:
                query = query.filter(
                    or_(
                        ChatMessage.created_at < cursor_created_at,
                        and_(
                            ChatMessage.created_at == cursor_created_at,
                            ChatMessage.id < cursor_id
                        )
                    )
                )
            else:
                query = query.filter(
                    ChatMessage.created_at < cursor_created_at
                )

        query = query.order_by(
            ChatMessage.created_at.desc()
        ).limit(limit)

        return query.all()
    
    @staticmethod
    def find_sessions_with_last_user_message(
        user_id: int,
        page: int = 1,
        limit: int = 20
    ) -> list[Row]:
        subquery = db_session.query(
            ChatMessage.session_id,
            func.max(ChatMessage.created_at).label("last_message_time")
        ).filter(
            ChatMessage.role == ChatMessageRole.USER
        ).group_by(ChatMessage.session_id).subquery()

        query = db_session.query(
                ChatSession.id.label("session_id"),
                ChatSession.last_activity_at,
                ChatMessage.message.label("last_user_message")
        ).outerjoin(
            subquery, 
            ChatSession.id == subquery.c.session_id
        ).outerjoin(
            ChatMessage,
            and_(
                ChatMessage.session_id == subquery.c.session_id,
                ChatMessage.created_at == subquery.c.last_message_time
            )
        ).filter(
                ChatSession.user_id == user_id,
                ChatSession.is_deleted == False,
                ChatMessage.role == ChatMessageRole.USER
        )

        offset_value = (page - 1) * limit

        query = query.order_by(
            ChatSession.last_activity_at.desc()
        ).offset(offset_value).limit(limit)

        return query.all()
