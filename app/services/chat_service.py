from datetime import datetime, timezone
from langchain.messages import HumanMessage
from werkzeug.exceptions import NotFound
from app.agent import agent, Context
from app.models import ChatSession, ChatMessage
from app.repositories import ChatRepository
from app.constants.chat import ChatMessageRole
from app.schemas.chat_schema import SessionsListQueryParams, ChatMessagesQueryParams
from app.utils.database import db_commit


class ChatService:

    @staticmethod
    def create_chat(user_id: int, message: str) -> str:
        chat_session = ChatSession(user_id=user_id)
        ChatRepository.save_chat_session(chat_session)

        return ChatService._process_message(user_id, chat_session, message)
    
    @staticmethod
    def send_message(user_id: int, session_id: int, message: str) -> str:
        chat_session = ChatRepository.find_session_by_id(session_id)

        if not chat_session or chat_session.user_id != user_id:
            raise NotFound("Chat session not found")
        
        return ChatService._process_message(user_id, chat_session, message)

    @staticmethod
    def list_sessions(user_id: int, params: SessionsListQueryParams) -> list[dict]:
        total_items = ChatRepository.count_sessions(
            user_id=user_id,
        )

        chat_sessions = ChatRepository.find_sessions_with_last_user_message(
            user_id=user_id, page=params.page, limit=params.limit
        )

        results = [
            {
                "session_id": s.session_id,
                "last_activity_at": s.last_activity_at.isoformat(),
                "last_user_message": s.last_user_message # Nullable
            }
            for s in chat_sessions
        ]

        # Build pagination info
        total_pages = (total_items + params.limit - 1) // params.limit
        pagination = {
            'current_page': params.page,
            'limit': params.limit,
            'total_items': total_items,
            'total_pages': total_pages, 
        }

        return results, pagination

    @staticmethod
    def get_messages(user_id: int, session_id: int, params: ChatMessagesQueryParams) -> list[dict]:
        session = ChatRepository.find_session_by_id(session_id)

        if not session or session.user_id != user_id:
            raise NotFound("Chat session not found")
        
        messages = ChatRepository.find_messages_by_session_id_paginated(
            session_id, params.cursor_created_at, params.cursor_id, params.limit
        )

        messages.reverse()

        results = [
            {
                "id": m.id,
                "role": m.role,
                "message": m.message,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]

        # Next cursor
        next_cursor = None
        if messages:
            last = messages[0]
            next_cursor = {
                "created_at": last.created_at.isoformat(),
                "id": last.id
            }

        has_more = len(messages) == params.limit

        return results, {
            "next_cursor": next_cursor,
            "has_more": has_more
        }
    
    @staticmethod
    def _process_message(user_id: int, chat_session: ChatSession, message: str):
        user_message = ChatMessage(
            session_id=chat_session.id,
            role=ChatMessageRole.USER,
            message=message,
            created_at=datetime.now(timezone.utc)
        )
        ChatRepository.save_chat_message(user_message)


        ai_message = ChatService._chat_ai(user_id, chat_session.id, message)

        last_activity_at = datetime.now(timezone.utc)

        assistant_message = ChatMessage(
            session_id=chat_session.id,
            role=ChatMessageRole.ASSISTANT,
            message=ai_message,
            created_at=last_activity_at
        )
        ChatRepository.save_chat_message(assistant_message)

        chat_session.last_activity_at = last_activity_at

        db_commit()

        return {
            "session_id": chat_session.id,
            "message": {
                "id": assistant_message.id,
                "content": assistant_message.message,
                "created_at": assistant_message.created_at.isoformat()
            }
        }
  
    @staticmethod
    def _chat_ai(user_id: int, session_id: int, message: str) -> str:
        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=message)
                ]
            },
            {
                "configurable": { 
                    "thread_id": f"session_{session_id}"
                }
            },
            context=Context(user_id=user_id)
        )

        return result["messages"][-1].content
        
    # @staticmethod
    # def get_foods_by_name(name: str) -> list[dict]:
    #     raw_results = FoodRepository.get_foods_by_name(name)

    #     results = []
    #     for f, dist in raw_results:
    #         similarity_score = round((1 - dist) * 100, 2) 

    #         results.append({
    #             "id": str(f.id),
    #             "name": f.name,
    #             "category": f.category,
    #             "distance": round(dist, 4),   
    #             "score_percentage": f"{similarity_score}%", 
    #             "servings": [
    #                 {
    #                     "unit": s.serving_unit,
    #                     "calories": s.calories_kcal,
    #                     "is_default": s.is_default
    #                 } for s in f.servings
    #             ]
    #         })

    #     return results
    
    # @staticmethod
    # def get_food_servings(food_id: str, serving: str) -> list[dict]:
    #     raw_results = ServingRepository.get_food_servings(food_id, serving)

    #     results = []
    #     for s, dist in raw_results:
    #         similarity_score = round((1 - dist) * 100, 2)

    #         results.append({
    #             "id": str(s.id),
    #             "food_name": s.food.name,
    #             "serving_unit": s.serving_unit,
    #             "calories_kcal": s.calories_kcal,
    #             "protein_g": s.protein_g,
    #             "distance": round(dist, 4),
    #             "score_percentage": f"{similarity_score}%"
    #         })

    #     return results
