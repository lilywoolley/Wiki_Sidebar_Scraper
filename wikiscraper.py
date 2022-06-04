from unicodedata import category
from pip._vendor import requests
from bs4 import BeautifulSoup
import time

while True:
	time.sleep(1)
	with open('data.txt', 'r+', encoding="utf-8") as f:
		read_data = f.readline()
		# Splits the first string before the ", " as the mainTopic and the following word as the category
		x = read_data.split(", ")
		
		# Try block to avoid index error crashing service
		try:
			mainTopic = x[0]
			category = x[1]
		except Exception as e:
			pass
		else:
			# Forms the url to scrape data from
			response = requests.get(url = "https://en.wikipedia.org/wiki/" + mainTopic)
			soup = BeautifulSoup(response.content, 'html.parser')
			table = soup.find("table", class_ = "infobox ib-country vcard")

			# Finds the row with the same name as the passed category
			for row in table.find_all("tr"):
				if (row.find("th", string = category) != None):
					break
			
			# If the row has the category already, sets it to the data row to find the data in its children
			if row.th.find(string = category) != None:
				dataRow = row
			else:
				dataRow = row.next_sibling
			
			i = 0
			# Error catching for possible datarows that only have one tag in them
			if len(dataRow.contents) < 2:
				dataRow = dataRow.next_sibling

			# Iterates through the data row finding the requested data
			for child in dataRow.children:
				# Error catching for spans
				if (child.find("span") != None):
					for kid in child.children:
						data = kid.contents
					if len(data) != 0:
						break
				i += 1	
				
				if i == 2:
					data = child.contents[0]
					break
			
			f.truncate(0)
			f.seek(0)
			
			# Error catching
			if (type(data) == list):
				holder = ""
				for entry in data:
					holder += entry.string

				f.write(holder)
				f.close()
			elif data == "":
				f.write("Category not listed")
			else:
				f.write(data.string)
				f.close()
	
	f.close()

	

