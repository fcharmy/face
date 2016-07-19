from . import api

class LibraryEReserves():
    # LibraryEReserves.LibEreserves
    def lib_ereserves(self, courseId, titleOnly=False, auth=True):
        params = {'CourseID': courseId, 'TitleOnly': titleOnly}
        return api.call('LibEreserves', params, auth)

    # LibraryEReserves.LibEreserveFiles
    def lib_ereserves_files(self, folderId, auth=True):
        params = {'FolderID': folderId}
        return api.call('LibEreserveFiles', params, auth)
