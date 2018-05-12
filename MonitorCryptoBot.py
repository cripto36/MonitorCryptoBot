import string
import telegram
import json
import requests
import logging
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.error import Unauthorized



def start(bot, update):		
	a=0	
	file_start = open("user.txt", "r")
	line = file_start.readlines()
	file_start.close()
	file_start = open("user.txt", "w")
	for x in range(0, len(line)):
		if(str(update.message.chat_id) == line[x].split(" ")[0]):			
			a=1
			file_start.writelines(str(update.message.chat_id) + " " + str(1) + " " + str(update.message.from_user.username) + "\n")
			bot.send_message(chat_id = update.message.chat_id, text = "Alert Enabled ")
		else:
			file_start.writelines(line[x])
	file_start.close()
	if(a==0):
		file_start_w = open("user.txt", "w")
		for i in range(0, len(line)):
			file_start_w.writelines(line[i])
		file_start_w.writelines(str(update.message.chat_id) + " " + str(1) + " " + str(update.message.from_user.username) + "\n")
		bot.send_message(chat_id = update.message.chat_id, text = "Welcome " + str(update.message.from_user.username) + ",\nYou have been registered.\nAlerts Enabled")
		file_start_w.close()
		bot.send_message(chat_id = str(myid().youridtelegram), text="New user registered: @" + str(update.message.from_user.username))

def max(bot, update):
	file_vol = open("volume.txt", "r")
	line_vol = file_vol.readline()
	file_vol.close()	
	if(line_vol==""):
		vol_max_js = requests.get('https://api.coinmarketcap.com/v1/global').json()
		max_vol=vol_max_js['total_24h_volume_usd']
	else:
		max_vol=line_vol
	file_btc = open("price_btc.txt", "r")
	line_btc = file_btc.readline()
	file_btc.close()	
	if(line_btc==""):
		btc_json_max = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin').json()
		max_btc=btc_json_max[0]['price_usd']
	else:
		max_btc=line_btc
	file_eth = open("price_eth.txt", "r")
	line_eth = file_eth.readline()
	file_eth.close()
	if(line_eth==""):
		eth_json_max = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum').json()
		max_eth=eth_json_max[0]['price_usd']
	else:
		max_eth=line_eth
	bot.send_message(chat_id=update.message.chat_id, text="Max BTC: " + "$ " + str(max_btc) + "\n" + "Max ETH: " + "$ " + str(max_eth) + "\n" + "Max VOL 24H: " + "$" + str(int(max_vol)))


def now(bot, update):
	volume_24_now = requests.get('https://api.coinmarketcap.com/v1/global').json()
	eth_json_now = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum').json()
	btc_json_now = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin').json()
	file_volume_now = open("volume.txt", "r")
	line_1vol_now = file_volume_now.readline()
	file_volume_now.close()
	if(line_1vol_now==""):
		max_volume_now=volume_24_now['total_24h_volume_usd']
	else:
		max_volume_now = line_1vol_now
	file_btc_now = open("price_btc.txt", "r")
	line_btc_now = file_btc_now.readline()
	file_btc_now.close()
	if(line_btc_now==""):
		max_btc_now=btc_json_now[0]['price_usd']
	else:
		max_btc_now=line_btc_now
	file_eth_now = open("price_eth.txt", "r")
	line_eth_now = file_eth_now.readline()
	file_eth_now.close()
	if(line_eth_now==""):
		max_eth_now=eth_json_now[0]['price_usd']
	else:
		max_eth_now=line_eth_now
	percent_from_max_btc = ((float(btc_json_now[0]['price_usd'])/float(max_btc_now))-1)*100
	percent_from_max_eth = ((float(eth_json_now[0]['price_usd'])/float(max_eth_now))-1)*100
	percent_from_max_vol = ((float(volume_24_now['total_24h_volume_usd'])/float(max_volume_now))-1)*100
	bot.send_message(chat_id=update.message.chat_id, text="BITCOIN: $ " + btc_json_now[0]['price_usd'] + "\nPercentage from max: " + str("%.2f" % percent_from_max_btc) + "%" +"\n\n" + "ETHEREUM: $ " + eth_json_now[0]['price_usd'] + "\nPercentage from max: " + str("%.2f" % percent_from_max_eth) + "%" + "\n\n" +  "VOLUME 24H: $" + str(int(volume_24_now['total_24h_volume_usd'])) + "\nPercentage from max: " + str("%.2f" % percent_from_max_vol) + "%")
	

def stop(bot, update):
	x=0
	file_user_stop = open("user.txt", "r")
	line = file_user_stop.readlines()
	file_user_stop.close()
	file_user_stop = open("user.txt", "w")
	for i in range(0,len(line)):
		if(str(update.message.chat_id) == line[i].split(" ")[0]):
			x=1
			file_user_stop.writelines(str(update.message.chat_id) + " " + str(0) + " " + str(update.message.from_user.username) + "\n")
			bot.send_message(chat_id=update.message.chat_id, text="Alert Disabled, if you want to exit database, type /suicide")
		else:					
			file_user_stop.writelines(line[i])
	file_user_stop.close()
	if(x==0):
		bot.send_message(chat_id=update.message.chat_id, text="You can't stop database because you are not registered")

def resetuser(bot, update, args):
	if(int(update.message.chat_id) == myid().youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]=="confirm"):
			file_user = open("user.txt", "w")
			file_user.close()
			bot.send_message(chat_id = update.message.chat_id, text="File user reset")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="To confirm enter parameter = confirm")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="You are not able to use this function")

def resetmax(bot, update, args):
	if(int(update.message.chat_id) == myid().youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]=="confirm"):
			file_btc = open("price_btc.txt", "w")
			file_btc.close()
			file_eth = open("price_eth.txt", "w")
			file_eth.close()
			file_vol = open("volume.txt", "w")
			file_vol.close()
			bot.send_message(chat_id = update.message.chat_id, text="File max eth/btc/vol24h reset")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="To confirm enter parameter = confirm")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="You are not able to use this function")


def setmax(bot, update, args):
	if(int(update.message.chat_id) == myid().youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==2 and float(ingresso[1])):
			if(ingresso[0] == "btc"):
				file_btc = open("price_btc.txt", "w")
				file_btc.write(ingresso[1])
				file_btc.close()
				bot.send_message(chat_id = update.message.chat_id, text="File max btc set")
			if(ingresso[0] == "eth"):
				file_eth = open("price_eth.txt", "w")
				file_eth.write(ingresso[1])
				file_eth.close()
				bot.send_message(chat_id = update.message.chat_id, text="File max eth set")
			if(ingresso[0] == "vol"):
				file_eth = open("volume.txt", "w")
				file_eth.write(str(int(ingresso[1])))
				file_eth.close()
				bot.send_message(chat_id = update.message.chat_id, text="File max volume24h set")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="First arg=btc/eth/vol\nSecond arg=maxprice")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="You are not able to use this function")
		
def help(bot, update):
	if(int(update.message.chat_id) == myid().youridtelegram):
		bot.send_message(chat_id = update.message.chat_id, text="/help info\n/start Start alerts and registration on bot\n/stop No Alerts\n/max price BTC/ETH/VOL24H Max price last period\n/now Current value\n/cap Total Market Cap $\n/setmax set max BTC/ETH/VOL24H\n/resetmax max BTC/ETH/VOL24H=0\n/resetuser reset users\n/stat View users use bot\n/suicide left bot\n/setuser set user alert\n/ban cancel a user from bot\n/updatebot send a message to users in db to self an update of bot")
	else:	
		bot.send_message(chat_id = update.message.chat_id, text="/help info\n/start Start Alert and registration on bot\n/stop No Alerts\n/max price BTC/ETH/VOL24H Max last period\n/now Current value\n/cap Total Market Cap $\n/stat view own state in database\n/suicide Left Bot")

def stat(bot, update):
	if(int(update.message.chat_id) == myid().youridtelegram):
		file_user = open("user.txt", "r")
		line_user = file_user.readlines()
		file_user.close()
		bot.send_message(chat_id = update.message.chat_id, text = "Bot is used from " + str(len(line_user)) + " users")
		lista_id = {}
		for c in range (0, len(line_user)):
			if(int(line_user[c].split(" ")[1])==1):
				lista_id[c] = line_user[c].split(" ")[2].split("\n")[0] + "*"
			if(int(line_user[c].split(" ")[1])==0):
				lista_id[c] = line_user[c].split(" ")[2].split("\n")[0]
		bot.send_message(chat_id = update.message.chat_id, text =  str(lista_id))
	else:
		x=0
		file_user = open("user.txt", "r")
		line_user = file_user.readlines()
		file_user.close()
		for c in range (0, len(line_user)):
			if(int(line_user[c].split(" ")[0])==int(update.message.chat_id)):
				x=1			
				if(int(line_user[c].split(" ")[1])==1):
					bot.send_message(chat_id = update.message.chat_id, text = "You are in database and your alerts are enabled")
					break
				if(int(line_user[c].split(" ")[1])==0):
					bot.send_message(chat_id = update.message.chat_id, text = "You are in database, but your alerts are disabled")
					break
		if(x==0):
			bot.send_message(chat_id = update.message.chat_id, text = "Unknown user, you are not in database!")

def suicide(bot, update):
	killme=0
	file_user_suicide = open("user.txt", "r")
	line = file_user_suicide.readlines()
	file_user_suicide.close()
	file_user_suicide = open("user.txt", "w")
	for i in range(0,len(line)):
		if(str(update.message.chat_id) == line[i].split(" ")[0]):
			killme=1			
			bot.send_message(chat_id=update.message.chat_id, text="Bot left, You have been canceled from database")
			if((i+1)<len(line)):
				file_user_suicide.writelines(line[i+1])
			else:
				file_user_suicide.writelines("")
		else:
			if(killme==1):
				if((i+1)<len(line)):	
					file_user_suicide.writelines(line[i+1])
				else:
					file_user_suicide.writelines("")
			else:			
				file_user_suicide.writelines(line[i])
	file_user_suicide.close()
	if(killme==1):
		bot.send_message(chat_id=str(myid().youridtelegram), text= "User @" + str(update.message.from_user.username) + " left bot")
	if(killme==0):
		bot.send_message(chat_id=update.message.chat_id, text="You can't left bot, because you are not in")	

def setuser(bot, update, args):
	if(int(update.message.chat_id) == myid().youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==2 and (ingresso[1]==str(0) or ingresso[1]==str(1))):
			x=0
			file_user = open("user.txt", "r")
			line_user = file_user.readlines()
			file_user.close()
			file_user_w = open("user.txt", "w")
			for c in range (0, len(line_user)):
				if(ingresso[0] + "\n" == line_user[c].split(" ")[2]):
					x=1
					file_user_w.writelines(line_user[c].split(" ")[0] + " " + ingresso[1] + " " + line_user[c].split(" ")[2])
					if(int(ingresso[1])==1):
						bot.send_message(chat_id = update.message.chat_id, text="User " + ingresso[0] + " set. Alert Enabled")
					if(int(ingresso[1])==0):
						bot.send_message(chat_id = update.message.chat_id, text="User " + ingresso[0] + " set. Alert Disabled")
				else:
					file_user_w.writelines(line_user[c])
			file_user_w.close()
			if(x==0):
				bot.send_message(chat_id = update.message.chat_id, text="User " + ingresso[0] + " is not found")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="Insert parameter 1 (username), parameter 2 (1 start/0 stop)")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="You are not able to use this function")



def ban(bot, update, args):
	if(int(update.message.chat_id) == myid().youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]!=""):
			kill=0
			file_user_kill = open("user.txt", "r")
			line = file_user_kill.readlines()
			file_user_kill.close()
			file_user_kill = open("user.txt", "w")
			for i in range(0,len(line)):
				if(ingresso[0] == line[i].split(" ")[2].split("\n")[0]):
					kill=1			
					bot.send_message(chat_id=update.message.chat_id, text="User " + ingresso[0] + " has been canceled")
					if((i+1)<len(line)):
						file_user_kill.writelines(line[i+1])
					else:
						file_user_kill.writelines("")
				else:
					if(kill==1):
						if((i+1)<len(line)):	
							file_user_kill.writelines(line[i+1])
						else:
							file_user_kill.writelines("")
					else:			
						file_user_kill.writelines(line[i])
			file_user_kill.close()
			if(kill==0):
				bot.send_message(chat_id=update.message.chat_id, text="User " + ingresso[0] + " is not in database")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Inserire 1 parametro (username to cancel)")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="You are not able to use this function")

def cap(bot, update):
	capitalization = requests.get('https://api.coinmarketcap.com/v1/global').json()
	bot.send_message(chat_id=update.message.chat_id, text="Total Market Cap: $" + str(int(capitalization['total_market_cap_usd'])))

def updatebot(bot, update, args):
	if(int(update.message.chat_id) == myid().youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]=="confirm"):
			file_user = open("user.txt", "r")
			lines = file_user.readlines()
			file_user.close()
			for c in range (0, len(lines)):
				time.sleep(.100)
				try:
					bot.send_message(chat_id=lines[c].split(" ")[0], text="Bot updated, type /help for info")
				except Unauthorized:
					bot.send_message(chat_id=myid().youridtelegram, text="User @" + lines[c].split(" ")[2].split("\n")[0] + " stopped bot.")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Insert parameter 1 = confirm")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="You are not able to use this function")



def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unknown command, type /help to see possible choices.")

class myid:
	youridtelegram=int(YOUR ID TELEGRAM)
	yourtokenbot='YOUR TOKEN BOT'
	pass


bot = telegram.Bot(token=myid().yourtokenbot)
updater = Updater(token=myid().yourtokenbot)
dispatcher = updater.dispatcher	
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
max_handler = CommandHandler('max', max)
dispatcher.add_handler(max_handler)
now_handler = CommandHandler('now', now)
dispatcher.add_handler(now_handler)
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)
resetuser_handler = CommandHandler('resetuser', resetuser, pass_args=True)
dispatcher.add_handler(resetuser_handler)
resetmax_handler = CommandHandler('resetmax', resetmax, pass_args=True)
dispatcher.add_handler(resetmax_handler)
setmax_handler = CommandHandler('setmax', setmax, pass_args=True)
dispatcher.add_handler(setmax_handler)
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)
stat_handler = CommandHandler('stat', stat)
dispatcher.add_handler(stat_handler)
suicide_handler = CommandHandler('suicide', suicide)
dispatcher.add_handler(suicide_handler)
setuser_handler = CommandHandler('setuser', setuser, pass_args=True)
dispatcher.add_handler(setuser_handler)
ban_handler = CommandHandler('ban', ban, pass_args=True)
dispatcher.add_handler(ban_handler)
cap_handler = CommandHandler('cap', cap)
dispatcher.add_handler(cap_handler)
updatebot_handler = CommandHandler('updatebot', updatebot, pass_args=True)
dispatcher.add_handler(updatebot_handler)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

while(1):
	time.sleep(300)
	volume_24 = requests.get('https://api.coinmarketcap.com/v1/global').json()
	eth_json = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum').json()
	btc_json = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin').json()
	file_main = open("user.txt", "r")
	lines = file_main.readlines()
	file_main.close()
	num_lines = len(lines)
	if(len(lines)==0):
		num_lines=1
	for c in range (0, num_lines):
			time.sleep(.100)
			file_volume = open("volume.txt", "r")
			line_1vol = file_volume.readline()
			file_volume.close()
			if(line_1vol==""):
				max_volume=0
			else:
				max_volume = int(line_1vol)	
			file_btc_in = open("price_btc.txt", "r")
			line_1btc = file_btc_in.readline()
			file_btc_in.close()
			if(line_1btc==""):
				max_price_btc=0
			else:
				max_price_btc = float(line_1btc)
			file_eth_in = open("price_eth.txt", "r")
			line_1eth = file_eth_in.readline()
			file_eth_in.close()
			if(line_1eth==""):
				max_price_eth=0
			else:
				max_price_eth = float(line_1eth)	
			if(int(volume_24['total_24h_volume_usd'])>int(max_volume)):	
				max_volume = int(volume_24['total_24h_volume_usd'])
			else:
				if(int(volume_24['total_24h_volume_usd'])<=int(max_volume)*0.8):
					if(int(lines[c].split(" ")[1])==1):
						try:
							bot.send_message(chat_id=lines[c].split(" ")[0], text="Alert! Volume 24h: $ " + str(int(volume_24['total_24h_volume_usd']))	+ "\nmax value volume 24h: $" + str(max_volume) + "\n-20%")
						except Unauthorized:
							bot.send_message(chat_id=myid().youridtelegram, text="User @" + lines[c].split(" ")[2].split("\n")[0] + " stopped bot.")			
					max_volume = int(volume_24['total_24h_volume_usd'])
			if(float(btc_json[0]['price_usd'])>float(max_price_btc)):
				max_price_btc = float(btc_json[0]['price_usd'])					
			else:
				if(float(btc_json[0]['price_usd'])<=float(max_price_btc)*0.8):
					if(int(lines[c].split(" ")[1])==1):
						try:
							bot.send_message(chat_id=lines[c].split(" ")[0], text="Alert! Current price BTC: $ "+ btc_json[0]	['price_usd'] + "\nMax price BTC: $ " + str(max_price_btc) + "\n-20%")
						except Unauthorized:
							bot.send_message(chat_id=myid().youridtelegram, text="User @" + lines[c].split(" ")[2].split("\n")[0] + " stopped bot.")
					max_price_btc = float(btc_json[0]['price_usd'])					
			if(float(eth_json[0]['price_usd'])>float(max_price_eth)):
				max_price_eth = float(eth_json[0]['price_usd'])							
			else:
				if(float(eth_json[0]['price_usd'])<=float(max_price_eth)*0.8):
					if(int(lines[c].split(" ")[1])==1):
						try:
							bot.send_message(chat_id=lines[c].split(" ")[0], text="Alert! Current price ETH: $ " + eth_json[0]	['price_usd'] + "\nMax price ETH: $ " + str(max_price_eth) + "\n-20%")
						except Unauthorized:
							bot.send_message(chat_id=myid().youridtelegram, text="User @" + lines[c].split(" ")[2].split("\n")[0] + " stopped bot.")					
					max_price_eth = float(eth_json[0]['price_usd'])				
	file_vol_out1 = open("volume.txt", "w")
	file_vol_out1.write(str(int(max_volume)))
	file_vol_out1.close()
	file_btc_out1 = open("price_btc.txt", "w")
	file_btc_out1.write(str(max_price_btc))
	file_btc_out1.close()
	file_eth_out1 = open("price_eth.txt", "w")
	file_eth_out1.write(str(max_price_eth))
	file_eth_out1.close()							

