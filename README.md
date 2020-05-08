# Mavis
A simple python beacon website

## Use Cases
The main reason to use this is if you're sending an email, or providing a specific webpage for a client and you need to know if the client has viewed it. You can just generate a beacon, embed it in either the page or an HTML based email. When the image is requested, the IP of the requestor will be logged on the Control Panel for you to view. There are some limitations in this method, due to caching and snooping governments/ISPs, as well as email clients serving images themselves rather than direct links, but in general this will provide you with a method to see if the page has been viewed.

## Installation
The only things required for this tool are Python3 and flask (via pip3 install flask).

## Running
   python site.py
   
## End points

### Control Panel
You can add new beacons, view old beacons, visit the beacon and remove beacons. If using '/all/', you can also see removed beacons. If you have viewed your own beacon on your current IP address, this will be highlighted for you.

localhost:5000/

localhost:5000/all/

### Adding Beacons
Adds a new beacon with the specified ID. This can be done on the Control Panel page. Note though that these beacons are randomly generated. If you need a specific ID you need to use the URL below.
  
  localhost:5000/add/[beaconID]/
  
### Viewing Beacons
Loads a transparent png if beacon exists, or a blank page if it doesn't. This is the payload that should be on a given page or in an html based email. Clicking the Beacon ID in the Control Panel will load this page.

  localhost:5000/[beaconID]/sig.png
  
### Removing Beacons
Removes the beacon with the specified ID. This can also be done from the Control Panel.

  localhost:5000/remove/[beaconID]
