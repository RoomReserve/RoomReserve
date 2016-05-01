from RoomReserve import *
from RoomReserve.admin.reservation import find_available_rooms, createReservation, getReservationByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.building import getBuildingById
from RoomReserve.admin.guest import getAllGuests, getGuest


class NewGuestForm(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    payment = StringField('Payment', validators=[DataRequired()])
    notes = TextAreaField('Notes')

@app.route('/reservation/new/', methods=['GET', 'POST'])
@Login.standard_required
def page_newres():
  def pullAvailableRooms(capacity, indate, outdate):
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
    
  return render("newReservation.html", getGuestByID=getGuestByID, pullAvailableRooms=pullAvailableRooms, getGuest=getGuest, allowEdit=allowEdit, guests=getAllGuests(), form=NewGuestForm())
