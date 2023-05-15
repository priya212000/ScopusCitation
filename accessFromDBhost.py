import mysql.connector as connector
import CitationRetrieval

from datetime import datetime
currDate = datetime.now().strftime('%B')+"_"+str(datetime.now().year)

database = connector.connect(host='citations.clqyzvodepst.us-east-1.rds.amazonaws.com',database='citations',user='admin',password='adminroot')
cursor=database.cursor()

cursor.execute('select orcid from report')
ids=cursor.fetchall()
orcids=[]
for i in ids:
    orcids.append(i[0])

cursor.execute('desc report')
ret=cursor.fetchall()
avail=[]
for i in ret:
    avail.append(i[0])

if currDate not in avail:
    cursor.execute('alter table report add column '+currDate+' VARCHAR(45)')
    for i in orcids:
        cursor.execute('update report set '+currDate+' = \''+str(CitationRetrieval.citeCount(i))+'\' where orcid = \''+i+'\'')
else:
    for i in orcids:
        cursor.execute('update report set '+currDate+' = \''+str(CitationRetrieval.citeCount(i))+'\' where orcid = \''+i+'\'')