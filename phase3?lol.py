from bsddb3 import db

#### PART 1: Creates databases and inserts elements ####

# Name of database files to be opened
# DB_File = "data.db"
da = "da.idx"  # Dates
em = "em.idx"  # Emails
te = "te.idx"  # Terms
re = "re.idx"  # Row IDs

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
re_db.open(re, None, db.DB_HASH, db.DB_CREATE)

# Skeletons for {database} being opened for each index type.
# database.open(DB_File ,None, db.DB_HASH, db.DB_CREATE)
# database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
# database.open(DB_File ,None, db.DB_QUEUE, db.DB_CREATE)
# database.open(DB_File ,None, db.DB_RECNO, db.DB_CREATE)
# The arguments correspond to (fileName, database name within the file for multiple databases, database type, flag to create database)

database = db.DB()
database.set_flags(db.DB_DUP)
database.open(re, None, db.DB_HASH, db.DB_CREATE)
curs = database.cursor()


# Output: Row Id | Subject field of all matching rows.

while(True):
    query = input("Query or q to exit: ")
    if (query == "q" or query == "Q"):
        break

    rec = curs.first()
    while rec:
        print(rec)
        rec = curs.next()

curs.close()
database.close()
