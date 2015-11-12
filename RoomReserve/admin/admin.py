from RoomReserve import *
from RoomReserve.helpers.linkList import linkList

@app.route("/admin")
@login_required
def page_admin():

    title="Configuration"

    # This object stores the links that we want on the page
    links = linkList()

    links.add("/admin/users", "Users", fa_icon="fa-user")
    links.add("/admin/buildings", "Buildings", fa_icon="fa-building")
    links.add("/admin/rooms", "Rooms", fa_icon="fa-home")

    return render('simpleMenuPage.html', title=title, links=links.getLinks())
