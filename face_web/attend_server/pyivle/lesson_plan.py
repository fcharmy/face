from . import api

class LessonPlan():
    # LessonPlan.LessonPlan_Events
    def lesson_plan_events(self, courseId, eventDate, auth=True):
        params = {'CourseID': courseId, 'EventDate': eventDate}
        return api.call('LessonPlan_Events', params, auth)

    # LessonPlan.Lessonplan_Summary_Name
    def lesson_plan_summary_name(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Lessonplan_Summary_Name', params, auth)

    # LessonPlan.Lessonplan_Summary_Week
    def lesson_plan_summary_week(self, courseId, weekNo, auth=True):
        params = {'CourseID': courseId, 'WeekNo': weekNo}
        return api.call('Lessonplan_Summary_Week', params, auth)

    # LessonPlan.Lessonplan_Summary_Week_Event
    def lesson_plan_summary_week_event(self, courseId, weekNo, auth=True):
        params = {'CourseID': courseId, 'WeekNo': weekNo}
        return api.call('Lessonplan_Summary_Week_Event', params, auth)

    # LessonPlan.Lessonplan_Summary_Topic
    def lesson_plan_summary_topic(self, courseId, topicNo, auth=True):
        params = {'CourseID': courseId, 'TopicNo': topicNo}
        return api.call('Lessonplan_Summary_Topic', params, auth)

    # LessonPlan.Lessonplan_Summary_Topic_Event
    def lesson_plan_summary_topic_event(self, courseId, topicNo, auth=True):
        params = {'CourseID': courseId, 'TopicNo': topicNo}
        return api.call('Lessonplan_Summary_Topic_Event', params, auth)
