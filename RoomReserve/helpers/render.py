from RoomReserve import *

def render(template, *args, **kwargs):
    kwargs['appname']='RoomReserve0.1'
    kwargs['build'] = 'in development. Running on ' + sys.platform
    return render_template(template, *args, **kwargs)
