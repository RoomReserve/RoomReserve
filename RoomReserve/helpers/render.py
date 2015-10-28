from RoomReserve import *

import random

feelings = ["magic", "love", "happiness", "friendship", "smiles", "laughter"]

def render(template, *args, **kwargs):
    kwargs['withGlobals']=True
    kwargs['appname']='RoomReserve'
    kwargs['build'] = 'in development. Running on ' + sys.platform
    kwargs['feeling'] = feelings[random.randrange(0,len(feelings))]

    return render_template(template, *args, **kwargs)
