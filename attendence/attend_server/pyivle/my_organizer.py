from . import api

class MyOrganizer():
    # MyOrganizer.MyOrganizer_Personal
    def my_organizer_personal(self, startDate=None, endDate=None, auth=True):
        params = {'StartDate': startDate, 'EndDate': endDate}
        return api.call('MyOrganizer_Personal', params, auth)

    # MyOrganizer.MyOrganizer_IVLE
    def my_organizer_ivle(self, startDate=None, endDate=None, auth=True):
        params = {'StartDate': startDate, 'EndDate': endDate}
        return api.call('MyOrganizer_IVLE', params, auth)

    # MyOrganizer.MyOrganizer_Events
    def my_organizer_events(self, startDate=None, endDate=None, auth=True):
        params = {'StartDate': startDate, 'EndDate': endDate}
        return api.call('MyOrganizer_Events', params, auth)

    # MyOrganizer.MyOrganizer_AddPersonalEvent_JSON
    def my_organizer_add_personal_event(self, eventTitle, venue, eventDateTime, description, recurType, weeklyRecurEvery, strDays, recurTillDate, auth=True):
        params = {'EventTitle': eventTitle, 'Venue': venue, 'EventDateTime': eventDateTime, 'Description': description, 'RecurType': recurType, 'WeeklyRecurEvery': weeklyRecurEvery, 'StrDays': strDays, 'RecurTillDate': recurTillDate}
        return api.call('MyOrganizer_AddPersonalEvent_JSON', params, auth, 'post')

    # MyOrganizer.MyOrganizer_UpdatePersonalEvent_JSON
    def my_organizer_update_personal_event(self, eventId, eventTitle, venue, eventDateTime, description, recurType, weeklyRecurEvery, strDays, recurFromDate, recurTillDate, updateRecurrenceEvent, auth=True):
        params = {'EventID': eventId, 'EventTitle': eventTitle, 'Venue': venue, 'EventDateTime': eventDateTime, 'Description': description, 'RecurType': recurType, 'WeeklyRecurEvery': weeklyRecurEvery, 'StrDays': strDays, 'RecurFromDate': recurFromDate, 'RecurTillDate': recurTillDate, 'UpdateRecurrenceEvent': updateRecurrenceEvent}
        return api.call('MyOrganizer_UpdatePersonalEvent_JSON', params, auth, 'post')

    # MyOrganizer.MyOrganizer_DeletePersonalEvent_JSON
    def my_organizer_delete_personal_event(self, eventId, deleteAllRecurrence, auth=True):
        params = {'EventID': eventId, 'DeleteAllRecurrence': deleteAllRecurrence}
        return api.call('MyOrganizer_DeletePersonalEvent_JSON', params, auth, 'post')

    # MyOrganizer.MyOrganizer_SpecialDays
    def my_organizer_special_days(self, startDate=None, endDate=None, auth=True):
        params = {'StartDate': startDate, 'EndDate': endDate}
        return api.call('MyOrganizer_SpecialDays', params, auth)

    # MyOrganizer.MyOrganizer_AcadSemesterInfo
    def my_organizer_acad_semester_info(self, acadYear, semester, auth=True):
        params = {'AcadYear': acadYear, 'Semester': semester}
        return api.call('MyOrganizer_AcadSemesterInfo', params, auth)

    # MyOrganizer.CodeTable_WeekTypes
    def code_table_week_types(self, auth=True):
        return api.call('CodeTable_WeekTypes', {}, auth)
