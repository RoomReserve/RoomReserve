from RoomReserve import *
from RoomReserve.helpers.stats import listOfReservationsCheckingInToday, listOfReservationsCheckingOutToday
from RoomReserve.admin.guest import getGuestByID

@app.route('/admin/checkin', methods=['GET','POST'])
def checkin_page():
  reslist = listOfReservationsCheckingInToday()
  return render('checkinout.html', reservations=reslist, checkInType=True, getGuestByID=getGuestByID)
  
@app.route('/admin/checkout', methods=['GET','POST'])
def checkout_page():
  reslist = listOfReservationsCheckingOutToday()
  return render('checkinout.html', reservations=reslist, checkInType=False, getGuestByID=getGuestByID)
