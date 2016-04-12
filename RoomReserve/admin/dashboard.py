from RoomReserve import *
import RoomReserve.helpers.stats as stats
from RoomReserve.admin.guest import getGuestByID
from RoomReserve.admin.rooms import getRoomByID
import datetime

@app.route("/admin/dashboard")
@login_required
def dashboard():

	title="Dashboard"
	content = ""
	data = {}

	data['getGuestByID'] = RoomReserve.admin.guest.getGuestByID
	data['getRoomByID'] = RoomReserve.admin.rooms.getRoomByID

	data['chin'] = []
	data['chout'] = []
	for d in range(7):
		# Get number of check ins and check outs for the next 7 days.
		data['chin'].append(stats.numberOfReservationsCheckingInOnDate(datetime.date.today() + datetime.timedelta(days=d)))
		data['chout'].append(stats.numberOfReservationsCheckingOutOnDate(datetime.date.today() + datetime.timedelta(days=d)))

	data['numOccupiedRooms'] = stats.numberOfRoomsCurrentlyOccupied()
	data['numUnoccupiedRooms'] = stats.numberOfRoomsCurrentlyUnoccupied()
	data['numInactiveRooms'] = stats.numberOfInactiveRooms()
	data['reservationsInToday'] = stats.listOfReservationsCheckingInToday()
	data['reservationsOutToday'] = stats.listOfReservationsCheckingOutToday()



	return render('dashboard.html', title=title, content=content, **data)
