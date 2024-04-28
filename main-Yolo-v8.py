# https://pysource.com/2023/03/28/object-detection-with-yolo-v8-on-mac-m1/
import cv2
from ultralytics import YOLO
import numpy as np
import torch
import time
import json

print(torch.backends.mps.is_available())

# read the classes file and convert an array
text_file = open("classes.txt", "r")
lines = text_file.readlines()
print (lines)
print (len(lines))
text_file.close()


# Path to your JSON file
file_path = 'FoodData_Central_survey_food_json_2022-10-28.json'

# Open the JSON file and load its content
with open(file_path, 'r') as file:
    data = json.load(file)

# Assuming the JSON data is loaded into 'data'
def my_function(search_term):
    search_term = str(search_term)
    print("*****", search_term)
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
    #time.sleep(1)

cap = cv2.VideoCapture("video-109_singular_display.mp4")
model = YOLO("best-3.pt")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, device="mps",conf=0.50)
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    try:
      data = np.array(lines[classes[0]])
      if (data.size > 0):
        print(lines[classes[0]])
        temp = lines[classes[0]]
        print(""+temp+"")
        my_function(temp[:-1])
    except IndexError:
      print("Attempted to access an index that doesn't exist")
    for cls, bbox in zip(classes, bboxes):
        (x, y, x2, y2) = bbox
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
        cv2.putText(frame, lines[cls], (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)
    cv2.imshow("Img", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()






