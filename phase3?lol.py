from bsddb3 import db
import time
import os
import re

#### PART 1: Creates 4 databases based on the 4 index files and initializes cursors to each database. ###########################################

# Name of database files to be opened
# DB_File = "data.db"
da = "da.idx"  # Dates
em = "em.idx"  # Emails
te = "te.idx"  # Terms
re2 = "re.idx"  # Row IDs

# Creates/opens primary database NOT SURE WE ACTUALLY NEED THIS.
# P_db = db.DB() # Creates instance of Berkeley DB: database
# P_db.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
# P_db.open(DB_File ,None, db.DB_HASH, db.DB_CREATE)

# Creates/opens secondary databases.
da_db = db.DB()
da_db.set_flags(db.DB_DUP)
da_db.open(da, None, db.DB_BTREE, db.DB_CREATE)

em_db = db.DB()
em_db.set_flags(db.DB_DUP)
em_db.open(em, None, db.DB_BTREE, db.DB_CREATE)

te_db = db.DB()
te_db.set_flags(db.DB_DUP)
te_db.open(te, None, db.DB_BTREE, db.DB_CREATE)

re_db = db.DB()
re_db.set_flags(db.DB_DUP)
re_db.open(re2, None, db.DB_HASH, db.DB_CREATE)

# Skeletons for {database} being opened for each index type.
# database.open(DB_File ,None, db.DB_HASH, db.DB_CREATE)
# database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
# database.open(DB_File ,None, db.DB_QUEUE, db.DB_CREATE)
# database.open(DB_File ,None, db.DB_RECNO, db.DB_CREATE)
# The arguments correspond to (fileName, database name within the file for multiple databases, database type, flag to create database)

# Defines cursors
cda = da_db.cursor()
cem = em_db.cursor()
cte = te_db.cursor()
cre = re_db.cursor()
####### END OF BUILDING CURSOR STUFF ###########################################################################################################################



####### SOME RANDOM VARIABLES:

# Brief Output: Row Id & Subject field of all matching rows.
# Full Output: Displays full record.
view = 1 # 1: Brief output | 2: Full output

range = "0" # 0 if date is exact, otherwise equals one of: >, <, >=, <=.




	# Code to print out all records of index file "re.idx". Just used to test with.
	# rec = cre.first()
	# while rec:
	#	  print("1: \n")
	#	  print(rec)
	#	  print("\n")
	#	  rec = cre.next()
	# break


########## PART 2: FUNCTION DEFINITIONS #######################
def mode_change(view):
	while(True):
		view = input("output=full or output=brief?")
		if view == "output=full":
			view = 2
			break
		elif view == "output=brief":
			view = 1
			break
		print("Error, try again.")

# Has user choose whether to enter a query, change output display or exit.
def main_menu(view):
	while(True):
		action = input("[1] Query\n[2] Mode change\n[3] Exit")
		if action == 2:
			mode_change(view)
		elif action == 3:
			print("Have a nice day!")
			time.sleep(2)
			exit()


### I am basing the following function definitions off of the marking rubric functionality list from eclass.

# single_search(): Search when only a single condition present, could possibly find a way to call back to this function when multiple conditions present.
# PROBLEM: For some reason 
def single_search(x):
	row = []
	i = 0
	
	# I have been testing this fn with the command: "subj:can" which should output all records with the term "can" in it 
	if(True):
		term1 = x[0]
		term2 = x[1].encode("utf-8") # encodes second term
		term1 = term1.lower()
		print(term1) # tests inputted first term
		print(term2) # tests inputted second term; shows: b'can'

		rec = cte.set(term2.encode("utf-8")) # DOES NOT FIND ANYTHING; SOMETHING WRONG WITH MATCHING
		print(rec[0].decode("utf-8")) # THE ENCODED SECOND TERM DOES NOT MATCH THE KEY IN THE INDEX FILE

		if term1 == "subj" or term1 == "subject" or term1 == "body":
			result = cte.set(term2.encode("utf-8"))
			print(result)
			print(result.decode("utf-8"))
			print(result)
			
			if result != None:
				row[i] = result[1].decode("utf-8")
				i += 1

				dup = cte.next_dup()
				while(dup != None):
					row[i] = dup[1].decode("utf-8")
					dup = cte.next_dup()
					i += 1
			j = 0
			while(j < i):
				result = cre.set(row[j].encode("utf-8"))
				print(result.decode("utf-8"))
				j += 1
		
		elif term1 == "date":
			range_search()
		elif term1 == "from" or term1 == "to" or term1 == "cc" or term1 == "bcc":
			result = cem.set(term2.encode("utf-8"))
		elif term1.find("%") != -1:
			partial_search()

			
	
def multiple_search():
	exit()

def partial_search():
	exit()

def range_search():
	exit()

def complex_search():
	exit()

def output(view):
	exit()





############ PART 3: MAIN PROGRAM ####################################################################
# So i never put in an actual main() cuz none of the lab's did and I dont know if it affects anything, but if anyone feels like it be my guest.

while(True):
	os.system('cls' if os.name=='nt' else 'clear')

	# See function definition for description. Commented out to save time while testing.
	#main_menu(view)


	# The following code Splits up the entered query into a list of each word entered.
	#***** CONSIDERS THAT THERE CAN BE ONLY ONE RANGED "DATE" CONDITION IN THE QUERY.
	txt = input("Query: ")
	x = re.split(" |:|>=|<=|<|>", txt)
	i = 0
	len = len(x)
	while(i < len):
		if x[i] == "":
			x.remove(x[i])
			len = len-1
			continue
		if x[i].lower() == "date":
			if txt.find("<") != -1:
				range = "<"
			elif txt.find("<=") != -1:
				range = "<="
			elif txt.find(">") != -1:
				range = ">"
			elif txt.find(">=") != -1:
				range = ">="
		i = i+1
		# print(x)
		# test = input(" ")

	# Checks if only 1 command given, if yes single condition search is initiated.
	if len == 2 or len == 1:
		single_search(x)
		test = input(" ")
		break
	












cda.close()
cem.close()
cte.close()
cre.close()
re_db.close()
da_db.close()
em_db.close()
te_db.close()
