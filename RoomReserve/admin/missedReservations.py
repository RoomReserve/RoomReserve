from RoomReserve import *
from RoomReserve.helpers.stats import listOfReservationsCheckingInToday, listOfReservationsCheckingOutToday
from RoomReserve.admin.guest import getGuestByID
from RoomReserve.admin.rooms import getRoomByID
from RoomReserve.admin.reservation import getReservationByID, getMissedReservations
import datetime

@app.route('/admin/missed', methods=['GET','POST'])
@Login.standard_required
def missed_res_page():
    reslist = getMissedReservations(datetime.date.today())
    return render('missedReservations.html', reservations=reslist, getGuestByID=getGuestByID, getRoomByID=getRoomByID)
