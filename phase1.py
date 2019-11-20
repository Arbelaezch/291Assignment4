import fileinput
import xml.etree.ElementTree as ET
import sys
import re

# Run program with following command: python3 phase1.py [xml file] 
def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    get_terms(root)
    get_emails(root)
    get_dates(root)
    get_recs(root, sys.argv[1])

def get_terms(root):
    rows = []
    subj_lines = []
    body_lines = []
    for element in root.iter("row"):
        rows.append(element.text)
    for element in root.iter("subj"):
        if element.text != None:
            txt = element.text.lower()
            txt = re.split(r'[^a-zA-Z0-9_\-]', txt)
            i = 0
            while i < len(txt):
                if len(txt[i]) < 3:
                    txt.remove(txt[i])
                else:
                    i += 1
        else:
            txt = None
        subj_lines.append(txt)
    for element in root.iter("body"):
        if element.text != None:
            txt = element.text.lower()
            txt = re.split(r'[^a-zA-Z0-9_\-]', txt)
            i = 0
            while i < len(txt):
                if len(txt[i]) < 3:
                    txt.remove(txt[i])
                else:
                    i += 1
        else:
            txt = None
        body_lines.append(txt)

    size = len(rows)
    outfile = open("terms.txt", "w")
    for i in range(size):
        try:
            length = len(subj_lines[i])
        except:
            length = 0
        for j in range(length):
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

def get_emails(root):
    rows = []
    from_lines = []
    to_lines = []
    cc_lines = []
    bcc_lines = []
    for element in root.iter("row"):
        rows.append(element.text)
    for element in root.iter("from"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')
        else:
            txt = None
        from_lines.append(txt)
    for element in root.iter("to"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')
        else:
            txt = None
        to_lines.append(txt)
    for element in root.iter("cc"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')
        else:
            txt = None
        cc_lines.append(txt)
    for element in root.iter("bcc"):
        if element.text != None:
            txt = element.text.lower()
            txt = txt.split(',')
        else:
            txt = None
        bcc_lines.append(txt)

    size = len(rows)
    outfile = open("emails.txt", 'w')
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

def get_dates(root):
    rows = []
    dates = []
    for element in root.iter("row"):
        rows.append(element.text)
    for element in root.iter("date"):
        if element.text != None:
            txt = element.text
        else:
            txt = None
        dates.append(txt)

    size = len(rows)
    outfile = open("dates.txt", 'w')
    for i in range(size):
        if dates[i] != None:
            outfile.write(dates[i]+":"+rows[i]+"\n")
    outfile.close()

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







