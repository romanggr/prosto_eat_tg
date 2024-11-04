def calculate_calories(user):
    gender = user['gender']
    age = user['age']
    height = user['height']
    weight = user['weight']
    activity_level = user['activity_level']
    target = user['target']

    # BMR calculation
    if gender == 'MEN':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'WOMEN':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Invalid gender format. Use 'MEN' or 'WOMEN'.")

    # Activity multiplier
    activity_multipliers = {
        "LOW": 1.2,
        "AVERAGE": 1.375,
        "HIGH": 1.55,
    }
    activity_multiplier = activity_multipliers.get(activity_level.upper(), 1.2)

    # Calculate daily caloric needs based on activity level
    daily_calories = bmr * activity_multiplier

    # Adjust daily calories based on target
    if target == "GAIN":
        daily_calories *= 1.15  # Increase by 15%
    elif target == "LOSE":
        daily_calories *= 0.85  # Decrease by 15%
    # If target is "MAINTAIN" or unrecognized, keep calories as is

    return daily_calories

