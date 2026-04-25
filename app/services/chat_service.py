from app.repositories.food_repository import FoodRepository
from langchain.messages import HumanMessage
from app.repositories.serving_repository import ServingRepository
from app.agent.agent import agent, Context

class ChatService:

    @staticmethod
    def chat_ai(user_id: str, message: str) -> str:
        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=message)
                ]
            },
            {
                "configurable": { 
                    "thread_id": user_id
                }
            },
            context=Context(user_id=user_id)
        )

        return result["messages"][-1].content
    
    @staticmethod
    def get_foods_by_name(name: str) -> list[dict]:
        # Ambil tuple (Food, distance) dari repository
        raw_results = FoodRepository.get_foods_by_name(name)

        results = []
        for f, dist in raw_results:
            # dist adalah nilai float (0.0 - 1.0)
            # Semakin kecil 'dist', semakin mirip makanannya
            similarity_score = round((1 - dist) * 100, 2) # Ubah ke % kemiripan jika mau

            results.append({
                "id": str(f.id),
                "name": f.name,
                "category": f.category,
                "distance": round(dist, 4),      # Nilai asli jarak (0 = identik)
                "score_percentage": f"{similarity_score}%", 
                "servings": [
                    {
                        "unit": s.serving_unit,
                        "calories": s.calories_kcal,
                        "is_default": s.is_default
                    } for s in f.servings
                ]
            })

        return results
    
    @staticmethod
    def get_food_servings(food_id: str, serving: str) -> list[dict]:
        raw_results = ServingRepository.get_food_servings(food_id, serving)

        results = []
        for s, dist in raw_results:
            similarity_score = round((1 - dist) * 100, 2) # Ubah ke % kemiripan jika mau

            results.append({
                "id": str(s.id),
                "food_name": s.food.name,
                "serving_unit": s.serving_unit,
                "calories_kcal": s.calories_kcal,
                "protein_g": s.protein_g,
                "distance": round(dist, 4),
                "score_percentage": f"{similarity_score}%"
            })

        return results
