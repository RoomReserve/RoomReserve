from RoomReserve import *

def render(template, *args, **kwargs):
    kwargs['withGlobals']=True
    kwargs['appname']='RoomReserve'
    kwargs['build'] = 'in development. Running on ' + sys.platform
    return render_template(template, *args, **kwargs)
