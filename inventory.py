#!/usr/bin/python
import MySQLdb as mdb
import sys
import db
import platform
import os
import myExceptions

class Inventory: 
  
  

  def __enter__(self): 
    try: 
      self.con = mdb.connect(db.server, db.user, db.password, db.database)
      self.cur = self.con.cursor(mdb.cursors.DictCursor) 
    except ImportError: 
      print "You are missing the MySQLdb module for pytyhon." 
      print "Please install the MySQLdb module and try again." 
 

    

  def __exit__(self, type, value, traceback): 
    if self.con: 
      self.con.close() 
  

  #Add a new machine to the inventory. 
  def add(self, idtag, location='', model='', status='', hostname='', 
          service_tag='', mac_address='', discarded=False, description=''): 

    if self.cur.execute("select idtag from " + db.table + " where idtag=%s", (idtag)):
      raise myExceptions.DuplicateException() 
    
    else: 
      service_tag = service_tag.upper() 

      self.cur.execute("insert into " + db.table + "(idtag, location, model, " + 
                  "status, hostname, service_tag, mac_address, discarded, " +
                  "description) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                  (idtag, location, model, status, hostname, service_tag,
                   mac_address, discarded, description))



  #Edit a machine in the inventory. Takes a dictionary.
  def edit(self, idtag, newValues): 
    
    newValues['service_tag'] = newValues['service_tag'].upper()
    
    self.cur.execute("update " + db.table + " set location=%s, model=%s, " + 
                     "status=%s, hostname=%s, service_tag=%s, mac_address=%s,"+ 
                     " discarded=%s, " +
                     "description=%s where idtag=%s;", 
                     (newValues['location'], newValues['model'], 
                      newValues['status'], newValues['hostname'], 
                      newValues['service_tag'], newValues['mac_address'], 
                      newValues['discarded'], newValues['description'], idtag))
    
  #Get based on idtag
  def get(self, idtag):
    if self.cur.execute("select * from " + db.table + " where idtag=%s;", (idtag)):
      info = self.cur.fetchone() 
      return info
    else: 
      raise myExceptions.NonexistentTag()
  
  #WARNING, USE WITH CAUTION: 
  def delete(self, idtag):
    self.cur.execute("delete from " + db.table + " where idtag=%s;", (idtag))

  def isDuplicateTag(self, idtag):
    if self.cur.execute("select idtag from " + db.table + " where idtag=%s", (idtag)): 
      raise myExceptions.DuplicateException()

  def isValidTag(self, idtag):
    int (idtag)
    if len(idtag) < 1 or len(idtag) > 8: 
      raise myExceptions.InvalidIDException() 
    
  def tagExists(self, idtag):
    return self.cur.execute("Select idtag from " + db.table + " where idtag=%s;", (idtag))

  def getID(self, service_tag):
    self.cur.execute("Select * from " + db.table + " where service_tag=%s;", (service_tag))
    return self.cur.fetchone()['idtag']
