from RoomReserve import *
from RoomReserve.admin.reservation import find_available_rooms, createReservation, getReservationByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.building import getBuildingById
from RoomReserve.admin.guest import getAllGuests, getGuest, createGuest
import re


class NewGuestForm(Form):
  firstname = StringField('First Name', validators=[DataRequired()])
  lastname = StringField('Last Name', validators=[DataRequired()])
  email = StringField('Email Address', validators=[DataRequired()])
  phone = StringField('Phone Number', validators=[DataRequired()])
  address = StringField('Address', validators=[DataRequired()])
  payment = StringField('Payment', validators=[DataRequired()])
  notes = TextAreaField('Notes')

@app.route('/reservation/new', methods=['GET', 'POST'])
@Login.standard_required
def page_newres():

  def pullAvailableRooms(itemlist):

    [capacity, indatey, indatem, indated, outdatey, outdatem, outdated] = itemlist

    indate = str(indatey) + "/" +  str(indatem) + "/" +  str(indated)
    outdate = str(outdatey) + "/" +  str(outdatem) + "/" +  str(outdated)
    indate = delorean.parse(indate).naive()
    outdate = delorean.parse(outdate).naive()

    availableRooms = find_available_rooms(indate, outdate, capacity=capacity)

    return availableRooms

  def allowEdit():
    '''
    Figures out if the current user should be allowed
    to edit the guest object.
    Parameters: GuestID for the guest we want to edit
    '''
    if current_user.is_standard():
      # Only admins and standard users can edit guests
      return True
    else:
      return False

  if request.method == 'POST':
    formdata = request.form
    indate = formdata['dates'].split()[0]
    outdate = formdata['dates'].split()[2]
    if formdata['capacity'] == "":
        capacity = 1
    else:
        capacity = int(formdata['capacity'])

    indate = delorean.parse(indate).naive()
    outdate = delorean.parse(outdate).naive()


    availableRooms = find_available_rooms(indate, outdate, capacity=capacity)
    if len(availableRooms) == 0:
      return render("basic.html", content="No rooms are available for selected capacity and date range. Try a different date range or try splitting the group into multiples.")
    firstroomid = availableRooms[0].getID()
    if formdata['newguestfirst'] != "" and formdata['newguestfirst'] != None:
      if formdata['guestID'] != "" and formdata['guestID'] != None:
        return render("basic.html", content="Tried to create new guest and use existing guest in same instance.")
      else:
        try:
          firstname = formdata['newguestfirst']
          lastname = formdata['newguestlast']
          email = formdata['newguestemail']

          phone = re.sub(r'[^\w]', '', formdata['newguestphone'])
          phone = int(phone)

          address = formdata['newguestaddress']

          payment = re.sub(r'[^\w]', '', formdata['newguestpayment'])
          try:
              payment = int(payment)
          except ValueError:
              payment = 0

          notes = formdata['newguestnotes']
        except Exception as e:
          print(e)
          return render("basic.html", content="An issue with new guest data occured.")

        myguest = createGuest(firstname, lastname, email, phone, address, payment, notes)
        if myguest == False:
          return render("basic.html", content="Could not create guest.")
        myguestid = myguest.get_id()
    elif formdata['guestID'] != "" and formdata['guestID'] != None:
      myguestid = int(formdata['guestID'])
      print("Got the guest (existing)")

    else:
      return render("basic.html", content="No guest selected")


    if 'roomselect' in formdata.keys():
      try:
        createReservation(guestID=myguestid, madeby=current_user.getID(), roomID=firstroomid, checkin=indate, checkout=outdate, status=CONST.unarrived_status)
      except:
        return render("basic.html", content="Could not complete reservation")

    else:
      try:
        myres = createReservation(guestID=myguestid, madeby=current_user.getID(), roomID=-1, checkin=indate, checkout=outdate, status=CONST.draft_status)
      except:
        return render("basic.html", content="Could not complete draft reservation")

      return render("roompick.html", resID = myres.getID(), rooms=availableRooms)
    return render("newReservation.html", pullAvailableRooms=pullAvailableRooms, getGuest=getGuest, allowEdit=allowEdit, guests=getAllGuests(), form=NewGuestForm(), successpage=True)


  return render("newReservation.html", pullAvailableRooms=pullAvailableRooms, getGuest=getGuest, allowEdit=allowEdit, guests=getAllGuests(), form=NewGuestForm())
