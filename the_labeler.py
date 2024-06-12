from flask import Flask, jsonify, flash, render_template, request, session, redirect
from datetime import datetime, timedelta
import random
import json
app = Flask(__name__)
from uuid import uuid4
app.secret_key=str(uuid4())#'Hot boogie nights'
################
## ENTRYPOINT ##
################
@app.route('/')
def index():
    s = """
    <html>
    <body>
    <a href="/sbs01">Side by Side application</a>
    </body>
    </html>
    """
    return s; 

@app.route('/query', methods=['GET', 'POST'])
def query_interface():
    
    if request.method == 'POST': 
        pd = str(request.get_data('params'))
        data = {}
        
    query_results = "RAd!"
    return render_template("queryI.html",
                           header_text="Query Interface",
                           query_results = query_results
    )
                        
@app.route('/sbs01', methods=['GET', 'POST'])
def sbs01():
    # parse post to string #

    debug_text = None;
    # TODO: This must be handled better by a framework method?
    if request.method == 'POST':
        pd = str(request.get_data('params'))
        data = {}
        for elt in pd.split('&'):
            k,v = elt.split('=')
            data[k] = v
        debug_text = json.dumps(data, indent=4)
    
    _lst = '''
        Yesterday I ate a lemon.
        Not a normal lemon, but one of those lemons
        that when you eat it
        you reflect on the state of life,
        the universe,
        and everything.
        A lemon thats 6*7.
    '''.split('\n')
    # have to split b/c flask escapes \n
    _rst = '''
        My esteemed coleauge would have you
        beleive that a lemon -- A lemon!
        Is six times seven.
        But when the dolphins left the ocean blue,
        they thanked us for the fish its true,
        and with their gratidude, said adieu.
        The knew mice were onto things more advanced
        than the size of a somewhat chubby man's pants.
    '''.split('\n')
    # randomize l/r
    if random.random() < .5:
        lst = _lst
        rst = _rst
    else:
        lst = _rst
        rst = _lst
    task_id = str(uuid4())
    return render_template("sbs.html",
                           header_text="LLM sbs v0.1",
                           lst=lst,
                           rst=rst,
                           task_id=task_id,
                           debug_text=debug_text)

