from cgi import escape
from json import dumps


def index(req):
    
    name = req.form.getfirst('argument', '')
    name = escape(name) # Escape the user input to avoid script injection attacks
    
    return dumps({"ws_code": "success", "number": len(name), "string": name, "bool": True})
    
