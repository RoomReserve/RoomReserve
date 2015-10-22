# Holds links for simpleMenuPage(s)

# ::Sample usage::
# @app.route("/admin")
# def page_admin():
#     title="Configuration"
#     links = linkList()
#     links.add("/admin/users", "Users", bold=True)
#     links.add("/admin/buildings", "Buildings", italics=True)
#     links.add("/admin/rooms", "Rooms", bold=True, italics=True)
#     return render_template('simpleMenuPage.html', title=title, links=links.getLinks())

class linkList():
    links = []
    def __init__(self):
        self.links = []

    def add(self, url, title, bold=False, italics=False):
        # Required parameters: url, title
        # Optional parameters: bold, italics (boolean)
        self.links.append(linkItem(url,title,bold,italics))

    def getLinks(self):
        return self.links



class linkItem():
    url = ""
    title = ""
    bold = False
    italics = False
    def __init__(self,url,title, bold, italics):
        self.url = url
        self.title = title
        self.bold = bold
        self.italics = italics
