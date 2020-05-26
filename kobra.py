import socket
import requests
import json
import pyperclip
import threading
from colorama import init, Fore, Back
from mcstatus import MinecraftServer
#from pprint import pprint
from time import sleep
import time

#sock = socket.socket()

#functions

def main():
	try:
		while True:
			printLogo()

			print(Fore.WHITE)

			#print("Entering main menu...")
			print("")
			print("1) Port scanner")
			print("2) Subdomain scanner")
			print("3) Fast subdomain scan (only play & build subdomains in ports 25560:25590)")
			print("4) Get IP address from a domain")
			print("5) Short range server finder")
			print("6) MCSRVSTAT.us")
			print("7) Nmap port scanner")

			print("")
			#scanPortRange("nytrux.cf", 25565, 25580)

			option = input(Fore.WHITE + "> " + Fore.GREEN)

			if option == "q" or option == "quit" or option == "exit":
				exit()

			try:

				if option == "1":
					portScanner()

				elif option == "2":
					subdomainScanner()

				elif option == "3":
					fastSubdomainScanner()

				elif option == "4":
					getIpAddress()

				elif option == "5":
					serverFinder()

				elif option == "6":
					getServerStatus()

				elif option == "7":
					nmapPortScanner()
			except KeyboardInterrupt:
				pass
	except KeyboardInterrupt:
		print("")
		print(Fore.WHITE + "Exit script...")


def printLogo():

	print(Fore.RED)

	print(" ▄▀▀▄ █  ▄▀▀▀▀▄   ▄▀▀█▄▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▄   ▄▀▀▄▀▀▀▄  ▄▀▀▄ ▀▀▄ ")
	print("█  █ ▄▀ █      █ ▐ ▄▀   █ █   █   █ ▐ ▄▀ ▀▄ █   █   █ █   ▀▄ ▄▀ ")
	print("▐  █▀▄  █      █   █▄▄▄▀  ▐  █▀▀█▀    █▄▄▄█ ▐  █▀▀▀▀  ▐     █   ")
	print("  █   █ ▀▄    ▄▀   █   █   ▄▀    █   ▄▀   █    █            █   ")
	print("▄▀   █    ▀▀▀▀    ▄▀▄▄▄▀  █     █   █   ▄▀ ▄ ▄▀           ▄▀    ")
	print("█    ▐           █    ▐   ▐     ▐   ▐   ▐   █             █     ")
	print("▐                ▐                          ▐             ▐     ")
	print("")
	print(Fore.MAGENTA + "Recoded by F3DEX22")




def scanPort(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.5)
	result = sock.connect_ex((ip,port))

	if result == 0:
		print(Fore.GREEN + str(ip) + ":" + str(port) + " [Open]      ", end='\n')
	elif result == 11:
		print(Fore.RED + str(ip) + ":" + str(port) + " [Timeout]", end='\r')
	else:
#		print(result)
		print(Fore.WHITE + str(ip) + ":" + str(port) + " [Closed] ", end='\r')

	sock.close()
	return result


def scanPortRange(ip, fromPort, toPort):
	openPorts = []
	for port in range(int(fromPort), int(toPort)+1):
		if scanPort(ip, port) == 0:
			openPorts.append(ip + ":" + str(port));

	return openPorts

def threadScanPort(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.5)
	result = sock.connect_ex((ip,port))

	if result == 0:

		server = MinecraftServer.lookup(str(ip) + ":" + str(port))

		try:
			status = server.status()
			print(Fore.GREEN + str(ip) + ":" + str(port) + Fore.MAGENTA + " > " + Fore.WHITE + str(status.latency) + "ms | " + status.version.name + " (" + str(status.version.protocol) + ") | " + str(status.players.online) + "/" + str(status.players.max) + " | " + status.description.replace('\n', '\\n') )
		except Exception as e:
			print(Fore.GREEN + str(ip) + ":" + str(port) + " [Open port]" + " (" + str(e) + ")")
			#print(str(e))


	sock.close()



def multiThreadedScanPortRange(ip, fromPort, toPort, max_threads):
	for port in range(fromPort, toPort):

		while threading.active_count() > max_threads:
			#print("waiting...")
			sleep(1)

		threading.Thread(target=threadScanPort, args=[ip, port]).start()
	return


def portScanner():
	ip = input(Fore.WHITE + "Type the IP: " + Fore.GREEN)

	print(Fore.WHITE)
	print("1) Low ports scan [SSH, FTP, WEB]")
	print("2) Normal port scan [Minecraft common ports]")
	print("3) Custom port range scan")
	print("4) One port scan")
	print("5) Multi-threaded port scanner")

	port = input(Fore.WHITE + "Select an option: ")

	if port == "1":
		scanPortRange(ip, 1, 80)

	elif port == "2":
		scanPortRange(ip, 23000, 30000)

	elif port == "3":
		customPortFrom = input("From port: ")
		customPortTo = input("To port: ")
		openPorts = scanPortRange(ip, customPortFrom, customPortTo)

		print("                                         ")
		print("Scan summary")
		print("")
		print("Total open ports: " + str(len(openPorts)))
		print("")

		if(len(openPorts) == -1):
			print("Port list:")
			print(Fore.GREEN)
			for port in openPorts:
				print(port)
			print(Fore.WHITE)
		print("--------------------------")


	elif port == "4":
		customPort = input("Custom port: ")
		scanPort(ip, int(customPort))


	elif port == "5":

		fromPort = input("From port: ")
		toPort = input("To port: ")
		max_threads = input("Max threads: ")

		start = time.time()

		multiThreadedScanPortRange(ip, int(fromPort), int(toPort), int(max_threads))

		while threading.active_count() > 1:
			#print("Debug: " + str(threading.active_count()))
			sleep(1)

		#print(threading.active_count())
		finish = time.time()

		print(Fore.WHITE)
		print("Scan finished -- Report")
		print("")
		print("Time passed: " + str(round((finish - start))) + " second(s).")


def subdomainScanner():
	subdomains = ["www", "build", "web", "dev", "staff", "mc", "play", "jogar", "sys", "node1", "node2", "node3", "builder", "developer", "test", "test1", "forum", "bans", "baneos", "ts", "ts3", "sys1", "sys2", "mods", "bungee", "bungeecord", "array", "spawn", "server", "help", "client", "api", "smtp", "s1", "s2", "s3", "s4", "server1", "server2", "jugar", "login", "mysql", "phpmyadmin", "demo", "na", "eu", "us", "es", "fr", "it", "ru", "support", "developing", "discord", "backup", "buy", "buycraft", "go", "dedicado1", "dedi", "dedi1", "dedi2", "dedi3", "minecraft", "prueba", "pruebas", "ping", "register", "cdn", "stats", "store", "serie", "buildteam", "info", "host", "jogar", "proxy", "vps", "ovh", "partner", "partners", "appeals", "appeal", "store-assets"]
	domain = input(Fore.WHITE + "Type the domain: " + Fore.GREEN)
	print(Fore.WHITE)

	for subdomain in subdomains:
		currentSubdomain = subdomain + "." + domain
		try:
			subdomainIp = socket.gethostbyname(currentSubdomain)
			print(Fore.GREEN + "[Found] " + subdomain + "." + domain + " [" + subdomainIp + "]")
		except Exception as e:
			#print(e)
			print(Fore.WHITE + "[Not found] " + subdomain + "." + domain)
			pass


def getIpAddress():
	domain = input(Fore.WHITE + "Type the domain: " + Fore.GREEN)
	try:
		ip = socket.gethostbyname(str(domain))
		print(ip)
		pyperclip.copy(ip)
		print("The IP has been copied to clipboard")
	except Exception as e:
		print("The domain " + domain + " has not an IP")


def getServerStatus():
	#print("In development :C")
	#return
	
	domain = input(Fore.WHITE + "Type the IP: ")
	try:
		server = MinecraftServer.lookup(domain)
		print(Fore.WHITE + "Status: " + Fore.GREEN + "ONLINE")

		latency = server.ping()

		print(Fore.WHITE + "Ping: " + Fore.GREEN + latency)

		try:
			query = server.query()
			print(Fore.WHITE + "Query: " + Fore.GREEN + "YES")
		except:
			print(Fore.WHITE + "Query: " + Fore.RED + "NO")
	except Exception as e:
		print(e)
		print(Fore.RED + "An error occurred :C")


#main
init()
#print(Fore.WHITE + "kobra.py recoded by F3DEX22")

main()
