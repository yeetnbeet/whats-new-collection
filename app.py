import lib
import os
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def index():
    newp = lib.products_from_month_ago(lib.get_month_ago())
    oldp = lib.older_products(lib.get_month_ago())
    lib.add_new_products(newp)
    lib.remove_old_products(oldp)
    return "<p> Removed: "+str(len(oldp))+" Added: "+str(len(newp))+"</p>"

@app.route("/pepe",methods=["GET"])
def pepe():
    filename = 'pepe-tea.gif'
    return send_file(filename, mimetype='image/gif')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)