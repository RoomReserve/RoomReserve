from RoomReserve import *
from RoomReserve.helpers.stats import listOfReservationsCheckingInToday, listOfReservationsCheckingOutToday
from RoomReserve.admin.guest import getGuestByID
from RoomReserve.admin.rooms import getRoomByID

@app.route('/admin/checkin', methods=['GET','POST'])
def checkin_page():
  reslist = listOfReservationsCheckingInToday()
  return render('checkinout.html', reservations=reslist, checkInType=True, getGuestByID=getGuestByID, getRoomByID=getRoomByID)
  
@app.route('/admin/checkout', methods=['GET','POST'])
def checkout_page():
  reslist = listOfReservationsCheckingOutToday()
  return render('checkinout.html', reservations=reslist, checkInType=False, getGuestByID=getGuestByID, getRoomByID=getRoomByID)
