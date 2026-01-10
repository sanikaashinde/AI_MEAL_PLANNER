# gui.py
import tkinter as tk
from tkinter import messagebox
from data import food_items_breakfast, food_items_lunch, food_items_dinner
import random

# -------------------------------
# Helper Functions
# -------------------------------

def flatten_food_dict(food_dict):
    """Convert nested category dictionary into a list of (name, calories) tuples"""
    flat_list = []
    for category in food_dict:
        for food_name, cal in food_dict[category].items():
            flat_list.append((food_name, cal))
    return flat_list

def knapsack(foods, calorie_limit):
    """Select optimal combination of foods using 0-1 knapsack"""
    n = len(foods)
    dp = [[0]*(calorie_limit+1) for _ in range(n+1)]

    for i in range(1, n+1):
        name, cal = foods[i-1]
        for w in range(calorie_limit+1):
            if cal <= w:
                dp[i][w] = max(cal + dp[i-1][w-cal], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    # Backtrack to get selected foods
    selected = []
    w = calorie_limit
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(foods[i-1])
            w -= foods[i-1][1]
    return selected

def generate_ai_meal_name(foods):
    adjectives = ["Healthy", "Power", "Energy", "Balanced", "Nutri"]
    return f"{random.choice(adjectives)} {' & '.join([f[0] for f in foods])}"

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return 10*weight + 6.25*height - 5*age + 5
    else:
        return 10*weight + 6.25*height - 5*age - 161

# -------------------------------
# GUI Setup
# -------------------------------

root = tk.Tk()
root.title("AI Meal Planner")
root.geometry("550x600")

# Input Fields
tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Gender (Male/Female)").pack()
gender_entry = tk.Entry(root)
gender_entry.pack()

tk.Label(root, text="Height (cm)").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Goal (weight loss / maintenance / weight gain)").pack()
goal_entry = tk.Entry(root)
goal_entry.pack()

# Output Text Box
output_text = tk.Text(root, height=20, width=65)
output_text.pack(pady=10)

# -------------------------------
# Generate Meal Plan
# -------------------------------

def generate_meal_plan():
    try:
        age = int(age_entry.get())
        gender = gender_entry.get()
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        goal = goal_entry.get().lower()
    except:
        messagebox.showerror("Error", "Please enter valid inputs")
        return

    # BMR and daily calories
    bmr = calculate_bmr(weight, height, age, gender)
    if goal == "weight loss":
        daily_cal = int(bmr - 300)
    elif goal == "weight gain":
        daily_cal = int(bmr + 300)
    else:
        daily_cal = int(bmr)

    # Split calories by meal
    breakfast_cal = int(daily_cal * 0.50)
    lunch_cal = int(daily_cal * 0.33)
    dinner_cal = int(daily_cal * 0.17)

    # Flatten food dictionaries
    breakfast_foods = flatten_food_dict(food_items_breakfast)
    lunch_foods = flatten_food_dict(food_items_lunch)
    dinner_foods = flatten_food_dict(food_items_dinner)

    # Generate meals using Knapsack
    breakfast = knapsack(breakfast_foods, breakfast_cal)
    lunch = knapsack(lunch_foods, lunch_cal)
    dinner = knapsack(dinner_foods, dinner_cal)

    # Display in output
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Total Daily Calories: {daily_cal} kcal\n\n")

    output_text.insert(tk.END, "=== BREAKFAST ===\n")
    output_text.insert(tk.END, f"Meal Name: {generate_ai_meal_name(breakfast)}\n")
    output_text.insert(tk.END, f"Items: {breakfast}\n")
    output_text.insert(tk.END, f"Calories: {sum(f[1] for f in breakfast)}\n\n")

    output_text.insert(tk.END, "=== LUNCH ===\n")
    output_text.insert(tk.END, f"Meal Name: {generate_ai_meal_name(lunch)}\n")
    output_text.insert(tk.END, f"Items: {lunch}\n")
    output_text.insert(tk.END, f"Calories: {sum(f[1] for f in lunch)}\n\n")

    output_text.insert(tk.END, "=== DINNER ===\n")
    output_text.insert(tk.END, f"Meal Name: {generate_ai_meal_name(dinner)}\n")
    output_text.insert(tk.END, f"Items: {dinner}\n")
    output_text.insert(tk.END, f"Calories: {sum(f[1] for f in dinner)}\n\n")

    output_text.insert(tk.END, "✅ AI Meal Plan Generated Successfully")

# Generate Button
generate_btn = tk.Button(root, text="Generate Meal Plan", command=generate_meal_plan)
generate_btn.pack(pady=10)

root.mainloop()
