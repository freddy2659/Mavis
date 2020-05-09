# pip3 install flask

from flask import Flask, render_template, send_from_directory, send_file, request, redirect
from model import *
import cfg

app = Flask(__name__, static_url_path='', static_folder='web/static', template_folder='web/templates')


@app.route('/add/<beaconID>/')
@app.route('/add/<beaconID>/<ref>/')
def create(beaconID, ref=None):
    ip_add = getIP(request)
    ref = getReferer(ref, request)
    if beaconID in b.dict:
        print("Beacon already exists")
        return create(beaconID + 1, ref)  # This is a recursive call, it's already saved the pickle
    b.addBeacon(beaconID)
    if beaconID in b.dict:
        print("Added beacon")
        cfg.save_pickle(b)
        return redirect(ref, code=303)
    else:
        print("Failed to add beacon")
        return "<html><head></head><body>Failed to create Beacon.</body></html>"
        
@app.route('/')
def read(all=False):
    ip_add = getIP(request)
    return  render_template('stats.html', dict = b.dict, sig = b.sig, thisip = ip_add, all = all)
    
@app.route('/all/')
def read_all():
    return  read(True)
    
@app.route('/<beaconID>/<img>')
def update(beaconID, img):
    if beaconID in b.dict and b.dict[beaconID].isEnabled():
        ip_add = getIP(request)
        b.dict[beaconID].visit(ip_add)
        cfg.save_pickle(b)
        return send_from_directory('web/static', img)
    else:
        return " "  # This could also return a default company signature instead
        
@app.route('/remove/<beaconID>/')
@app.route('/remove/<beaconID>/<ref>/')
def delete(beaconID, ref=None):
    ref = getReferer(ref, request)
    if beaconID in b.dict and b.dict[beaconID].isEnabled():
        b.dict[beaconID].remove()
        cfg.save_pickle(b)
        print(f"Beacon {beaconID} marked as disabled")
    else:
        print(f"Beacon {beaconID} doesn't exist, or is already disabled")
    return redirect(ref, code=303)
    
# This function is reasonably robust in attempting to get the IP of the requests origin
def getIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        return request.environ.get('HTTP_X_FORWARDED_FOR')
    elif 'HTTP_X_REAL_IP' in request.environ:
        return request.environ.get('HTTP_X_REAL_IP')
    elif 'REMOTE_ADDR' in request.environ:
        return request.environ.get('REMOTE_ADDR')
    elif request.remote_addr is not None and request.remote_addr != "":
        return request.remote_addr
    else:
        print("WARNING: There was no IP address in the request!")
        return "UNKNOWN"
        
# This function will attempt to get the referer for the URL. It will use the provided urlRef, then the 
#   headerRef and fall back to '/' if it cannot find either. It will warn if there is a mismatch between
#   urlRef and headerRef.
def getReferer(urlRef, request):
    headerRef = request.environ.get('HTTP_REFERER')
    if headerRef is None:
        # This could occur from visiting the page directly, weird redirects, browsers that don't provide
        #   the header, someone guessing pages etc.
        if urlRef is None:
            print("WARNING: Referer was none")
            return "/"
        return f"/{urlRef}"
    else:
        if urlRef is None:
            return headerRef
        else:
            if headerRef.endswith(urlRef) or headerRef.endswith(f"{urlRef}/"):
                return f"/{urlRef}"
            else:
                print("WARNING: HeaderRef and URLRef don't match!")
                return f"/{urlRef}"
                
if __name__ == '__main__':
    b = None
    if cfg.use_pickle():
        b = cfg.load_pickle()
    if cfg.use_sql():
        b = cfg.load_sql(b)
    if b is None:
        b = Beacons('sig.png')
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    
    