from RoomReserve import *
from RoomReserve.admin.reservation import find_available_rooms, createReservation, getReservationByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.building import getBuildingById
from RoomReserve.admin.guest import getAllGuests


@app.route('/reservation/new/', methods=['GET', 'POST'])
@Login.standard_required
def page_newres():
  def pullAvailableRooms(capacity, indate, outdate):
    indate = delorean.parse(indate).naive()
    outdate = delorean.parse(outdate).naive()

    availableRooms = find_available_rooms(indate, outdate, capacity=capacity)

    return availableRooms
    
  def allowEdit(id):
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
    
  return render("newReservation.html", pullAvailableRooms=pullAvailableRooms, allowEdit=allowEdit)
