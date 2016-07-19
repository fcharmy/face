from . import api

class IVLENews():
    # IVLENews.PublicNews
    def public_news(self, titleOnly=False, auth=False):
        params = {'TitleOnly': titleOnly}
        return api.call('PublicNews', params, auth)
