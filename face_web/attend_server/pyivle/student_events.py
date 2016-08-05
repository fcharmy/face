from . import api

class StudentEvents():
    # StudentEvents.StudentEvents
    def student_events(self, titleOnly=False, auth=True):
        params = {'TitleOnly': titleOnly}
        return api.call('StudentEvents', params, auth)

    # StudentEvents.StudentEvents_Categories
    def student_events_categories(self, includeEvents=True, titleOnly=False, auth=True):
        params = {'IncludeEvents': includeEvents, 'TitleOnly': titleOnly}
        return api.call('StudentEvents_Categories', params, auth)

    # StudentEvents.StudentEvents_Committees
    def student_events_committees(self, includeEvents=True, titleOnly=False, auth=True):
        params = {'IncludeEvents': includeEvents, 'TitleOnly': titleOnly}
        return api.call('StudentEvents_Committees', params, auth)

    # StudentEvents.StudentEvents_Category
    def student_events_category(self, categoryId, titleOnly=False, auth=True):
        params = {'CategoryID': categoryId, 'TitleOnly': titleOnly}
        return api.call('StudentEvents_Category', params, auth)

    # StudentEvents.StudentEvents_Committee
    def student_events_committee(self, committeeId, titleOnly=False, auth=True):
        params = {'CommitteeID': committeeId, 'TitleOnly': titleOnly}
        return api.call('StudentEvents_Committee', params, auth)

    # StudentEvents.StudentEvents_PostNewEvent_JSON
    def student_events_post_new_event(self, categoryId, committeeId, title, evtStartDate, evtEndDate, auth=True):
        params = {'CategoryID': categoryId, 'CommitteeID': committeeId, 'Title': title, 'evtStartDate': evtStartDate, 'evtEndDate': evtEndDate}
        return api.call('StudentEvents_PostNewEvent_JSON', params, auth, 'post')
