import fileinput
import xml.etree.ElementTree as ET
import sys
import re

# Run program with following command: >python3 phase1.py [XML file] 
def main():
    tree = ET.parse(sys.argv[1])    # XML element tree takes each section of XML file and organizes it as a tree where each section is an element (root, child, etc.)
    root = tree.getroot()
    get_terms(root)
    get_emails(root)
    get_dates(root)
    get_recs(root, sys.argv[1])

# Extract all terms (strings of consecutive alphanumeric, '-', and '_' characters with length > 2) and print to file
def get_terms(root):
    rows = []
    subj_lines = []     # contains lists of terms in each <subject> section, in the order to be written out
    body_lines = []     # contains lists of terms from each <body> section, in the order to be written out
    # Get each contents of <row> sections in XML file
    for element in root.iter("row"):
        rows.append(element.text)
    # Go through each <subject> section and get the terms
    for element in root.iter("subj"):
        if element.text != None:            # Access the contents of section using element.text attribute (check that it's not None so that empty rows won't be in output)
            txt = element.text.lower()      # Convert all characters from section to lowercase
            txt = re.split(r'[^a-z0-9_\-]', txt)     # Split on all invalid characters
            i = 0
            while i < len(txt):
                if len(txt[i]) < 3:     # If term length is less than 3, remove from output list
                    txt.remove(txt[i])
                else:
                    i += 1
        else:
            txt = None
        subj_lines.append(txt)
    # Get terms from each <body> section
    for element in root.iter("body"):
        if element.text != None:
            txt = element.text.lower()      # Convert all characters from section to lowercase
            txt = re.split(r'[^a-z0-9_\-]', txt)     # Split on all invalid characters
            i = 0
            while i < len(txt): 
                if len(txt[i]) < 3:     # If term length is less than 3, remove from output list
                    txt.remove(txt[i])
                else:
                    i += 1
        else:
            txt = None
        body_lines.append(txt)

    size = len(rows)
    outfile = open("terms.txt", "w")    # Write output to the file "terms.txt"
    for i in range(size):               # for loop to ensure each section is printed in order
        try:
            length = len(subj_lines[i])
        except:
            length = 0
        for j in range(length):         # for loop to ensure each term from section is printed in the right order
            if subj_lines[i] != None:
                outfile.write("s-"+subj_lines[i][j]+":"+rows[i]+"\n")
        try:
            length = len(body_lines[i])
        except:
            length = 0
        for j in range(length):
            if body_lines[i] != None:
                outfile.write("b-"+body_lines[i][j]+":"+rows[i]+"\n")
    outfile.close()

# Extract the contents of every from, to, cc, and bcc section of XML file and write to file
def get_emails(root):
    rows = []
    from_lines = []
    to_lines = []
    cc_lines = []
    bcc_lines = []
    # Get each row
    for element in root.iter("row"):
        rows.append(element.text)
    # Get the email address of each sender
    for element in root.iter("from"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')   
        else:
            txt = None
        from_lines.append(txt)
    # Get email addresses of recipient(s)
    for element in root.iter("to"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')        # Only split on commas so that there is one email address per line in output file
        else:
            txt = None
        to_lines.append(txt)
    # Get email addresses in each cc section
    for element in root.iter("cc"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')
        else:
            txt = None
        cc_lines.append(txt)
    # Get email addresses in each bcc section
    for element in root.iter("bcc"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')
        else:
            txt = None
        bcc_lines.append(txt)

    size = len(rows)
    outfile = open("emails.txt", 'w')
    # write to output file
    for i in range(size):
        if from_lines[i] != None:
            length = len(from_lines[i])
            for j in range(length):
                outfile.write("from-"+from_lines[i][j]+":"+rows[i]+"\n")
        if to_lines[i] != None:
            length = len(to_lines[i])
            for j in range(length):
                outfile.write("to-"+to_lines[i][j]+":"+rows[i]+"\n")
        if cc_lines[i] != None:
            length = len(cc_lines[i])
            for j in range(length):
                outfile.write("cc-"+cc_lines[i][j]+":"+rows[i]+"\n")
        if bcc_lines[i] != None:
            length = len(bcc_lines[i])
            for j in range(length):
                outfile.write("bcc-"+bcc_lines[i][j]+":"+rows[i]+"\n")
    outfile.close()

# Extract the dates that each email was sent and write to output file
def get_dates(root):
    rows = []
    dates = []
    # Gets rows
    for element in root.iter("row"):
        rows.append(element.text)
    # Gets dates
    for element in root.iter("date"):
        if element.text != None:
            txt = element.text
        else:
            txt = None
        dates.append(txt)

    size = len(rows)
    outfile = open("dates.txt", 'w')
    # Write to output file
    for i in range(size):
        if dates[i] != None:
            outfile.write(dates[i]+":"+rows[i]+"\n")
    outfile.close()

# Extract the full contents of each email.
# Uses element tree to get the rows and reads in the whole XML file to get contents of each email.
# (one email = one string)
def get_recs(root, inputfile):
    infile = open(inputfile, 'r')
    lines = infile.readlines()
    lines.pop(len(lines)-1)
    lines.pop(0)
    lines.pop(0)
    rows = []
    for element in root.iter("row"):
        rows.append(element.text)
    size = len(rows)
    outfile = open("recs.txt", 'w')
    for i in range(size):
        outfile.write(rows[i]+":"+lines[i])
    infile.close()
    outfile.close()

main()







