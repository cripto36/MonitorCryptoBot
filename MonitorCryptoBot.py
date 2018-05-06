import string
import telegram
import json
import requests
import logging
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters



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
			bot.send_message(chat_id = update.message.chat_id, text = "Alert Abilitati ")
		else:
			file_start.writelines(line[x])
	file_start.close()
	if(a==0):
		file_start_w = open("user.txt", "w")
		for i in range(0, len(line)):
			file_start_w.writelines(line[i])
		file_start_w.writelines(str(update.message.chat_id) + " " + str(1) + " " + str(update.message.from_user.username) + "\n")
		bot.send_message(chat_id = update.message.chat_id, text = "Benvenuto " + str(update.message.from_user.username) + ",\nSei stato registrato nel database.\nAlert Abilitati")
		file_start_w.close()

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
	bot.send_message(chat_id=update.message.chat_id, text="MAX BTC: " + "$ " + str(max_btc) + "\n" + "MAX ETH: " + "$ " + str(max_eth) + "\n" + "MAX VOL 24H: " + "$" + str(int(max_vol)))


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
	bot.send_message(chat_id=update.message.chat_id, text="BITCOIN: $ " + btc_json_now[0]['price_usd'] + "\nPercentuale dal massimo: " + str("%.2f" % percent_from_max_btc) + "%" +"\n\n" + "ETHEREUM: $ " + eth_json_now[0]['price_usd'] + "\nPercentuale dal massimo: " + str("%.2f" % percent_from_max_eth) + "%" + "\n\n" +  "VOLUME 24H: $" + str(int(volume_24_now['total_24h_volume_usd'])) + "\nPercentuale dal massimo: " + str("%.2f" % percent_from_max_vol) + "%")
	

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
			bot.send_message(chat_id=update.message.chat_id, text="Alert Disabilitati, se vuoi uscire dal database digita /suicide")
		else:					
			file_user_stop.writelines(line[i])
	file_user_stop.close()
	if(x==0):
		bot.send_message(chat_id=update.message.chat_id, text="Nulla da disabilitare, non sei presenta nel database.\nPremi start per registrarti e avviare gli alert!")

def resetuser(bot, update, args):
	if(int(update.message.chat_id) == youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]=="confirm"):
			file_user = open("user.txt", "w")
			file_user.close()
			bot.send_message(chat_id = update.message.chat_id, text="File user resettato")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="Per confermare inserire parametro 1 = confirm")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="Non sei abilitato per resettare gli utenti")

def resetmax(bot, update, args):
	if(int(update.message.chat_id) == youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]=="confirm"):
			file_btc = open("price_btc.txt", "w")
			file_btc.close()
			file_eth = open("price_eth.txt", "w")
			file_eth.close()
			file_vol = open("volume.txt", "w")
			file_vol.close()
			bot.send_message(chat_id = update.message.chat_id, text="File max eth/btc/vol24h resettati")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="Per confermare inserire parametro 1 = confirm")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="Non sei abilitato per resettare i massimi di btc/eth")


def setmax(bot, update, args):
	if(int(update.message.chat_id) == youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==2 and float(ingresso[1])):
			if(ingresso[0] == "btc"):
				file_btc = open("price_btc.txt", "w")
				file_btc.write(ingresso[1])
				file_btc.close()
				bot.send_message(chat_id = update.message.chat_id, text="File max btc settato")
			if(ingresso[0] == "eth"):
				file_eth = open("price_eth.txt", "w")
				file_eth.write(ingresso[1])
				file_eth.close()
				bot.send_message(chat_id = update.message.chat_id, text="File max eth settato")
			if(ingresso[0] == "vol"):
				file_eth = open("volume.txt", "w")
				file_eth.write(str(int(ingresso[1])))
				file_eth.close()
				bot.send_message(chat_id = update.message.chat_id, text="File max volume24h settato")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="primo arg=btc/eth/vol\nsecondo arg=prezzomax")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="Non sei abilitato per accedere a questa funzione!")
		
def help(bot, update):
	if(int(update.message.chat_id) == youridtelegram):
		bot.send_message(chat_id = update.message.chat_id, text="/help Premi per info\n/start Avvio alert e ingresso nel bot\n/stop No Alert\n/max Prezzo BTC/ETH/VOL24H Massimo ultimo periodo\n/now Valore corrente\n/cap Visualizza Market Cap $\n/setmax Setta massimi BTC/ETH/VOL24H\n/resetmax Massimi BTC/ETH/VOL24H=0\n/resetuser Resetta gli user\n/stat Visualizza gli utenti che utilizzano il bot\n/suicide Uscita dal bot\n/setuser Setta l'alert di un user\n/ban cancella un utente dal database\n/updatebot invia un messaggio a tutti gli utenti presenti nel db per segnalare un update del bot")
	else:	
		bot.send_message(chat_id = update.message.chat_id, text="/help Premi per info\n/start Avvio alert e ingresso nel bot\n/stop No Alert\n/max Prezzo BTC/ETH/VOL24H Massimo ultimo periodo\n/now Valore corrente\n/cap Visualizza Market Cap $\n/stat Visualizza il proprio stato nel database\n/suicide Uscita dal bot")

def stat(bot, update):
	if(int(update.message.chat_id) == youridtelegram):
		file_user = open("user.txt", "r")
		line_user = file_user.readlines()
		file_user.close()
		bot.send_message(chat_id = update.message.chat_id, text = "Il bot viene utilizzato da " + str(len(line_user)) + " utenti")
		lista_id = {}
		for c in range (0, len(line_user)):
			if(int(line_user[c].split(" ")[1])==1):
				lista_id[c] = line_user[c].upper().split(" ")[2].split("\n")[0]
			if(int(line_user[c].split(" ")[1])==0):
				lista_id[c] = line_user[c].split(" ")[2].split("\n")[0]
		bot.send_message(chat_id = update.message.chat_id, text = "Maiuscolo == Alert Attivi\nMinuoscolo == Alert Disattivati\n" + str(lista_id))
	else:
		x=0
		file_user = open("user.txt", "r")
		line_user = file_user.readlines()
		file_user.close()
		for c in range (0, len(line_user)):
			if(int(line_user[c].split(" ")[0])==int(update.message.chat_id)):
				x=1			
				if(int(line_user[c].split(" ")[1])==1):
					bot.send_message(chat_id = update.message.chat_id, text = "Sei presente nel database e hai gli alert abilitati")
					break
				if(int(line_user[c].split(" ")[1])==0):
					bot.send_message(chat_id = update.message.chat_id, text = "Sei presente nel database, ma hai gli alert disabilitati")
					break
		if(x==0):
			bot.send_message(chat_id = update.message.chat_id, text = "Utente sconosciuto, non sei presente nel database!")

def suicide(bot, update):
	killme=0
	file_user_suicide = open("user.txt", "r")
	line = file_user_suicide.readlines()
	file_user_suicide.close()
	file_user_suicide = open("user.txt", "w")
	for i in range(0,len(line)):
		if(str(update.message.chat_id) == line[i].split(" ")[0]):
			killme=1			
			bot.send_message(chat_id=update.message.chat_id, text="Bot abbandonato, sei stato cancellato dal database")
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
	if(killme==0):
		bot.send_message(chat_id=update.message.chat_id, text="Non puoi abbandonare perchè non sei presente nel database")	

def setuser(bot, update, args):
	if(int(update.message.chat_id) == youridtelegram):
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
						bot.send_message(chat_id = update.message.chat_id, text="User " + ingresso[0] + " settato con successo. Alert Abilitati")
					if(int(ingresso[1])==0):
						bot.send_message(chat_id = update.message.chat_id, text="User " + ingresso[0] + " settato con successo. Alert Disabilitati")
				else:
					file_user_w.writelines(line_user[c])
			file_user_w.close()
			if(x==0):
				bot.send_message(chat_id = update.message.chat_id, text="User " + ingresso[0] + " non trovato")
		else:
			bot.send_message(chat_id = update.message.chat_id, text="Inserire parametro 1 (username utente), parametro 2 (1 start/0 stop)")
	else:
		bot.send_message(chat_id = update.message.chat_id, text="Non sei abilitato per questa funzione!")



def ban(bot, update, args):
	if(int(update.message.chat_id) == youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]!=""):
			kill=0
			file_user_kill = open("user.txt", "r")
			line = file_user_kill.readlines()
			file_user_kill.close()
			file_user_kill = open("user.txt", "w")
			for i in range(0,len(line)):
				if(ingresso[0] + "\n" == line[i].split(" ")[2]):
					kill=1			
					bot.send_message(chat_id=update.message.chat_id, text="User " + ingresso[0] + " eliminato dal database")
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
				bot.send_message(chat_id=update.message.chat_id, text="User " + ingresso[0] + " non presente nel database")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Inserire 1 parametro (username utente da eliminare)")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Non sei abilitato per accedere a questa funzione")

def cap(bot, update):
	capitalization = requests.get('https://api.coinmarketcap.com/v1/global').json()
	bot.send_message(chat_id=update.message.chat_id, text="Market Cap: $" + str(int(capitalization['total_market_cap_usd'])))

def updatebot(bot, update, args):
	if(int(update.message.chat_id) == youridtelegram):
		ingresso = ' '.join(args).split(" ")
		if(len(ingresso)==1 and ingresso[0]=="confirm"):
			file_user = open("user.txt", "r")
			lines = file_user.readlines()
			file_user.close()
			for c in range (0, len(lines)):
				bot.send_message(chat_id=lines[c].split(" ")[0], text="Bot aggiornato, premi /help per le info")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Inserire parametro 1 = confirm")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Non sei abilitato per accedere a questa funzione")

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Comando inesistente, premi /help per vedere le possibili scelte.")



bot = telegram.Bot(token='id(token)yourtelegrambot')
updater = Updater(token='id(token)yourtelegrambot')
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
						bot.send_message(chat_id=lines[c].split(" ")[0], text="Alert! Volume 24h: $ " + str(int(volume_24['total_24h_volume_usd']))	+ "\nValore max Volume 24h: $" + str(max_volume) + "\n-20%")			
					max_volume = int(volume_24['total_24h_volume_usd'])
			if(float(btc_json[0]['price_usd'])>float(max_price_btc)):
				max_price_btc = float(btc_json[0]['price_usd'])					
			else:
				if(float(btc_json[0]['price_usd'])<=float(max_price_btc)*0.8):
					if(int(lines[c].split(" ")[1])==1):
						bot.send_message(chat_id=lines[c].split(" ")[0], text="Alert! Valore attuale BTC: $ "+ btc_json[0]	['price_usd'] + "\nValore max BTC: $ " + str(max_price_btc) + "\n-20%")
					max_price_btc = float(btc_json[0]['price_usd'])					
			if(float(eth_json[0]['price_usd'])>float(max_price_eth)):
				max_price_eth = float(eth_json[0]['price_usd'])							
			else:
				if(float(eth_json[0]['price_usd'])<=float(max_price_eth)*0.8):
					if(int(lines[c].split(" ")[1])==1):
						bot.send_message(chat_id=lines[c].split(" ")[0], text="Alert! Valore attuale ETH: $ " + eth_json[0]	['price_usd'] + "\nValore max ETH: $ " + str(max_price_eth) + "\n-20%")					
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

