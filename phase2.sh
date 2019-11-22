# make the script executable: chmod +x phase2.sh
# run with ./phase2.sh
sort -u dates.txt > s_dates.txt
sort -u emails.txt > s_emails.txt
sort -u terms.txt > s_terms.txt
sort -u recs.txt > s_recs.txt

# from: docs.oracle.com/cd/E17276_01/html/api_reference/C/db_load.html
awk -F: '{print $1; print $0}' < s_recs.txt | sed 's/\\/\\\\/g' | db_load -c duplicates=1 -T -t hash re.idx
awk -F: '{print $1; print $0}' < s_terms.txt | sed 's/\\/\\\\/g' | db_load -c duplicates=1 -T -t btree te.idx
awk -F: '{print $1; print $0}' < s_emails.txt | sed 's/\\/\\\\/g' | db_load -c duplicates=1 -T -t btree em.idx
awk -F: '{print $1; print $0}' < s_dates.txt | sed 's/\\/\\\\/g' | db_load -c duplicates=1 -T -t btree da.idx