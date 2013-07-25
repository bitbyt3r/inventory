#!/usr/bin/python
import MySQLdb as mdb
import sys
import db
import platform
import os
import myExceptions

class Inventory: 
  
  

  def __enter__(self): 
    self.con = mdb.connect(db.server, db.user, db.password, db.database)
    self.cur = self.con.cursor(mdb.cursors.DictCursor) 

    

  def __exit__(self, type, value, traceback): 
    if self.con: 
      self.con.close() 
  

  #Add a new machine to the inventory. 
  def add(self, idtag, location='', model='', status='', hostname='', 
          service_tag='', mac_address='', discarded=False, description=''): 

    print idtag
    
    if self.cur.execute("select idtag from " + db.table + " where idtag=%s", (idtag)):
      raise myExceptions.DuplicateException() 
    
    else: 
      print idtag
      print location
      print model
      print status
      print hostname
      print service_tag
      print mac_address
      print discarded
      print description
      self.cur.execute("insert into " + db.table + "(idtag, location, model, " + 
                  "status, hostname, service_tag, mac_address, discarded, " +
                  "description) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                  (idtag, location, model, status, hostname, service_tag,
                   mac_address, discarded, description))


  #Get based on idtag
  def get(self, idtag): 
    self.cur.execute("select * from " + db.table + " where idtag=%s;", (idtag)) 
    info = self.cur.fetchone() 
    return info
  
  #WARNING, USE WITH CAUTION: 
  def delete(self, idtag): 
    self.cur.execute("delete from " + db.table + " where idtag=%s;", (idtag))
    
  def isValidTag(self, idtag): 
    if self.cur.execute("select idtag from " + db.table + " where idtag=%s", (idtag)): 
      raise myExceptions.DuplicateException()

    elif len(idtag) < 1 or len(idtag) > 8: 
      raise myExceptions.InvalidIDException() 
    
  def tagExists(self, idtag): 
    return self.cur.execute("Select idtag from " + db.table + " where idtag=%s;", (idtag))

    
  
