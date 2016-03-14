from RoomReserve import *
from RoomReserve.admin.rooms import getAllRooms, getActiveRooms, getRoomsByStatus
from RoomReserve.admin.reservation import getReservationsStartingBetweenDates, getReservationsEndingBetweenDates
import datetime


# ::: Rooms :::

def listOfAllTotalRooms():
    return list(getAllRooms())

def numberOfAllTotalRooms():
    return len(listOfAllTotalRooms())

def listOfActiveRooms():
    return list(getActiveRooms())

def numberOfActiveRooms():
    return len(getActiveRooms())

def listOfRoomsCurrentlyOccupied():
    return list(getRoomsByStatus(CONST.occupied_status))

def numberOfRoomsCurrentlyOccupied():
    return len(listOfRoomsCurrentlyOccupied())

def listOfRoomsCurrentlyUnoccupied():
    return list(getRoomsByStatus(CONST.ready_status))

def numberOfRoomsCurrentlyUnoccupied():
    return len(listOfRoomsCurrentlyUnoccupied())

def listOfInactiveRooms():
    return list(getRoomsByStatus(CONST.inactive_status))

def numberOfInactiveRooms():
    return len(listOfInactiveRooms())



# ::: Reservations :::

def listOfAllTotalReservations():
    return list(getAllReservations())

def numberOfAllTotalReservations():
    return len(listOfAllTotalReservations())

def listOfAllUpcomingReservations():
    today = datetime.date.today()
    max = datetime.date.max
    return list(getReservationsStartingBetweenDates(today, max))

def numberOfAllUpcomingReservations():
    return len(listOfAllUpcomingReservations())


# :::::: Reservations: Checking In ::::::

def listOfReservationsCheckingInOnDate(dt):
    return list(getReservationsStartingBetweenDates(dt, dt))

def numberOfReservationsCheckingInOnDate(dt):
    return len(listOfReservationsCheckingInOnDate(dt))

def listOfReservationsCheckingInToday():
    return listOfReservationsCheckingInOnDate(datetime.date.today())

def numberOfReservationsCheckingInToday():
    return len(listOfReservationsCheckingInToday())

def listOfReservationsCheckingInTomorrow():
    return listOfReservationsCheckingInOnDate(datetime.date.today()+datetime.timedelta(days=1))

def numberOfReservationsCheckingInTomorrow():
    return len(listOfReservationsCheckingInToday())


# :::::: Reservations: Checking Out ::::::

def listOfReservationsCheckingOutOnDate(dt):
    return list(getReservationsEndingBetweenDates(dt, dt))

def numberOfReservationsCheckingOutOnDate(dt):
    return len(listOfReservationsCheckingOutOnDate(dt))

def listOfReservationsCheckingOutToday():
    return listOfReservationsCheckingOutOnDate(datetime.date.today())

def numberOfReservationsCheckingOutToday():
    return len(listOfReservationsCheckingOutToday())

def listOfReservationsCheckingOutTomorrow():
    return listOfReservationsCheckingOutOnDate(datetime.date.today()+datetime.timedelta(days=1))

def numberOfReservationsCheckingOutTomorrow():
    return len(listOfReservationsCheckingOutToday())
