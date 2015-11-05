from RoomReserve import *
from RoomReserve.helpers.linkList import linkList

@app.route("/admin")
@Login.login_required
def page_admin():

    title="Configuration"

    # This object stores the links that we want on the page
    links = linkList()

    links.add("/admin/users", "Users", bold=True)
    links.add("/admin/buildings", "Buildings", italics=True)
    links.add("/admin/rooms", "Rooms", bold=True, italics=True)

    return render('simpleMenuPage.html', title=title, links=links.getLinks())
