import pandas as pd
from diet_genetic import genetic

ideal_bmi = 22
sedantary = 25
moderate = 30

def round_to_ceil_10(value):
	tens = value // 10
	return int((tens + 1) * 10)

def amount_to_string(amount):
	whole = str(int(amount))
	if(whole == "0"):
		whole = ""
	if(amount != int(amount)):
		whole += " 1/2"
	return whole


def get_recommendation(weight,height,diet_type):#weight in kg,height in m
	result = {}
	bmi = weight / (height * height)
	result["bmi"] = bmi

	ideal_weight = int(ideal_bmi * height * height)
	result["ideal_weight"] = ideal_weight

	calorie_req = moderate * ideal_weight
	result["calorie_req"] = calorie_req

	surplus_calories = 5 * ideal_weight
	result["surplus_calories"] = surplus_calories
	result["exercise"] = get_exercise(surplus_calories,weight)

	protein_req = ideal_weight
	result["protein_req"] = protein_req

	protein_calories = protein_req * 4

	carb_req = 0.5 * (calorie_req - protein_calories) // 4
	result["carb_req"]= carb_req

	fat_req = 0.5 * (calorie_req - protein_calories) // 9
	result["fat_req"] = fat_req

	result["diet"] = get_diet(carb_req,protein_req,fat_req,diet_type)

	return result

def get_exercise(surplus_calories,weight):
	result = []
	calories_per_min = 5 * 3.5 * weight / 200
	time = surplus_calories // calories_per_min
	item = {}
	item["name"] = "Walking"
	item["duration"] = round_to_ceil_10(time)
	result.append(item)

	item = {}
	item["name"] = "Running"
	item["duration"] = round_to_ceil_10(time / 2)
	result.append(item)

	return result


def get_diet(carbs,protein,fat,diet_type):
	result = {}

	constituents = {
		"breakfast":{
			"veg":["Starches","Fruits Related","Dairy","Plant-based Protein","Fats"],
			"nonveg":["Starches","Fruits Related","Dairy","Meat","Fats"]
		},
		"lunch":{
			"veg":["Starches","Vegetables","Plant-based Protein","Fats"],
			"nonveg":["Starches","Vegetables","Meat","Fats"]
		},
		"dinner":{
			"veg":["Starches","Vegetables","Plant-based Protein","Fats"],
			"nonveg":["Starches","Vegetables","Meat","Fats"]
		}
	}

	lunch = dinner = ((int(0.4 * carbs)),int(0.4 * protein),int(0.4 * fat))
	breakfast = (carbs - 2 * lunch[0],protein - 2 * lunch[1],fat - 2 * lunch[2])

	df = pd.read_csv("food_chart.csv")

	breakfast_constituents = []
	for food_type in constituents["breakfast"][diet_type]:
		breakfast_constituents.append(df.loc[df["Type"] == food_type].sample().to_records(index=False).tolist()[0])

	lunch_constituents = []
	for food_type in constituents["lunch"][diet_type]:
		lunch_constituents.append(df.loc[df["Type"] == food_type].sample().to_records(index=False).tolist()[0])

	dinner_constituents = []
	for food_type in constituents["dinner"][diet_type]:
		dinner_constituents.append(df.loc[df["Type"] == food_type].sample().to_records(index=False).tolist()[0])
	
	items = []
	for constituent in breakfast_constituents:
		item = (constituent[-3],constituent[-2],constituent[-1])
		items.append(item)
	breakfast_amounts = genetic(breakfast,items)

	items = []
	for constituent in lunch_constituents:
		item = (constituent[-3],constituent[-2],constituent[-1])
		items.append(item)
	lunch_amounts = genetic(lunch,items)

	items = []
	for constituent in dinner_constituents:
		item = (constituent[-3],constituent[-2],constituent[-1])
		items.append(item)
	dinner_amounts = genetic(dinner,items)

	breakfast_foods = []
	for index,amount in enumerate(breakfast_amounts):
		breakfast_foods.append({"name":breakfast_constituents[index][0],
			"amount":amount_to_string(amount)+" "+breakfast_constituents[index][2]})

	lunch_foods = []
	for index,amount in enumerate(lunch_amounts):
		lunch_foods.append({"name":lunch_constituents[index][0],
			"amount":amount_to_string(amount)+" "+lunch_constituents[index][2]})

	dinner_foods = []
	for index,amount in enumerate(dinner_amounts):
		dinner_foods.append({"name":dinner_constituents[index][0],
			"amount":amount_to_string(amount)+" "+dinner_constituents[index][2]})

	result["breakfast"] = breakfast_foods
	result["lunch"] = lunch_foods
	result["dinner"] = dinner_foods
	return result


print(get_recommendation(80,1.81,"veg"))



