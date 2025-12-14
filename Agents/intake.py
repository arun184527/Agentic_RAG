def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def calculate_bmr(weight_kg, height_cm, age, gender):
    if gender.lower() == "male":
        return round(10 * weight_kg + 6.25 * height_cm - 5 * age + 5, 2)
    else:
        return round(10 * weight_kg + 6.25 * height_cm - 5 * age - 161, 2)


def calculate_tdee(bmr, activity_level):
    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725
    }
    return round(bmr * activity_factors.get(activity_level, 1.2), 2)


def intake_agent(user_input):
    """
    Input: raw user data
    Output: structured health profile for other agents
    """

    name = user_input["name"]
    age = user_input["age"]
    gender = user_input["gender"]
    height_cm = user_input["height_cm"]
    weight_kg = user_input["weight_kg"]
    activity_level = user_input.get("activity_level", "sedentary")
    goal = user_input.get("goal", "weight_loss")  # weight_loss / weight_gain
    allergies = user_input.get("allergies", [])
    preference = user_input.get("preference", "mixed")

    bmi = calculate_bmi(weight_kg, height_cm)
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    # calorie logic
    if goal == "weight_loss":
        target_calories = tdee - 500
    else:
        target_calories = tdee + 300

    # safety minimums
    if gender.lower() == "male" and target_calories < 1500:
        target_calories = 1500
    if gender.lower() == "female" and target_calories < 1200:
        target_calories = 1200

    # risk flags
    risk_flags = []
    if age >= 60:
        risk_flags.append("elderly")
    if weight_kg >= 120:
        risk_flags.append("high_weight")
    if weight_kg <= 40:
        risk_flags.append("underweight")

    return {
        "user_profile": {
            "name": name,
            "age": age,
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "activity_level": activity_level,
            "goal": goal,
            "preference": preference,
            "allergies": allergies
        },
        "calculations": {
            "BMI": bmi,
            "BMR": bmr,
            "TDEE": tdee,
            "target_calories": int(target_calories)
        },
        "risk_flags": risk_flags
    }
if __name__ == "__main__":
    print("=== Nutrition Intake Agent ===")

    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ")
    height_cm = float(input("Enter your height (cm): "))
    weight_kg = float(input("Enter your weight (kg): "))
    activity_level = input(
        "Enter activity level (sedentary / lightly_active / moderately_active / very_active): "
    )
    goal = input("Enter goal (weight_loss / weight_gain): ")
    preference = input("Enter diet preference (vegetarian / nonvegetarian / mixed): ")

    allergies_input = input("Enter allergies (comma separated, or none): ")
    if allergies_input.lower() == "none":
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

    result = intake_agent(user_input)

    print("\n=== Agent-1 Output ===")
    print(result)