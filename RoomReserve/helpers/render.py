from RoomReserve import *

import random

#Feelings used at the bottom of the page. (Made with __ at Luther College)
feelings = ["magic", "love", "happiness", "friendship", "smiles", "laughter", "care"]

def render(template, *args, **kwargs):
    # Adds more variables to kwargs for the template
    # before rendering the template

    kwargs['withGlobals']=True
    kwargs['appname']='RoomReserve'
    kwargs['build'] = 'in development. Running on ' + sys.platform
    kwargs['feeling'] = feelings[random.randrange(0,len(feelings))]

    if current_user.is_authenticated:
        # Pass along some user information if the user is logged in.
        kwargs['current_user_name'] = current_user.getName()
        kwargs['current_user_email'] = current_user.getEmail()
        kwargs['current_user_role'] = current_user.getRole()
        kwargs['current_user_id'] = current_user.getID()

    return render_template(template, *args, **kwargs)
