from . import api

class Timetable():
    #Timetable.Timetable_Student
    def timetable_student(self, acadYear, semester, auth=True):
        params = {'AcadYear': acadYear, 'semester': semester}
        return api.call('Timetable_Student', params, auth)

    #Timetable.Timetable_Module
    def timetable_module(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Timetable_Module', params, auth)

    #Timetable.Timetable_Student_Module
    def timetable_student_module(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Timetable_Student_Module', params, auth)

    #Timetable.Timetable_ModuleExam
    def timetable_module_exam(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Timetable_ModuleExam', params, auth)
