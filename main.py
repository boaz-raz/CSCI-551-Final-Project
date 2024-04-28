import json

# Path to your JSON file
file_path = 'FoodData_Central_survey_food_json_2022-10-28.json'

# Open the JSON file and load its content
with open(file_path, 'r') as file:
    data = json.load(file)


# Assuming the JSON data is loaded into 'data'
# search_term = "Ice cream"
search_term = "Pizza"
# search_term = "Chicken"
matching_items = []  # To store items matching the search term with their nutrients

# Process each food item
for item in data['SurveyFoods']:
    if search_term.lower() in item['description'].lower():
        # Initialize nutrient amounts for the current item
        nutrients = {'fat': None, 'sugar': None, 'carbohydrates': None}

        # Search for nutrients in the current item
        for nutrient_info in item['foodNutrients']:
            nutrient_name = nutrient_info['nutrient']['name'].lower()
            if 'fat' in nutrient_name:
                nutrients['fat'] = nutrient_info['amount']
            elif 'sugar' in nutrient_name:
                nutrients['sugar'] = nutrient_info['amount']
            elif 'carbohydrate' in nutrient_name:
                nutrients['carbohydrates'] = nutrient_info['amount']

        # Add item and its nutrients to the list if it has the relevant nutrient data
        if any(nutrients.values()):
            matching_items.append({'item': item, 'nutrients': nutrients})

# Sort and pick top 5 for each nutrient
top_5_fat = sorted(matching_items, key=lambda x: (x['nutrients']['fat'] is not None, x['nutrients']['fat']))[:5]
top_5_sugar = sorted(matching_items, key=lambda x: (x['nutrients']['sugar'] is not None, x['nutrients']['sugar']))[:5]
top_5_carbs = sorted(matching_items, key=lambda x: (x['nutrients']['carbohydrates'] is not None, x['nutrients']['carbohydrates']))[:5]

# Function to print top 5 items for a given nutrient
def print_top_5(items, nutrient_name):
    print(f"Top 5 items with lowest {nutrient_name}:")
    for entry in items:
        description = entry['item']['description']
        amount = entry['nutrients'][nutrient_name]
        print(f"- {description}: {amount} g")
    print("\n")

# Display the results
print_top_5(top_5_fat, 'fat')
print_top_5(top_5_sugar, 'sugar')
print_top_5(top_5_carbs, 'carbohydrates')
