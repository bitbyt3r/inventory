#!/usr/bin/python
import _mysql
import sys
import db

try:
  con = _mysql.connect(db.server, db.user, db.password, db.database)
        
  con.query("SELECT VERSION()")
  result = con.use_result()
    
  print "MySQL version: %s" % result.fetch_row()[0]
    
except _mysql.Error, e:
  
  print "Error %d: %s" % (e.args[0], e.args[1])
  sys.exit(1)

finally:
  if con:
    con.close()

def validCode(code):
  return True

barcode = raw_input(":")
while validCode(barcode):
  try:
    con = _mysql.connect(db.server, db.user, db.password, db.database)

    con.query("insert into %s set idtag=%s" % (db.table, barcode))
  except _mysql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
  finally:
    if con:
      con.close()

  barcode = raw_input(":")
