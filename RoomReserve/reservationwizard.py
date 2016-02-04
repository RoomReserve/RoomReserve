from RoomReserve import *
from RoomReserve.admin.reservation import find_available_rooms

class Form_Wizard_Form(Form):
    '''
    The first form for the reservation wizard.
    Asks for dates and capacity.
    '''
    check_in_date = DateField('Check In')
    check_out_date = DateField('Check Out')
    capacity = IntegerField()

@app.route('/res/new', methods=['GET', 'POST'])
@Login.standard_required
def page_reservation_wizard():
    '''
    The first page in the reservation wizard
    '''
    form = Form_Wizard_Form()
    if request.method == 'POST':
        formdata = request.form
        indate = formdata['check_in_date']
        outdate = formdata['check_out_date']
        capacity = formdata['capacity']

        indate = delorean.parse(indate).naive()
        outdate = delorean.parse(outdate).naive()

        availableRooms = find_available_rooms(indate, outdate)
        return render('reswizard.html', form=form, rooms=availableRooms)



    return render('reswizard.html', form=form)
