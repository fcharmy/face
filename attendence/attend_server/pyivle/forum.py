from . import api

class Forum():
    #Forum.Forums
    def forums(self, courseId, duration=0, includeThreads=True, titleOnly=False, auth=True):
        params = {'CourseID': courseId, 'Duration': duration, 'IncludeThreads': includeThreads, 'TitleOnly': titleOnly}
        return api.call('Forums', params, auth)

    #Forum.Forum
    def forum(self, forumId, duration=0, includeThreads=True, auth=True):
        params = {'ForumID': forumId, 'Duration': duration, 'IncludeThreads': includeThreads}
        return api.call('Forum', params, auth)

    #Forum.Forum_Headings
    def forum_headings(self, forumId, duration=0, includeThreads=True, auth=True):
        params = {'ForumID': forumId, 'Duration': duration, 'IncludeThreads': includeThreads}
        return api.call('Forum_Headings', params, auth)

    #Forum.Forum_HeadingThreads
    def forum_heading_threads(self, headingId, duration=0, getMainTopicsOnly=True, auth=True):
        params = {'HeadingID': headingId, 'Duration': duration, 'GetMainTopicsOnly': getMainTopicsOnly}
        return api.call('Forum_HeadingThreads', params, auth)

    #Forum.Forum_Threads
    def forum_threads(self, threadId, duration=0, getSubThreads=True, auth=True):
        params = {'ThreadID': threadId, 'Duration': duration, 'GetSubThreads': getSubThreads}
        return api.call('Forum_Threads', params, auth)

    #Forum.Forum_Thread
    def forum_thread(self, threadId, auth=True):
        params = {'ThreadID': threadId}
        return api.call('Forum_Thread', params, auth)

    #Forum.Forum_PostNewThread_JSON
    def forum_post_new_thread(self, headingId, title, reply, auth=True):
        params = {'headingID': headingId, 'Title': title, 'Reply': reply}
        return api.call('Forum_PostNewThread_JSON', params, auth, 'post')

    #Forum.Forum_ReplyThread_JSON
    def forum_reply_thread(self, threadId, title, reply, auth=True):
        params = {'ThreadID': threadId, 'Title': title, 'Reply': reply}
        return api.call('Forum_ReplyThread_JSON', params, auth, 'post')

    #Forum.Forum_Thread_AddLog_JSON
    def forum_thread_add_log(self, threadId, auth=True):
        params = {'ThreadID': threadId}
        return api.call('Forum_Thread_AddLog_JSON', params, auth, 'post')

    #Forum.Forum_SaleOfUsedTextbooks
    def forum_sale_of_used_textbooks(self, duration=0, includeThreads=True, auth=True):
        params = {'Duration': duration, 'IncludeThreads': includeThreads}
        return api.call('Forum_SaleOfUsedTextbooks', params, auth)

    #Forum.Forum_StudentFeedback
    def forum_student_feedback(self, duration=0, includeThreads=True, auth=True):
        params = {'Duration': duration, 'IncludeThreads': includeThreads}
        return api.call('Forum_StudentFeedback', params, auth)
