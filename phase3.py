from bsddb3 import db
import time
import os
import re

# region Constant Variables
DEBUG = False
UTF_8 = "utf-8"
VIEW_BRIEF = 1  # DEFAULT
VIEW_FULL = 2
WILDCARD_CHAR = "%"
DELIMITERS = (":", "<", ">", "<=", ">=", "%")
# endregion

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


# SOME RANDOM VARIABLES:

# Brief Output: Row Id & Subject field of all matching rows.
# Full Output: Displays full record.
view = VIEW_BRIEF  # 1: Brief output | 2: Full output

range = "0"  # 0 if date is exact, otherwise equals one of: >, <, >=, <=.


########## PART 2: FUNCTION DEFINITIONS #######################
def mode_change(view):
    while(True):
        view = input("output=full or output=brief?")
        if view == "output=full":
            view = VIEW_FULL
            break
        elif view == "output=brief":
            view = VIEW_BRIEF
            break
        print("Error, try again.")

# Has user choose whether to enter a query, change output display or exit.


def main_menu():
    while(True):
        print_title("Main menu")
        action = input("[1] Enter a command\n[2] Exit\nInput: ").strip()
        if action == "1":
            entering_command()
        elif action == "2":
            print("Have a nice day!")
            time.sleep(2)
            # we need the break here so we could close the database
            break
        else:
            print("Invalid input")
            time.sleep(2)


# I am basing the following function definitions off of the marking rubric functionality list from eclass.

# single_search(): Search when only a single condition present, could possibly find a way to call back to this function when multiple conditions present.
# PROBLEM: For some reason
# def single_search(x):
# 	row = []
# 	i = 0

# 	# I have been testing this fn with the command: "subj:can" which should output all records with the term "can" in it
# 	if(True):
# 		term1 = x[0]
# 		term2 = x[1].encode("utf-8") # encodes second term
# 		term1 = term1.lower()
# 		print(term1) # tests inputted first term
# 		print(term2) # tests inputted second term; shows: b'can'

# 		rec = cte.set(term2.encode("utf-8")) # DOES NOT FIND ANYTHING; SOMETHING WRONG WITH MATCHING
# 		print(rec[0].decode("utf-8")) # THE ENCODED SECOND TERM DOES NOT MATCH THE KEY IN THE INDEX FILE

# 		if term1 == "subj" or term1 == "subject" or term1 == "body":
# 			result = cte.set(term2.encode("utf-8"))
# 			print(result)
# 			print(result.decode("utf-8"))
# 			print(result)

# 			if result != None:
# 				row[i] = result[1].decode("utf-8")
# 				i += 1

# 				dup = cte.next_dup()
# 				while(dup != None):
# 					row[i] = dup[1].decode("utf-8")
# 					dup = cte.next_dup()
# 					i += 1
# 			j = 0
# 			while(j < i):
# 				result = cre.set(row[j].encode("utf-8"))
# 				print(result.decode("utf-8"))
# 				j += 1

# 		elif term1 == "date":
# 			range_search(query,filtered_indices)
# 		elif term1 == "from" or term1 == "to" or term1 == "cc" or term1 == "bcc":
# 			result = cem.set(term2.encode("utf-8"))
# 		elif term1.find("%") != -1:
# 			partial_search(query,filtered_indices)


# def multiple_search():
# 	exit()

# def range_search():
#         exit()

# def complex_search():
#         exit()
"""
    Returns a set of row_ids (string) based on a given key and cursor
"""


def partial_search(cursor, key):
    result_indices = set()
    iter = cursor.set_range(key)
    while(iter != None and iter[0].find(key) == 0):
        # we're putting the string representation of the number here instead
        # of the actual integer since we have to encode it later, which
        # requires a string
        # i don't know if turning it to int makes the set interesection faster, though
        result_indices.add(iter[1].decode(UTF_8).split(":")[1])

        dup = cursor.next_dup()
        while(dup != None):
            result_indices.add(dup[1].decode(UTF_8).split(":")[1])
            dup = cursor.next_dup()
        iter = cursor.next()
    return result_indices

# Not sure if we are supposed to filter out the weird characters like &#10


def output(indices, output_type):

    # check if none in result indices
    for ind in indices:
        if ind == None:
            print("Okie dokie")
        else:
            print(ind)

    print("Output: \n")
    rows = []
    subjects = []
    dates = []
    froms = []
    to = []
    cc = []
    bcc = []
    body = []
    for index in indices:
        index = cre.set(index.encode(UTF_8))
        for i in index:
            string = str(i)

            r = re.split("<row>", string)
            if len(r) > 1:
                r = re.split("</row>", r[1])
                rows.append(r[0])
            s = re.split("<subj>", string)
            if len(s) > 1:
                s = re.split("</subj>", s[1])
                subjects.append(s[0])
            if output_type == VIEW_FULL:
                d = re.split("<date>", string)
                if len(d) > 1:
                    d = re.split("</date>", d[1])
                    dates.append(d[0])
                f = re.split("<from>", string)
                if len(f) > 1:
                    f = re.split("</from>", f[1])
                    froms.append(f[0])
                t = re.split("<to>", string)
                if len(t) > 1:
                    t = re.split("</to>", t[1])
                    to.append(t[0])
                c = re.split("<cc>", string)
                if len(c) > 1:
                    c = re.split("</cc>", c[1])
                    cc.append(c[0])
                bc = re.split("<bcc>", string)
                if len(bc) > 1:
                    bc = re.split("</bcc>", bc[1])
                    bcc.append(bc[0])
                b = re.split("<body>", string)
                if len(b) > 1:
                    b = re.split("</body>", b[1])
                    body.append(b[0])

    if output_type == VIEW_BRIEF:
        i = 0
        while (i < len(rows)):
            print("Row: " + rows[i])
            print("Subject: " + subjects[i])
            print("-"*50)
            i += 1
    elif output_type == VIEW_FULL:
        i = 0
        while (i < len(rows)):
            print("Row: " + rows[i] + "\n")
            print("Date: " + dates[i] + "\n")
            print("From: " + froms[i] + "\n")
            print("To: " + to[i] + "\n")
            print("Subject: " + subjects[i] + "\n")
            print("cc: " + cc[i] + "\n")
            print("bcc: " + bcc[i] + "\n")
            print("body: " + body[i] + "\n")
            print("-"*50)
            i += 1


def range_search(query):
    cursor = cda
    result = re.split(">=|<=|<|>", query)
    arg1 = result[0].strip()
    arg2 = result[1].strip()
    key = arg2.encode(UTF_8)
    result_indices = set()

    date = set()

    # >=
    if query.find(">=") != -1:
        itera = cursor.set(key)
        print("wrong way")
        exit()
    # <=
    elif query.find("<=") != -1:
        print("wrong way")
        exit()
    # >
    elif query.find(">") != -1:
        itera = cursor.set(key)
        if itera == None:
            return set()
        
        dup = cursor.next()
        while(True):
            if itera[0] == dup[0]:
                itera = dup
                dup = cursor.next()
            else:
                itera = dup
                break
        while(itera != None):
            result_indices.add(itera[1].decode(UTF_8).split(":")[1])
            itera = cursor.next()
        return result_indices
    # <
    elif query.find("<") != -1:
        itera = cursor.first()
        if itera == None:
            return set()

        date = itera[0].decode(UTF_8).split(":")[0]

        while(date < arg2):
            # print(itera[0])

            stuff = itera[1].decode(UTF_8).split(":")[1]
            result_indices.add(stuff)
            itera = cursor.next()
            if itera == None:
                break
            date = itera[1].decode(UTF_8).split(":")[0]

        return result_indices


'''
Returns a set of row_ids (string) based on a given key and cursor
'''


def range_search_helper(cursor, key):
        # todo: handle cases where key has % here
    result_indices = set()
    iter = cursor.set(key)
    while(iter != None and iter[0] == key):
                # we're putting the string representation of the number here instead
                # of the actual integer since we have to encode it later, which
                # requires a string
                # i don't know if turning it to int makes the set interesection faster, though
        result_indices.add(iter[1].decode(UTF_8).split(":")[1])

        dup = cursor.next_dup()
        while(dup != None):
            result_indices.add(dup[1].decode(UTF_8).split(":")[1])
            dup = cursor.next_dup()
        iter = cursor.next()
    return result_indices


"""
    Processes the proper queries and does the appropriate kind of search
    This function returns None if a grammatical error was found
    Grammatical errors include having more than one delimiter in the query
"""


def process_query(query, filtered_indices):
    # Test for range search
    result = re.split(">=|<=|<|>", query)
    if len(result) == 2:
        # do range search
        indices = set()
        indices = indices | range_search(query)
        if result[0].find("=") != -1:
            indices = process_query("date:" + result[1], filtered_indices)
            # todo: ranged search here


        if filtered_indices == None:
            return indices
        else:
            return indices & filtered_indices
    elif len(result) > 2:
        print("Grammatical error")
        return None
    
    # Test for equality searches
    result = query.split(":")
    if len(result) == 2:
        return equality_search(result, filtered_indices)
    elif len(result) == 1:
        # search on both subject and body
        result1 = process_query("subj:" + query, None)
        result1 |= process_query("body:" + query, None)
        if filtered_indices != None:
            result1 &= filtered_indices
        return result1
    else:
        print("Grammatical error")
        return None


"""
    Does equality search and partial search for email queries, term queries,
    and equality date queries
    If filtered indices is None, returns the resulting row ids from search
    If filtered indices is a set, returns the intersection between filtered_indices
        and the resulting row ids from search
"""


def equality_search(pair, filtered_indices):
        # todo: delete assertion to make things faster
    assert len(pair) == 2

    # don't need to lower here because we already lowered the characters at the start
    arg1 = pair[0].strip()
    arg2 = pair[1].strip()
    cursor = None
    key = None

    if arg1 in ("subj", "subject"):
        key = ("s-"+arg2).encode(UTF_8)
        cursor = cte
    elif arg1 == "body":
        key = ("b-"+arg2).encode(UTF_8)
        cursor = cte
    elif arg1 in ("to", "from", "bcc", "cc"):
        key = (arg1+"-"+arg2).encode(UTF_8)
        cursor = cem
    elif arg1 == "date":
        key = arg2.encode(UTF_8)
        cursor = cda

    # todo: delete for faster queries
    assert cursor != None
    assert key != None

    # result_indices is a set
    key_str = key.decode(UTF_8)
    wildcard_ind = key_str.find(WILDCARD_CHAR)
    if wildcard_ind == -1:
        result_indices = equality_search_helper(cursor, key)
    else:
        key_str = key_str[:wildcard_ind]
        key = key_str.encode(UTF_8)
        result_indices = partial_search(cursor, key)

    # for multiple searches
    if filtered_indices == None:
        filtered_indices = result_indices
    else:
        # set intersection here
        filtered_indices = filtered_indices & result_indices

    return filtered_indices


"""
    Returns a set of row_ids (string) based on a given key and cursor
"""


def equality_search_helper(cursor, key):
    # todo: handle cases where key has % here
    result_indices = set()
    iter = cursor.set(key)
    while(iter != None and iter[0] == key):
        # we're putting the string representation of the number here instead
        # of the actual integer since we have to encode it later, which
        # requires a string
        # i don't know if turning it to int makes the set interesection faster, though
        result_indices.add(iter[1].decode(UTF_8).split(":")[1])

        dup = cursor.next_dup()
        while(dup != None):
            result_indices.add(dup[1].decode(UTF_8).split(":")[1])
            dup = cursor.next_dup()
        iter = cursor.next()
    return result_indices


"""
    Checks if there's a delimiter in the given text
"""


def check_delimiter(text):
    for delim in DELIMITERS:
        val = text.find(delim)
        if val != -1:
            return val
    return -1


# reference: docs.python.org/3/howto/regex.html
date_pattern = re.compile("^date(>\=|<\=|:|>|<)\d{4}/\d{2}/\d{2}$")
email_pattern = re.compile("^(from|to|cc|bcc):(\w|\.)+@(\w|\.)+$")
term_pattern = re.compile("^(subj:|subject:|body:)?[\w]+[%]?$")

"""
    Checks if current query is valid based on query language grammar
"""


def is_query_valid(query):
    is_valid = date_pattern.match(query) != None
    is_valid |= email_pattern.match(query) != None
    is_valid |= term_pattern.match(query) != None
    return is_valid


def debug_print(message):
    if DEBUG:
        print(message)


"""
    This while-loop cleans up the input queries
    It divides up the input into single queries that process query can understand
    if each element was used as the query argument
"""


def cleanup_input(txt):
    queries = []
    ind = 0
    text_list = txt.split()
    list_len = len(text_list)
    current_query = ""

    while ind < list_len:
        curr_text = text_list[ind]
        current_query += curr_text
        delim_ind = check_delimiter(current_query)

        # the delimiter is at last
        if delim_ind == len(current_query) - 1:
            debug_print("Case 1: " + current_query)
            wild_ind = current_query.find("%")
            if wild_ind != -1 and delim_ind == wild_ind:
                # if that delim is % then check if valid: at last
                if is_query_valid(current_query):
                    queries.append(current_query)
                    ind += 1
                    current_query = ""
                    continue
            elif wild_ind != -1 and delim_ind != wild_ind:
                # if wild delim is not last: error
                # just go down
                pass
            else:
                # else, then check next text
                ind += 1
                continue
        elif delim_ind != -1:
            # delimiter is in between
            debug_print("Case 2: " + current_query)
            if is_query_valid(current_query):
                queries.append(current_query)
                ind += 1
                current_query = ""
                continue
        else:
            # there is no delimiter in current text
            debug_print("Case 3: " + current_query)
            if ind + 1 < list_len:
                debug_print("Case 3.1: " + current_query)
                # there is still a next term
                next_term = text_list[ind + 1]
                if check_delimiter(next_term) == -1:
                    # if next term has no delimiter
                    debug_print("Case 3.1.1: " + current_query)
                    if is_query_valid(current_query):
                        queries.append(current_query)
                        ind += 1
                        current_query = ""
                        continue
                elif next_term.find("%") != -1:
                    debug_print("Case 3.1.2: " + current_query)
                    if next_term == "%":
                        current_query += next_term
                        if is_query_valid(current_query):
                            queries.append(current_query)
                            ind += 2
                            current_query = ""
                            continue
                    else:
                        # grammatical error
                        pass
                elif next_term in DELIMITERS and ind + 2 < list_len:
                    debug_print("Case 3.1.3: " + current_query)
                    current_query += next_term + text_list[ind + 2]
                    if is_query_valid(current_query):
                        queries.append(current_query)
                        ind += 3
                        current_query = ""
                        continue
                else:
                    # delimiter is before last term and has other characters in
                    # SPECIAL CASE
                    debug_print("Case 3.1.4:")

                    # if first part contains special keywords then we don't add next term
                    first_part = re.split(" |:|>=|<=|<|>", next_term)[0]
                    if first_part in ("body", "subj", "subject", "cc", "bcc", "date", "from", "to"):
                        debug_print("Case 3.1.4.1: " + current_query)
                        ind += 1
                    else:
                        current_query += next_term
                        debug_print("Case 3.1.4.2: " + current_query)
                        ind += 2

                    if is_query_valid(current_query):
                        queries.append(current_query)
                        current_query = ""
                        continue
            elif is_query_valid(current_query):
                debug_print("Case 3.2: " + current_query)
                # there is no more terms left
                queries.append(current_query)
                ind += 1
                current_query = ""
                continue

        queries = None
        print("Grammatical error near " + curr_text)
        break

    return queries


def entering_command():
    global view

    clear_screen("Entering a command")

    if view == VIEW_FULL:
        print("View type: FULL")
    else:
        print("View type: BRIEF")

    txt = input("Command: ").lower()

    if (txt == "output=full"):
        view = VIEW_FULL
        print("Changing output to full...")
        entering_command()
        return
    elif (txt == "output=brief"):
        view = VIEW_BRIEF
        print("Changing output to full...")
        entering_command()
        return

    queries = cleanup_input(txt)

    if queries == None:
        return

    filtered_indices = None
    debug_print(queries)

    for query in queries:
        filtered_indices = process_query(query, filtered_indices)
        if filtered_indices == None:
            # an error happened somewhere
            return
    
    if filtered_indices != None:
        output(filtered_indices, view)
    else:
        print("No matching output.")

def main():
    main_menu()

def clear_screen(title):
    os.system('cls' if os.name=='nt' else 'clear')
    if title != None:
        print_title(title)

def print_title(title):
    print("-" * 20)
    print(title)
    print("-" * 20)
    

############ PART 3: MAIN PROGRAM ####################################################################
CODE_VER = 2

if CODE_VER == 2:
    main_menu()
        
elif CODE_VER == 1:
    while(True):
        os.system('cls' if os.name=='nt' else 'clear')

        # See function definition for description. Commented out to save time while testing.
        # main_menu(view)


        # The following code Splits up the entered query into a list of each word entered.
        # ***** CONSIDERS THAT THERE CAN BE ONLY ONE RANGED "DATE" CONDITION IN THE QUERY.
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
