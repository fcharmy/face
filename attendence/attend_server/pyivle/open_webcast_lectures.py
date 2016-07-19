from . import api

class OpenWebcastLectures():
    # OpenWebcastLectures.OpenWebcasts
    def open_webcasts(self, acadYear, semester, titleOnly=False, mediaChannelId=None, auth=True):
        params = {'AcadYear': acadYear, 'Semester': semester, 'TitleOnly': titleOnly, 'MediaChannelID': mediaChannelId}
        return api.call('OpenWebcasts', params, auth)

    # OpenWebcastLectures.OpenWebcast_AddLog_JSON
    def open_webcast_add_log(self, mediaChannelId, mediaChannelItemId, auth=True):
        params = {'MediaChannelID': mediaChannelId, 'MediaChannelItemID': mediaChannelItemId}
        return api.call('OpenWebcast_AddLog_JSON', params, auth, 'post')
