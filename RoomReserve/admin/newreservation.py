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
    
  return render("newReservation.html", pullAvailableRooms=pullAvailableRooms)
