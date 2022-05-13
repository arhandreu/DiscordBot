import json

cenzor_list = []

with open('cenzor.txt', encoding='utf-8') as file:
	for string in file:
		word = string.lower().strip()
		if word != "":
			cenzor_list.append(word)
			
with open('cenzor.json', 'w', encoding='utf-8') as file:
	json.dump(cenzor_list, file)
