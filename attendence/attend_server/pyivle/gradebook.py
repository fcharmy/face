from . import api

class Gradebook():
    # Gradebook.Gradebook_ViewItems
    def gradebook_view_items(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Gradebook_ViewItems', params, auth)
