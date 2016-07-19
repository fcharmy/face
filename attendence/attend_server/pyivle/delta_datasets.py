from . import api

class DeltaDatasets():
    # DeltaDatasets.Delta_ModuleTimeTable
    def delta_module_timetable(self, lastModified, moduleCode=None, auth=True):
        params = {'LastModified': lastModified, 'ModuleCode': moduleCode}
        return api.call('Delta_ModuleTimeTable', params, auth)
