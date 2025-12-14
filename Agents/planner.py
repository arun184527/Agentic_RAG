from langchain_groq import ChatGroq


def planner_agent(intake_output, retrieved_docs):
    """
    Agent-4: Planner Agent
    Generates a personalized diet plan using Groq LLM + RAG context
    """

    # 1. Combine retrieved KB content
    knowledge_context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    # 2. Extract user data
    user = intake_output["user_profile"]
    calc = intake_output["calculations"]

    # 3. Build prompt (grounded + constrained)
    prompt = f"""
You are a certified nutritionist AI.

USER PROFILE:
Name: {user['name']}
Age: {user['age']}
Gender: {user['gender']}
Height: {user['height_cm']} cm
Weight: {user['weight_kg']} kg
Goal: {user['goal']}
Diet Preference: {user['preference']}
Allergies: {user['allergies']}
Target Calories: {calc['target_calories']} kcal/day

RETRIEVED NUTRITION KNOWLEDGE:
{knowledge_context}

TASK:
- Create a 1-day personalized meal plan
- Include: Breakfast, Lunch, Snack, Dinner
- Respect diet preference and allergies strictly
- Stay close to the target calorie value
- Use common, practical foods
- Avoid medical claims or extreme dieting advice
- Keep explanations simple and clear

OUTPUT FORMAT:
Breakfast:
Lunch:
Snack:
Dinner:
Tips:
"""

    # 4. Initialize Groq LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

    # 5. Invoke model
    response = llm.invoke(prompt)

    return response.content


# ---------------- TEST RUN ----------------
if __name__ == "__main__":
    sample_intake = {
        "user_profile": {
            "name": "Arun",
            "age": 30,
            "gender": "male",
            "height_cm": 175,
            "weight_kg": 85,
            "goal": "weight_loss",
            "preference": "vegetarian",
            "allergies": ["peanut"]
        },
        "calculations": {
            "target_calories": 1800
        }
    }

    sample_docs = [
        type("Doc", (), {
            "page_content": "Vegetarian protein sources include lentils, tofu, paneer, and legumes."
        }),
        type("Doc", (), {
            "page_content": "A daily calorie deficit of around 500 kcal is considered safe for weight loss."
        })
    ]

    print("\n===== GENERATED DIET PLAN =====\n")
    print(planner_agent(sample_intake, sample_docs))