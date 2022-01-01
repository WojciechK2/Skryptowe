# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.realpath('__file__'))
openinghours_filename = os.path.join(script_dir, '../opening_hours.json')
menu_filename = os.path.join(script_dir, '../menu.json')
orders_filename = os.path.join(script_dir, '../orders.txt')

with open(openinghours_filename) as f:
	openinghours_data = json.load(f)
	
with open(menu_filename) as f:
	menu_data = json.load(f)

class ActionReadOpeningHoursFromJSONFile(Action):

	def name(self) -> Text:
		return "action_read_opening_hours"
		
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
			
		question_day = tracker.get_slot("date_question_day")
		
		if question_day != None:
			question_day = question_day[0].upper() + question_day[1:]
		
		question_time = tracker.get_slot("date_question_time")
		
		if question_time != None:
			try:
				question_time = int(question_time)
			except ValueError: 
				question_time = None

		return_string = ""

		if question_day == None:
			for x in openinghours_data["items"].keys():
				inner_dict = openinghours_data["items"].get(x)
				
				return_string += x
				return_string += " : open: "
				return_string += str(inner_dict["open"])
				return_string += " : close: "
				return_string += str(inner_dict["close"])
				return_string += "\n"
				
		elif question_day != None and question_time == None:
			
			if question_day in openinghours_data["items"].keys():
				
				inner_dict = openinghours_data["items"][question_day]
				
				if inner_dict["open"] != 0:
					
					return_string = f'At {question_day} we are open from {inner_dict["open"]} to {inner_dict["close"]}'
				
				else:
				
					return_string = f'At {question_day} we are closed'
			else:
				return_string = f'I don\'t understand, please check your spelling and repeat the question'
				
		elif question_day != None and question_time != None:
			
			if question_day in openinghours_data["items"].keys():
				
				inner_dict = openinghours_data["items"][question_day]
				
				opening = inner_dict["open"]
				closing = inner_dict["close"]
				
				if question_time >= opening and question_time <= closing:
				
					return_string = f'Yes, on {question_day} at {question_time} we are open, assuming that we are using 24 hour format'
					
				else:
				
					return_string = f'No, on {question_day} at {question_time} we are closed, assuming that we are using 24 hour format'
			else:
				return_string = f'I don\'t understand, please check your spelling and repeat the question'
			
		dispatcher.utter_message(return_string)
		return [SlotSet("date_question_day",None),SlotSet("date_question_time",None)]
		
class ActionReadMenuItemsFromJSONFile(Action):

	def name(self) -> Text:
		return "action_read_menu_items"
		
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
		
		return_string = ""
			
		for x in menu_data["items"]:

			return_string += "Name: "
			return_string += str(x["name"])
			return_string += " : price: "
			return_string += str(x["price"])
			return_string += " : prep_time: "
			return_string += str(x["preparation_time"])
			return_string += "\n"

		dispatcher.utter_message(return_string)
		
class ActionCheckOrderedItems(Action):

	def name(self) -> Text:
		return "action_check_ordered_items"
		
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
			
		ordered = tracker.get_slot("menu_item")
		dishes = []
		
		for x in menu_data["items"]:
			dishes.append(x["name"].lower())
		
		error = False
		invalid_item = ""
		
		for x in ordered:
			x = x.lower()
			if x in dishes:
				continue
			else:
				error = True
				invalid_item = x
				break

		if error:
			dispatcher.utter_message("I am sorry" + invalid_item + "is not in the offer")
		else:
			dispatcher.utter_message("Order received")
	
