# Password Vault 1.1 by Fanat1c

# Going to use hash for the passwords 
# Starting by outputting to a simple text file
import os, sys, csv, getpass
import pandas as pd
from tabulate import tabulate

# Defines the path of the directory where the password storage .csv file will be stored
path = os.path.join(os.path.join(os.path.expanduser('~')), 'System/Library/PasswordStorage')

# Defines the path of where the main password is stored in a .txt file
path2 = os.path.join(os.path.join(os.path.expanduser('~')), 'System/Library/PasswordStorage/Main')


# Defines variable textfilepath as directory 'path' and a text file
textfilepath = os.path.join(path, "Passwords.csv")
mainpasswordpath = os.path.join(path2, "Main.txt")

# Clear out the initial post from the terminal 
os.system('clear')

# Encryption function for services/usernames/passwords
def encrypt():
	f = open(textfilepath, 'r')
	filedata = f.read()
	newdata = filedata.replace("a","<").replace("b",">").replace("e","{").replace("i","}").replace("o","[").replace("u","]").replace("g","=").replace("q","+").replace("k", "/")
	f = open(textfilepath, 'w')
	f.write(newdata)
	f.close()
	
# Decryption function for services/usernames/passwords
def decrypt():
	f = open(textfilepath, 'r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace("<","a").replace(">","b").replace("{","e").replace("}","i").replace("[","o").replace("]","u").replace("=","g").replace("+","q").replace("/", "k")
	f = open(textfilepath, 'w')
	f.write(newdata)
	f.close()

# Encrypt main password function
def encrypt_master():
	f = open(mainpasswordpath, 'r')
	filedata = f.read()
	newdata = filedata.replace("a","<").replace("b",">").replace("e","{").replace("i","}").replace("o","[").replace("u","]").replace("g","=").replace("q","+").replace("k", "/")
	f = open(mainpasswordpath, 'w')
	f.write(newdata)
	f.close()
		
# Decryption main password function
def decrypt_master():
	f = open(mainpasswordpath, 'r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace("<","a").replace(">","b").replace("{","e").replace("}","i").replace("[","o").replace("]","u").replace("=","g").replace("+","q").replace("/", "k")
	f = open(mainpasswordpath, 'w')
	f.write(newdata)
	f.close()		
		

# If the aforementioned variable 'path' doesn't exist, create it
# Variable 'f' creates a text file... w+ = writeable, and plus means if it exists ignore it
if not os.path.exists(path):
	os.makedirs(path)
	f = open(textfilepath, "w+")
	file = open(textfilepath, "a")
	file.write("SERVICE" + ",")
	file.write("USERNAME" + ",")
	file.write("PASSWORD" + "\n")
	file.close()
	
# create password, if 'path2' not found, creates it. Creates text file for main password
master_password = ""
def password_creation():
	if not os.path.exists(path2):
		os.makedirs(path2)
		m = open(mainpasswordpath, "w+")
		mainp = open(mainpasswordpath, "a")
		mainp.close()
		master_password = ""
		# Loop to ensure password isn't saved unless it matches
		while True:
			master_password = getpass.getpass("Please create a master password: ")
			master_password_again = getpass.getpass("Please re-enter master password: ")
			if master_password_again == master_password:
				f = open(mainpasswordpath, "w+")
				f.write(master_password)
				f.close()
				break
			else:
				print "Passwords didn't match...Try again."
				password_creation()
password_creation()

# Clears the terminal after password creation
os.system('clear')	

# First encrypt for master pass, calls 'encrypt_master()' function from earlier
encrypt_master()

# login function
def login():
	encrypt_master()
	# Blanking out user input (over the shoulder password theft)
	os.system("stty -echo")
	login_attempt = raw_input("Please enter master password: ")
	os.system("stty echo")
	# The stored master password is encrypted, user enters in "human readable" password, the program decrypts the password in the .txt file, reads it's contents, and compares the two
	decrypt_master()
	m = open(mainpasswordpath, "r")
	lines=m.readlines()
	master_password = lines[0]
	#If the contents match, the function closes and the program continues, then re-encrypts the .txt file. If they don't match, it will loop endlessly, preventing the user from continuing
	if login_attempt == master_password:
		m.close()
		encrypt_master()
	if login_attempt != master_password:
		print ("\n") + "Incorrect password, try again..."
		login()
	print ""
	m.close()
login()		

os.system('clear')

# Defining the main menu function
def main_menu():
	print (31 * '*')
	print "Password Manager 1.1 by Fanat1c"
	print (31 * '*')
	print "1. Add service and password"
	print "2. Access passwords"
	# User enters their selection number, then presses enter key
	choice = raw_input()
	os.system('clear')
	if choice == "1":
		file = open(textfilepath, "a")
		file.write(raw_input("Type in the service > ") + ",")
		file.write(raw_input("Type in the username > ") + ",")
		file.write(raw_input("Type in the password > ") + "\n")
		file.close()
		encrypt()
		os.system('clear')
		main_menu()	
	# Uses module called tabulate to return a pretty table from a .csv file	
	elif choice == "2": 
		decrypt()
		df = pd.read_csv(textfilepath)
		print tabulate(df, headers='keys', tablefmt='psql')
		encrypt()
		
		print raw_input("\nPress enter to return to main menu... ")
		os.system('clear')
		main_menu()		
	else: 
		os.system('clear')
		main_menu()
main_menu()

# UPCOMING CHANGES:
# 1. GUI
# 2. Actually encrypt main password, services, usernames, and passwords individually, with a secure encryption algorithm.
# 3. Package into .app file for all Mac users

# BUGS:
# 1. In the current encryption format, if you use certain special characters for passwords, the encryption/decryption process will almost definitely be a hot mess
# 2. The current application can't be packaged into a .app file because it uses the terminal, it needs a console/gui programmed to launch a .app file natively