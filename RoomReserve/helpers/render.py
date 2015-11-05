from RoomReserve import *

import random

feelings = ["magic", "love", "happiness", "friendship", "smiles", "laughter"]

def render(template, *args, **kwargs):
    kwargs['withGlobals']=True
    kwargs['appname']='RoomReserve'
    kwargs['build'] = 'in development. Running on ' + sys.platform
    kwargs['feeling'] = feelings[random.randrange(0,len(feelings))]

    if current_user.is_authenticated:
        kwargs['current_user_name'] = current_user.getName()
        kwargs['current_user_email'] = current_user.getEmail()
        kwargs['current_user_role'] = current_user.getRole()

    return render_template(template, *args, **kwargs)
