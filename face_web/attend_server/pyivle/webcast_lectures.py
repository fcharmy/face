from . import api

class WebcastLectures():
    # Webcast_Lectures.Webcasts
    def webcasts(self, courseId, duration=0, mediaChannelId=None, auth=True):
        params = {'CourseID': courseId, 'Duration': duration, 'MediaChannelID': mediaChannelId}
        return api.call('Webcasts', params, auth)

    # Webcast_Lectures.Webcasts_AddLog_JSON
    def webcasts_add_log(self, mediaChannelId, mediaChannelItemId, auth=True):
        params = {'MediaChannelID': mediaChannelId, 'MediaChannelItemID': mediaChannelItemId}
        return api.call('Webcasts_AddLog_JSON', params, auth, 'post')
