from . import api

class Module():
    # Module.Modules
    def modules(self, duration=0, includeAllInfo=True, auth=True):
        params = {'Duration': duration, 'IncludeAllInfo': includeAllInfo}
        return api.call('Modules', params, self, auth)

    # Module.Modules_Staff
    def modules_staff(self, duration=0, includeAllInfo=True, auth=True):
        params = {'Duration': duration, 'IncludeAllInfo': includeAllInfo}
        return api.call('Modules_Staff', params, self, auth)

    # Module.Modules_Student
    def modules_student(self, duration=0, includeAllInfo=True, auth=True):
        params = {'Duration': duration, 'IncludeAllInfo': includeAllInfo}
        return api.call('Modules_Student', params, self, auth)

    # Module.module
    def module(self, courseId, duration=0, includeAllInfo=True, titleOnly=False, auth=True):
        params = {'Duration': duration, 'IncludeAllInfo': includeAllInfo, 'CourseID': courseId, 'TitleOnly': titleOnly}
        return api.call('Module', params, self, auth)

    # Module.Modules_Search
    def modules_search(self, duration=0, includeAllInfo=True, auth=True):
        params = {'Duration': duration, 'IncludeAllInfo': includeAllInfo}
        return api.call('Modules_Search', params, self, auth)

    # Module.Modules_Lecturers
    def module_lecturers(self, courseId, duration=0, auth=True):
        params = {'Duration': duration, 'CourseID': courseId}
        return api.call('Module_Lecturers', params, self, auth)

    # Module.Module_Information
    def module_information(self, courseId, duration=0, auth=True):
        params = {'Duration': duration, 'CourseID': courseId}
        return api.call('Module_Information', params, self, auth)

    # Module.Module_Weblinks
    def module_weblinks(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Module_Weblinks', params, self, auth)

    # Module.Module_ReadingFormatted
    def module_reading_formatted(self, courseId, duration=0, auth=True):
        params = {'Duration': duration, 'CourseID': courseId}
        return api.call('Module_ReadingFormatted', params, self, auth)

    # Module.Module_ReadingUnformatted
    def module_reading_unformatted(self, courseId, duration=0, auth=True):
        params = {'Duration': duration, 'CourseID': courseId}
        return api.call('Module_ReadingUnformatted', params, self, auth)

    # Module.Module_ReadingsFormatted_Coop
    def module_readings_formatted_coop(self, date, auth=True):
        params = {'date': date}
        return api.call('Module_ReadingsFormatted_Coop', params, self, auth)

    # Module.Module_Reading
    def module_reading(self, courseId, duration=0, auth=True):
        params = {'Duration': duration, 'CourseID': courseId}
        return api.call('Module_Reading', params, self, auth)

    # Module.Modules_Taken
    def modules_taken(self, studentId, auth=True):
        params = {'StudentID': studentId}
        return api.call('Modules_Taken', params, self, auth)
