from Agents.intake import intake_agent
from Agents.retriever import retrieve_knowledge
from Agents.planner import planner_agent
from Agents.safety import safety_agent


def run_pipeline(user_input):
    print("\n===== AGENTIC RAG PIPELINE STARTED =====\n")

    # 1. Intake Agent
    print("▶ Running Agent-1: Intake Agent")
    intake_output = intake_agent(user_input)

    # 2. Retriever Agent
    print("▶ Running Agent-3: Retriever Agent")
    retrieved_docs = retrieve_knowledge(intake_output)

    # 3. Planner Agent
    print("▶ Running Agent-4: Planner Agent")
    planner_output = planner_agent(intake_output, retrieved_docs)

    # 4. Safety Agent
    print("▶ Running Agent-5: Safety Agent")
    final_output = safety_agent(intake_output, planner_output)

    print("\n===== FINAL SAFE DIET PLAN =====\n")
    print(final_output)

    print("\n===== PIPELINE COMPLETED SUCCESSFULLY =====\n")

# ------------------ USER INPUT RUN ------------------
if __name__ == "__main__":

    print("\n=== Personalized Nutrition Planner ===\n")

    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ").strip().lower()
    height_cm = float(input("Enter your height (cm): "))
    weight_kg = float(input("Enter your weight (kg): "))

    activity_level = input(
        "Enter activity level (sedentary / lightly_active / moderately_active / very_active): "
    ).strip().lower()

    goal = input("Enter goal (weight_loss / weight_gain): ").strip().lower()
    preference = input("Diet preference (vegetarian / nonvegetarian / mixed): ").strip().lower()

    allergies_input = input("Enter allergies (comma separated or 'none'): ").strip().lower()
    if allergies_input == "none":
        allergies = []
    else:
        allergies = [a.strip() for a in allergies_input.split(",")]

    user_input = {
        "name": name,
        "age": age,
        "gender": gender,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "activity_level": activity_level,
        "goal": goal,
        "preference": preference,
        "allergies": allergies
    }

    run_pipeline(user_input)