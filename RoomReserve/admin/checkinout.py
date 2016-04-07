from RoomReserve import *
from RoomReserve.helpers.stats import listOfReservationsCheckingInToday, listOfReservationsCheckingOutToday
from RoomReserve.admin.guest import getGuestByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.reservation import getReservationByID

@app.route('/admin/checkin', methods=['GET','POST'])
def checkin_page():
    reslist = listOfReservationsCheckingInToday()
    return render('checkinout.html', reservations=reslist, checkInType=True, getGuestByID=getGuestByID, getRoomByID=getRoomByID)
  
@app.route('/admin/checkout', methods=['GET','POST'])
def checkout_page():
    reslist = listOfReservationsCheckingOutToday()
    return render('checkinout.html', reservations=reslist, checkInType=False, getGuestByID=getGuestByID, getRoomByID=getRoomByID)
  
  
@app.route('/check/<int:resID>/in')
@login_required
def processCheckin(resID):
    res = getReservationByID(resID)
    try:
        res.set_status(checkedin_status)
    except ex:
        return render('basic.html', content="Could not check in reservation with ID "+str(resID) + ex)

    return redirect('/admin/checkin')

@app.route('/check/<int:resID>/out')
@login_required
def processCheckout(resID):
    res = getReservationByID(resID)
    try:
        res.set_status(checkedout_status)
    except:
        return render('basic.html', content="Could not check out reservation with ID "+str(resID))

    return redirect('/admin/checkout')

    
    
    

