def safety_agent(intake_output, planner_output):
    """
    Agent-5: Safety & Validation Agent
    Enforces calorie safety, risk warnings, and allergy checks.
    """

    user = intake_output["user_profile"]
    calc = intake_output["calculations"]
    risks = intake_output.get("risk_flags", [])
    allergies = [a.lower() for a in user.get("allergies", [])]

    warnings = []

    # 1. Calorie safety checks
    target_cal = calc["target_calories"]

    if user["gender"] == "male" and target_cal < 1500:
        warnings.append("Calorie target is too low for a male user (minimum 1500 kcal/day).")

    if user["gender"] == "female" and target_cal < 1200:
        warnings.append("Calorie target is too low for a female user (minimum 1200 kcal/day).")

    # 2. Risk-based warnings
    if "elderly" in risks:
        warnings.append("User is elderly. Extreme calorie deficits should be avoided.")

    if "underweight" in risks:
        warnings.append("User is underweight. Weight loss is not recommended.")

    if "high_weight" in risks:
        warnings.append("User has high body weight. Gradual weight loss is recommended.")

    # 3. Allergy enforcement (NEW)
    allergy_hits = []
    for allergy in allergies:
        if allergy in planner_output.lower():
            allergy_hits.append(allergy)

    if allergy_hits:
        warnings.append(
            f"Meal plan contains foods related to declared allergies: {', '.join(allergy_hits)}. "
            "These items should be removed or replaced."
        )

    # 4. Safety disclaimer
    safety_note = (
        "\n\n⚠️ Safety Note:\n"
        "This diet plan is for general wellness only and is not a medical prescription. "
        "Please consult a healthcare professional for medical conditions."
    )

    # 5. Build final output
    final_output = planner_output

    if warnings:
        final_output += "\n\n⚠️ Safety Warnings:\n"
        for w in warnings:
            final_output += f"- {w}\n"

    final_output += safety_note

    return final_output
