#!/usr/bin/python
import MySQLdb as mdb
import sys
import db
import platform
import os

NAME = platform.system() 

################################################################################
def getID(): 
  id = raw_input("ID> ") 
  try: 
    int(id)
    return id
  except ValueError: 
    return False
    
################################################################################
  
#Open the database connection. 
con = mdb.connect(db.server, db.user, db.password, db.database)

with con: 
  
  cur = con.cursor()

  while True: 
  
    #Read in the code: 
    id = getID() 
    

    if id != False: 
      # Check for a duplicate tag. If it's duplicate, don't put it in. 
      if cur.execute("select idtag from " + db.table + " where idtag=%s", (id)):
        print "Duplicate tag." 
        if NAME == "Linux": 
          os.system("""spd-say "Rejected tag" """)
        elif NAME == "Darwin": 
          os.system("say Rejected tag") 

      else: 
        #insert into the database. 
        cur.execute("insert into " + db.table + "(idtag) values(%s);", (id))

    else: 
      print "invalid input!"
      
   
