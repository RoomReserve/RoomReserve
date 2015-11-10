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

    def add(self, url, title, fa_icon="none", bold=False, italics=False):
        # Required parameters: url, title
        # Optional parameters: fa_icon (font-awesome icon), bold, italics (boolean)
        self.links.append(linkItem(url,title,fa_icon,bold,italics))

    def getLinks(self):
        return self.links



class linkItem():
    url = ""
    title = ""
    fa_icon = "none"
    bold = False
    italics = False

    def __init__(self,url,title, fa_icon, bold, italics):
        self.url = url
        self.title = title
        self.fa_icon = fa_icon
        self.bold = bold
        self.italics = italics
