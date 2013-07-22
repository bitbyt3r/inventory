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
    if len(id) > 8:
      print "invalid tag!"
      if NAME == "Linux": 
        os.system("""spd-say "Invalid Tag" """)
      elif NAME == "Darwin": 
        os.system("say Invalid Tag")       
      return False
    return id
  except ValueError: 
    print "invalid Input."
    if NAME == "Linux": 
      os.system("""spd-say "Invalid Input" """)
    elif NAME == "Darwin": 
      os.system("say Invalid Input")       
    return False
    
################################################################################
  
#Open the database connection. 
con = mdb.connect(db.server, db.user, db.password, db.database)

with con: 
  
  cur = con.cursor()

  while True: 
  
    #Read in the code: 
    if id:
      lastID = id
    id = getID() 
    if lastID == id:
      print "Rescan"
      if NAME == "Linux": 
        os.system("""spd-say "Rescan" """)
      elif NAME == "Darwin": 
        os.system("say Rescan")             
      continue
    

    if id != False: 
      # Check for a duplicate tag. If it's duplicate, don't put it in. 
      if cur.execute("select idtag from " + db.table + " where idtag=%s", (id)):
        print "Duplicate tag." 
        if NAME == "Linux": 
          os.system("""spd-say "Duplicate tag" """)
        elif NAME == "Darwin": 
          os.system("say Duplicate tag") 

      else: 
        #insert into the database. 
        cur.execute("insert into " + db.table + "(idtag) values(%s);", (id))      
        print "Tag Accepted." 
        if NAME == "Linux": 
          os.system("""spd-say "Tag Accepted." """)
        elif NAME == "Darwin": 
          os.system("say Tag Accepted") 
   
