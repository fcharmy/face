from . import api

class RostersAndGroups():
    # Rosters_and_Groups.Class_Roster
    def class_roster(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Class_Roster', params, self, auth)

    # Rosters_and_Groups.Guest_Roster
    def guest_roster(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Guest_Roster', params, self, auth)

    # Rosters_and_Groups.GroupsByUserAndModule
    def groups_by_user_and_module(self, courseId=None, acadYear=None, semester=None, auth=True):
        if courseId is None and (None in [acadYear, semester]):
            raise api.InvalidParametersException('If courseId is empty, then acadYear and semester cannot be empty.')
        else:
            params = {'CourseID': courseId, 'AcadYear': acadYear, 'Semester': semester}
        return api.call('GroupsByUserAndModule', params, self, auth)

    # Rosters_and_Groups.GroupsByUser
    def groups_by_user(self, auth=True):
        return api.call('GroupsByUser', {}, self, auth)

    # Rosters_and_Groups.Module_ClassGroups
    def module_class_groups(self, courseId, auth=True):
        params = {'CourseID': courseId}
        return api.call('Module_ClassGroups', params, self, auth)

    # Rosters_and_Groups.Module_ClassGroupUsers
    def module_class_group_users(self, classGroupId, auth=True):
        params = {'ClassGroupID': classGroupId}
        return api.call('Module_ClassGroupUsers', params, self, auth)

    # Rosters_and_Groups.Module_OfficialGroupUsers
    def module_official_group_users(self, courseId=None, moduleCode=None, groupName=None, acadYear=None, semester=None, groupType=None, auth=True):
        if courseId and (None in [groupName, groupType]):
            raise api.InvalidParametersException('If courseId is given, then groupName and groupType cannot be empty.')
        elif courseId is None and (None in [moduleCode, groupName, acadYear, semester, groupType]):
            raise api.InvalidParametersException('If courseId is empty, then moduleCode, groupName, acadYear, semester, and groupType cannot be empty.')
        else:
            params = {'CourseID': courseId, 'ModuleCode': moduleCode, 'GroupName': groupName, 'AcadYear': acadYear, 'Semester': semester, 'GroupType': groupType}
        return api.call('Module_OfficialGroupUsers', params, self, auth)

    # Rosters_and_Groups.ClassGroupSignUp_JSON
    def class_group_sign_up(self, courseId, groupId, auth=True):
        params = {'CourseID': courseId, 'GroupID': groupId}
        return api.call('ClassGroupSignUp_JSON', params, self, auth, 'post')

    # Rosters_and_Groups.ClassGroupSignUpRemove_JSON
    def class_group_sign_up_remove(self, courseId, groupId, auth=True):
        params = {'CourseID': courseId, 'GroupID': groupId}
        return api.call('ClassGroupSignUpRemove_JSON', params, self, auth, 'post')

    # Rosters_and_Groups.GroupProjectsByUser
    def group_projects_by_user(self, courseId, includeGroups, groupType, auth=True):
        params = {'CourseID': courseId, 'IncludeGroups': includeGroups, 'GroupType': groupType}
        return api.call('GroupProjectsByUser', params, self, auth)

    # Rosters_and_Groups.Project_SelfEnrolGroups
    def project_self_enrol_groups(self, projectId, auth=True):
        params = {'ProjectID': projectId}
        return api.call('Project_SelfEnrolGroups', params, self, auth)

    # Rosters_and_Groups.ProjectGroupUsers
    def project_group_users(self, projectGroupId, auth=True):
        params = {'ProjectGroupID': projectGroupId}
        return api.call('ProjectGroupUsers', params, self, auth)

    # Rosters_and_Groups.Project_EnrolledGroups
    def project_enrolled_groups(self, auth=True):
        return api.call('Project_EnrolledGroups', {}, self, auth)

    # Rosters_and_Groups.ProjectGroup_SignUp_JSON
    def project_group_sign_up(self, projectGroupId, auth=True):
        params = {'ProjectGroupID': projectGroupId}
        return api.call('ProjectGroup_SignUp_JSON', params, self, auth, 'post')

    # Rosters_and_Groups.ProjectGroup_RemoveSignUp_JSON
    def project_group_remove_sign_up(self, projectGroupId, auth=True):
        params = {'ProjectGroupID': projectGroupId}
        return api.call('ProjectGroup_RemoveSignUp_JSON', params, self, auth, 'post')
