#!/usr/bin/python
import whiptail
import inventory
import sys
import myExceptions 

inv = inventory.Inventory() 
whip = whiptail.Whiptail() 

def showMenu(): 
    return whip.menu("Pick an option.", ("Add new tag", "Batch add", "Look up a tag", "Delete a Tag", "quit"))


def addNewTag(inv): 
    try: 
        idtag = whip.prompt("Enter ID Tag") 
        
        #Validate the tag and check for duplicates. Exceptions can be thrown here. 
        inv.isValidTag(idtag)

        location = whip.prompt("Enter Location") 
        model = whip.prompt("Enter Model") 
        status = whip.menu("Pick an option: ", ("In Storage", "Installed", "Removed"))
        hostname = whip.prompt("Enter Hostname") 
        service_tag = whip.prompt("Enter Service Tag") 
        mac_address = whip.prompt("Enter Mac Address") 
        discarded = whip.confirm("Discarded?", 'no')
        description = whip.prompt("Description")
    
        inv.add(idtag, location, model, status, hostname, service_tag, 
                mac_address, discarded, description)
        whip.alert("Added successfully.") 

    except myExceptions.DuplicateException:  
        whip.alert("Duplicate Tag") 
    except myExceptions.InvalidIDException: 
        whip.alert("Invalid Tag") 
    except myExceptions.CancelledException: 
        whip.alert("Operation Cancelled") 
    
    

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
            



def tagLookup(inv): 
    idtag = whip.prompt("Enter an ID Tag") 
    asset = inv.get(idtag) 
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
                                    "Discarded", "Description:")
    whip.alert(info)


def delete(inv): 
    idtag = whip.prompt("Enter an ID Tag to Delete")
    if not inv.tagExists(idtag):
        whip.alert("Tag does not exist") 
    else: 
        sure = whip.confirm("Are you sure you want to delete %s?" % idtag)
        if sure: 
            inv.delete(idtag)
            whip.alert("Deleted Successfully") 
        else: 
            whip.alert("Cancelled") 
            
    


def main(): 
    inv = inventory.Inventory() 
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
            elif result == "Delete a Tag": 
                delete(inv)
            elif result == "quit": 
                sys.exit(0) 
                
                
main() 
