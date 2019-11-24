from bsddb3 import db
import time
import os
import re

#### PART 1: Creates databases and inserts elements ####

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


#### PART 2: MAIN PROGRAM ####


# Brief Output: Row Id & Subject field of all matching rows.
# Full Output: Displays full record.
view = 1 # 1: Brief output | 2: Full output

while(True):
    os.system('cls' if os.name=='nt' else 'clear')

    # Has user choose whether to enter a query, change output display or exit.
    #main_menu(view)


    # Splits up entered query into a list of each word entered.
    # Should make it much easier to figure out wtf the user is asking.
    txt = input("Query: ")
    lst = []        # List that contains list of words after splitting
    if ' ' in txt:  # If input has any spaces
        q = txt.lower()
        if ":" in q:
            lst.append(re.split("[:]", q))  # Split on : then add to list
        elif ">" in q:
            lst.append(re.split(">=?", q))  # Split on > and >= then add to list
        elif "<" in q:
            lst.append(re.split("<=?", q))  # Split on < and <= then add to list
        else:    # Just one word
            lst.append([q])
    else:      # Input has no spaces
        txt = txt.lower()
        if ":" in txt:
            lst.append(txt.split(':'))
        elif ">" in txt:
            lst.append(re.split(">=?", txt))
        elif "<" in txt:
            lst.append(re.split("<=?", txt))
        else:
            lst.append([txt])
                
    print(lst)
    break


    # Test to print out all records in re (row id index file)
    # rec = cre.first()
    # while rec:
    #     print("1: \n")
    #     print(rec)
    #     print("\n")
    #     rec = cre.next()
    # break



########## Function definitions #######################
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

def main_menu(view):
    while(True):
        action = input("[1] Query\n[2] Mode change\n[3] Exit")
        if action == 2:
            mode_change(view)
        elif action == 3:
            print("Have a nice day!")
            time.sleep(2)
            exit()



cda.close()
cem.close()
cte.close()
cre.close()
re_db.close()
da_db.close()
em_db.close()
te_db.close()
