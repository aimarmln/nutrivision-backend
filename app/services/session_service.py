# import uuid
# from datetime import datetime, timedelta, timezone
# from app.models.chat_session import ChatSession
# from app.extensions import redis_client
# from app.repositories.session_repository import SessionRepository

# SESSION_TTL_SECONDS = 1800  # 30 minutes

# class SessionService:

#     @staticmethod
#     def get_or_create_session(user_id: uuid.UUID, session_id: uuid.UUID | None) -> ChatSession:

#         # Check database for active session
#         if session_id:
#             session = SessionRepository.get_by_id(session_id)

#             if session and not SessionService._is_expired(session):
#                 SessionService.touch(session.id)
#                 return session

#         # Check redis for active session
#         redis_session_id = redis_client.get(f"session:{user_id}")

#         if redis_session_id:
#             session = SessionRepository.get_by_id(redis_session_id)

#             if session and not SessionService._is_expired(session):
#                 SessionService.touch(session.id)
#                 return session

#         # Create new session
#         new_session = SessionRepository.create(
#             id=uuid.uuid4(),
#             user_id=user_id,
#             created_at=datetime.now(timezone.utc),
#             last_activity_at=datetime.now(timezone.utc)
#         )

#         # Store in redis
#         redis_client.set(
#             f"session:{user_id}",
#             str(new_session.id),
#             ex=SESSION_TTL_SECONDS
#         )

#         return new_session

#     @staticmethod
#     def touch(session_id: str):
#         now = datetime.now(timezone.utc)

#         SessionRepository.update_last_activity(session_id, now)

#         session = SessionRepository.get_by_id(session_id)

#         # sync Redis TTL ulang
#         redis_client.setex(
#             f"session:{session.user_id}",
#             SESSION_TTL_SECONDS,
#             str(session_id)
#         )

#     @staticmethod
#     def _is_expired(session: ChatSession) -> bool:
#         return datetime.now(timezone.utc) - session.last_activity_at > timedelta(seconds=SESSION_TTL_SECONDS)