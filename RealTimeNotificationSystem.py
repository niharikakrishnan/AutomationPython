import requests
from bs4 import BeautifulSoup
import sys, select
from urllib.parse import urlparse
from twilio.rest import Client

ACCOUNT_SID = 'AC18af5c6a152f783dc6399f167d2cc3f2'
AUTH_TOKEN = '1503fb0b99712ced07c6ec46a226f2a1'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def wait_minute():
    import time
    time.sleep(60)

class Item:

    def __init__(self, company, url, notif_p):
    	self.company = company
    	self.url = url
    	self.notif_p = notif_p
    	self.actual_p = 0.0
    	self.prod_name = ""

    	if company == "Snapdeal":
    		self.get_sd_title()
    		self.get_sd_price()
    	elif company == "Amazon":
    		self.get_amazon_title()
    		self.get_amazon_price()
    	else:
    		self.get_fk_title()
    		self.get_fk_price()

    def get_sd_price(self):
    	try:
    		r = requests.get(self.url)
    		soup = BeautifulSoup(r.content, "html.parser")
    		data = soup.find_all("div", {"class":"row pdp-e-i-PAY"})[0]
    		span_data = data.find_all("span",{"class":"payBlkBig"})[0]
    		price_text = span_data.text.strip()
    		self.actual_p = float(price_text.replace(',',''))		#print self.actual_p

    	except:
    		print("\n---------------Incorrect URL or site has been recently modified. Try different item---------------")
    
    def get_sd_title(self):
    	try:
    		r = requests.get(self.url)
    		soup = BeautifulSoup(r.content, "html.parser")
    		title_data = soup.find_all("meta", {"name":"og_title"})[0] #print title_data
    		temp_title = title_data.get("content")
    		title_words = temp_title.split()
    		if len(title_words) > 3:
    			self.prod_name = title_words[0]+' '+title_words[1]+' '+title_words[2]
    		else:
    			self.prod_name = temp_title
    			#print self.prod_name
    	except:
    		print("\n---------------Incorrect URL or site has been recently modified. Try different item---------------")
		

    def get_amazon_price(self):
    	r = requests.get(self.url)
    	soup = BeautifulSoup(r.content, "html.parser")
    	data_obtained = 0
    	if data_obtained == 0 and len(soup.find_all("div", {"id":"price_feature_div"})) > 0:    #to fetch banner data
    		try:
    			data = soup.find_all("div", {"id":"price_feature_div"})[0]
    			span_data = data.find_all("span", {"class":"a-size-medium a-color-price"})[0]
    			self.actual_p = float(span_data.text.strip().replace(',',''))
    			data_obtained = 1

    		except:
    			pass

    	if len(soup.find_all("div", {"class":"sims-fbt-rows"})) > 0:	#to get data from this item
    		try:
    			data = soup.find_all("div", {"class":"sims-fbt-rows"})
    			span_data = data[0].find_all("span", {"class":"a-color-price"})[0]
    			price_text = span_data.text.strip()
    			self.actual_p = float(price_text.split()[1].replace(',',''))
    			data_obtained = 1

    		except:
    			pass

    	if data_obtained == 0 and len(soup.find_all("div",{"id":"tmmSwatches"})) > 0:	#to get data from swatch, mainly in books

    		try:
    			data = soup.find_all("div", {"id":"tmmSwatches"})[0]
    			li_data = soup.find_all("li", {"class":"swatchElement selected"})[0]
    			span_data = soup.find_all("span",{"class":"a-color-price"})[0]
    			self.actual_p = float(span_data.text.strip().replace(',',''))
    			data_obtained = 1

    		except:
    			print ("\n------Working-------")

    	if data_obtained == 0 and len(soup.find_all("div", {"id":"buybox"})) > 0:    #to fetch data from buybox
    		try:
    			data = soup.find_all("div", {"id":"buybox"})[0]
    			div_data = soup.find_all("div", {"id":"buyNewSection"})[0]
    			self.actual_p = float(div_data.text.strip().replace(',',''))
    			data_obtained = 1

    		except:
    			pass

    def get_amazon_title(self):
    	r = requests.get(self.url)
    	soup = BeautifulSoup(r.content, "html.parser")
    	try:
    		if len(soup.find_all("span",{"id":"productTitle"})) > 0:
    			title_data = soup.find_all("span",{"id":"productTitle"})[0]
    			title = title_data.text.strip()
    			temp_title = title.split()
    			if len(temp_title) > 4:
    				self.prod_name = temp_title[0]+' '+temp_title[1]+' '+temp_title[2]+' '+temp_title[3]
    			else:
    				self.prod_name = title

    	except:
    		pass

    def get_fk_price(self):
    	try:
    		r = requests.get(self.url)
    		soup = BeautifulSoup(r.content, "html.parser")
    		r = requests.get(self.url)
    		soup = BeautifulSoup(r.content, "html.parser")
    		data = soup.find_all("div", {"class":"prices"})
    		for item in data:
    			span_data = item.find_all("span", {"class":"selling-price omniture-field"})[0]
    			price_text = span_data.text.strip()
    			self.actual_p = float(price_text.split()[1].replace(',',''))

    	except:
    		print ("\n---------------Incorrect URL or site has been recently modified. Try different item---------------")
    		pass

    def get_fk_title(self):
    	try:
    		r = requests.get(self.url)
    		soup = BeautifulSoup(r.content, "html.parser")
    		title_data = soup.find_all("meta",{"name":"Keywords"})[0]
    		temp_title = title_data.get("content")
    		title_words = temp_title.split()
    		if len(title_words) > 3:
    			self.prod_name = title_words[0]+' '+title_words[1]+' '+title_words[2]
    		else:
    			self.prod_name = temp_title
    	except:
    		print("\n---------------Incorrect URL or site has been recently modified. Try different item---------------")
    		pass

def add_item_to_track(items):
	try:
		print ("\nPaste URL of product from E commerce site:")
		url = input().strip()
		parsed_uri = urlparse(url)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

		if str.find(domain, "amazon") > -1:
			company = "Amazon"
		elif str.find(domain, "snapdeal") > -1:
			company = "Snapdeal"
		elif str.find(domain, "flipkart"):
			company = "Flipkart"
		else:
			print ("Not a valid url")

		print ("\nEnter price below which you want to be notified:")
		notif_p = float(input())
		temp_item = Item(company, url, notif_p)
		client.messages.create(to = '+917507640066',from_ = '+17144971968',body = "you will be notified")

		if temp_item.actual_p < temp_item.notif_p:
			print ("\n---------------Item price is already less than notification price---------------")
			return
		else:
			items.append(temp_item)

	except:
		print ("An error occured")
		pass

def delete_tracked_item(items):
	if len(items) == 0:
		print ("\n---------------No item to delete---------------")
		return

	print_item_list(items)
	print ("\nEnter index of item to be deleted:")
	index = int(input())

	if index > len(items):
		print ("\n---------------Number of items is less than given index-------------")
		return

	elif index < 1:	
		print ("\n---------------Item index can't be less than 1-------------")
		return

	del_desc = items[index-1]
	items.pop(index-1)
	print ("\nFollowing item successfully deleted.")
	print (del_desc.company, " ",del_desc.prod_name)

def edit_notification_price(items):
	if len(items) == 0:
		print ("\n---------------No item to edit---------------")
		return

	print_item_list(items)
	print ("\nEnter index of item to be edited:")
	index = int(input())
	if index > len(items):
		print ("\n---------------Number of items is less than given index-------------")
		return

	elif index < 1:
		print ("\n---------------Item index can't be less than 1---------------")
		return

	print("\nEnter new notification price:")
	new_price = float(input())
	if new_price >= items[index-1].actual_p:
		print ("\n---------------Entered price is more than the actual price---------------")
		client.messages.create(to = '+917507640066',from_ = '+17144971968',body = "Sorry. Entered price is more than the actual price")
		return
	items[index-1].notif_p = new_price

def print_item_list(items):
    print ("\n%-12s %-45s %-18s %-18s" %("Company", "Product", "Present Price", "Notification Price"))

    for item in items:
    	print ("%-12s %-45s %-18.1f %-18.1f" %(item.company, item.prod_name, item.actual_p, item.notif_p))

def save_item_list(items):
	record_file = open("saved_items.txt","w")
	for item in items:
		record_file.write(item.company+" "+str(item.notif_p)+" "+item.url+"\n")
		record_file.close()

def process_input(my_input, items):
    my_input = input().strip()

    if my_input.lower() == 'q' or my_input.lower() == 'quit':
    	print ("\nDo you want to save item list  (\'Y\' or \'N\')")
    	is_save = input()
    	if is_save.lower() == 'y':
    		save_item_list(items)	#write to file here
    	exit()

    elif my_input.lower() == 'h' or my_input.lower() == 'help':		
    	#print help
    	pass

    elif my_input == '1':	
    	add_item_to_track(items)

    elif my_input == '2':	
    	delete_tracked_item(items)

    elif my_input == '3':
    	print_item_list(items)

    elif my_input == '4':
    	edit_notification_price(items)

    elif my_input == '5':
    	save_item_list(items)

    else:
    	print ("\nInput not recognised. Please enter correct value")
    	print ("\nEnter...\n1 To add item to track\n2 To delete tracked item\n3 To print tracked item list\n4 To edit notification price of item\n5 To save item list\n\'Q\' or \'quit\' to exit from program\n\'h\' or \'help\' to view operating instructions")    

def update_notif_p(items):

	notify_items = []
	for item in items:
		if item.company == "Snapdeal":
		    item.get_sd_price()
		elif item.company == "Amazon":
		    item.get_amazon_price()
		else:
		    item.get_fk_price()

		if item.actual_p < item.notif_p:
		    notify_items.append(item)

		if len(notify_items) > 0:
			print ("\n**********Notification Alert !!! **********\nFollowing items are below their notification price")
			print_item_list(notify_items)

if __name__ == "__main__":
	items = []
	print ("Checking for previously saved items...")
	try:
		saved_items = open("saved_items.txt","r")
		all_items = saved_items.readlines()
		for item in all_items:
			item_values = item.split()
			temp_item = Item(item_values[0], item_values[2], float(item_values[1]))
			items.append(temp_item)

			if len(items) > 0:
				print("\nFollowing ",len(items)," items have been loaded from previous save:")
				print_item_list(items)

			else:
				print("\nNo item has been saved previously")
	except:
		pass

	print("\nEnter...\n1 To add item to track\n2 To delete tracked item\n3 To print tracked item list\n4 To edit notification price of item\n5 To save item list\n\'Q\' or \'quit\' to exit from program\n\'h\' or \'help\' to view operating instructions")
	while(1):
	i, o, e = select.select([sys.stdin], [], [], 20)
	if (i):
		process_input(i, items)
	elif len(items) > 0:
		update_notif_p(items)

