#!/usr/bin/python
import whiptail
import inventory
import sys
import myExceptions 

#To get a dell service tag from the linux command line, run as root: 
#dmidecode -s system-serial-number

inv = inventory.Inventory() 
whip = whiptail.Whiptail() 


################################################################################
# Shows the main menu and returns the value of the menu option chosen. 
################################################################################
def showMenu(): 
    return whip.menu("Pick an option.", ("Add new tag", "Batch add", 
                                         "Look up a tag", "Edit a Tag", 
                                         "Delete a Tag", "quit"))

################################################################################
# adds a single tag to the inventory system.
################################################################################
def addNewTag(inv): 
    try: 
        idtag = whip.prompt("Enter ID Tag") 
        
        #Validate the tag and check for duplicates. 
        #Exceptions can be thrown here. 
        inv.isValidTag(idtag)
        inv.isDuplicateTag(idtag) 

        # Ask for everything else. 
        location = whip.prompt("Enter Location") 
        model = whip.prompt("Enter Model") 
        status = whip.menu("Pick an option: ", 
                           ("In Storage", "Installed", "Removed"))
        hostname = whip.prompt("Enter Hostname") 
        service_tag = whip.prompt("Enter Service Tag") 
        mac_address = whip.prompt("Enter Mac Address") 
        discarded = whip.confirm("Discarded?", 'no')
        description = whip.prompt("Description")
    
        # Add the tag
        inv.add(idtag, location, model, status, hostname, service_tag, 
                mac_address, discarded, description)
        whip.alert("Added successfully.") 

    except myExceptions.DuplicateException:  
        whip.alert("Duplicate Tag") 
    except myExceptions.InvalidIDException: 
        whip.alert("Tag too long") 
    except myExceptions.CancelledException: 
        whip.alert("Operation Cancelled") 
    except ValueError: 
        whip.alert("Invalid Characters in Tag") 
    
    
################################################################################
# add a bunch of tags to the inventory system. Asks for everything except for 
# ID Tag and Service tag ahead of time. 
################################################################################
def batchAdd(inv): 
    try: 
        #Get all the generic information. 
        location = whip.prompt("Enter Location") 
        model = whip.prompt("Enter Model") 
        status = whip.menu("Pick an option: ", ("In Storage", "Installed", "Removed"))
        hostname = whip.prompt("Enter Hostname") 
        discarded = whip.confirm("Discarded?", 'no')
        description = whip.prompt("Description")
        
        
        idtag="" 
        whip.alert("enter \"quit\" to exit.")
        
        while idtag.lower() != "quit": 
            try: 
                idtag = whip.prompt("Enter ID Tag")     
                inv.isValidTag(idtag)
                inv.isDuplicateTag(idtag)
                
                service_tag = whip.prompt("Enter Service Tag") 
                
                inv.add(idtag, location, model, status, hostname, service_tag, 
                        mac_address, discarded, description)
                
                whip.alert("Added successfully") 
                
            except myExceptions.DuplicateException: 
                whip.alert("Duplicate Tag") 
            except myExceptions.InvalidIDException: 
                whip.alert("Invalid ID tag") 
    except myExceptions.CancelledException: 
        whip.alert("Operation Cancelled")            
            


################################################################################
# Look up a tag in the inventory system. 
################################################################################
def tagLookup(inv): 
    
    try: 
        idtag = whip.prompt("Enter an ID Tag") 
        try: 
            asset = inv.get(idtag) 
            
            if asset['discarded'] == 1: 
                asset['discarded'] = "yes"
            else: 
                asset['discarded'] = "no" 
                
            #This is ugly as sin. Basically the %-12s keeps the titles of the 
            #information lined up nicely. Then the {0}... is used to actually
            #insert the information. 
                info = """%-12s {0} 
%-12s {1}
%-12s {2} 
%-12s {3} 
%-12s {4} 
%-12s {5} 
%-12s {6} 
%-12s {7} 
%-12s {8} 
""".format(idtag, asset['location'], asset['model'], asset['status'], 
           asset['hostname'], asset['service_tag'], asset['mac_address'], 
           asset['discarded'], 
           asset['description']) % ("ID Tag:", "Location:", "Model:", "Status:",
                                    "Hostname:", "Service Tag:", "Mac Address:",
                                    "Discarded:", "Description:")
            # Give the user the information back. 
            whip.alert(info)
        except myExceptions.NonexistentTag: 
            whip.alert("Tag does not exist") 
    except myExceptions.CancelledException: 
        whip.alert("Operation Cancelled")
        
           
################################################################################
# Delete a tag from the inventory system
################################################################################
def delete(inv): 
    try: 

        idtag = whip.prompt("Enter an ID Tag to Delete")
        
        #First, make sure the tag exists. Alert the user if it doesn't. 
        if not inv.tagExists(idtag):
            whip.alert("Tag does not exist") 
             
        # Otherwise, give the user a chance to change their mind and...
        else: 
            sure = whip.confirm("Are you sure you want to delete %s?" % idtag)
            if sure: 
                
                #...finally, delete the tag. 
                inv.delete(idtag)
                whip.alert("Deleted Successfully") 
            else: 
                whip.alert("Cancelled") 
    except myExceptions.CancelledException: 
        whip.alert("Operation Cancelled") 


################################################################################
# Edit a tag. Has the user scan the tag and then asks which fields to edit. 
################################################################################
def edit(inv): 
    try: 
        # Ask the user for an ID tag: 
        idtag = whip.prompt("Enter an ID tag to edit:") 
        
        
        options = ("Location", "Model", "Status", "Hostname", "Service Tag", 
                   "Mac Address", "Discarded", "Description")
        
        try: 
            # Get existing values from the database: 
            new = inv.get(idtag)
            
            toEdit = whip.checklist("Pick options to edit: ", options)
            
            for item in toEdit: 
                key = item.lower().replace(" ", "_")
                if key == "discarded": 
                    newValue = whip.confirm("Discarded?", new[key])
                    new[key] = newValue
                elif key == "status": 
                    newValue = whip.menu("Pick an option: ", ("In Storage", "Installed", "Removed"), new[key])
                    new[key]= newValue
                else:
                    newValue = whip.prompt("Enter new value for %s." % item, new[key])
                    new[key] = newValue
                
            inv.edit(idtag, new)
                
            whip.alert("Completed Succsesfully") 
        
        except myExceptions.NonexistentTag: 
            whip.alert("Tag does not exist") 
            
    except myExceptions.CancelledException: 
        whip.alert("Operation Cancelled") 
            
    
################################################################################
# Main. Nothing terribly fancy here.
################################################################################
def main(): 
    try: 
        #Initilize the inventory object. 
        inv = inventory.Inventory() 
        
        #This is where the magic happens. At the beginning of this, the __enter__()
        #function is called, and at the end, __exit__() is called.
        with inv: 
            result = ""
            while result != "quit": 
                result = showMenu()
                if result == "Add new tag": 
                    addNewTag(inv)
                elif result == "Batch add": 
                    batchAdd(inv) 
                elif result == "Look up a tag": 
                    tagLookup(inv) 
                elif result == "Edit a Tag": 
                    edit(inv)
                elif result == "Delete a Tag": 
                    delete(inv)
                elif result == "quit": 
                    sys.exit(0) 

    except myExceptions.CancelledException: 
        print "Bye" 
        sys.exit(0)
    except ImportError: 
        print "You are missing the MySQLdb module for pytyhon." 
        print "Please install the MySQLdb module and try again." 

                
                
main() 
