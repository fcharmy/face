from . import api

class Profile():
    # Profile.Profile_View
    def profile_view(self, auth=True):
        return api.call('Profile_View', {}, self, auth)
