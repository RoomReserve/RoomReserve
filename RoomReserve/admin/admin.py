from RoomReserve import *
from RoomReserve.helpers.linkList import linkList

@app.route("/admin")
def page_admin():
    title="Configuration"
    links = linkList()
    links.add("/admin/users", "Users", bold=True)
    links.add("/admin/buildings", "Buildings", italics=True)
    links.add("/admin/rooms", "Rooms", bold=True, italics=True)

    return render('simpleMenuPage.html', title=title, links=links.getLinks())
