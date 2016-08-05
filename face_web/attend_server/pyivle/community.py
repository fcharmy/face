from . import api

class Community():
    # Community.Communities
    def communities(self, duration=0, auth=True):
        params = {'Duration': duration}
        return api.call('Communities', params, auth)

    # Community.CommunitySearch
    def community_search(self, searchType, keyword, activeOnly=False, titleOnly=False, auth=True):
        params = {'SearchType': searchType, 'Keyword': keyword, 'ActiveOnly': activeOnly, 'TitleOnly': titleOnly}
        return api.call('CommunitySearch', params, auth)

    # Community.CommunityCategories
    def community_categories(self, activeOnly=False, auth=True):
        params = {'ActiveOnly': activeOnly}
        return api.call('CommunityCategories', params, auth)

    # Community.CommunityTags
    def community_tags(self, activeOnly=False, auth=True):
        params = {'ActiveOnly': activeOnly}
        return api.call('CommunityTags', params, auth)

    # Community.Community
    def community(self, comId, duration=0, auth=True):
        params = {'ComID': comId, 'Duration': duration}
        return api.call('Community', params, auth)

    # Community.CommunityMembers
    def community_members(self, comId, auth=True):
        params = {'ComID': comId}
        return api.call('CommunityMembers', params, auth)

    # Community.CommunityAnnouncements
    def community_announcements(self, comId, duration=0, auth=True):
        params = {'ComID': comId, 'Duration': duration}
        return api.call('CommunityAnnouncements', params, auth)

    # Community.CommunityWorkbinFolders
    def community_workbin_folders(self, comId, includingFiles=True, duration=0, auth=True):
        params = {'ComID': comId, 'IncludingFiles': includingFiles, 'Duration': duration}
        return api.call('CommunityWorkbinFolders', params, auth)

    # Community.CommunityWorkbinFiles
    def community_workbin_files(self, comId, folderId, duration=0, auth=True):
        params = {'ComID': comId, 'FolderID': folderId, 'Duration': duration}
        return api.call('CommunityWorkbinFiles', params, auth)

    # Community.CommunityForumHeadings
    def community_forum_headings(self, comId, includingPosts=True, duration=0, auth=True):
        params = {'ComID': comId, 'IncludingPosts': includingPosts, 'Duration': duration}
        return api.call('CommunityForumHeadings', params, auth)
    
    # Community.CommunityForumPosts
    def community_forum_posts(self, headingId, duration=0, auth=True):
        params = {'HeadingId': headingId, 'Duration': duration}
        return api.call('CommunityForumPosts', params, auth)

    # Community.CommunityForum_AddLogByPost_JSON
    def community_forum_add_log_by_post(self, postId, auth=True):
        params = {'PostID': postId}
        return api.call('CommunityForum_AddLogByPost_JSON', params, auth, 'post')

    # Community.CommunityForum_NewTopic_JSON
    def community_forum_new_topic(self, headingId, title, message, auth=True):
        params = {'HeadingID': headingId, 'Title': title, 'Message': message}
        return api.call('CommunityForum_NewTopic_JSON', params, auth, 'post')

    # Community.CommunityForum_ReplyPost_JSON
    def community_forum_reply_post(self, postId, title, message, auth=True):
        params = {'PostID': postId, 'Title': title, 'Message': message}
        return api.call('CommunityForum_ReplyPost_JSON', params, auth, 'post')

    # Community.CommunityWeblinks
    def community_weblinks(self, comId, auth=True):
        params = {'ComID': comId}
        return api.call('CommunityWeblinks', params, auth)

    # Community.Community_Join_JSON
    def community_join(self, comId, auth=True):
        params = {'ComID': comId}
        return api.call('Community_Join_JSON', params, auth, 'post')

    # Community.Community_Quit_JSON
    def community_quit(self, comId, auth=True):
        params = {'ComID': comId}
        return api.call('Community_Quit_JSON', params, auth, 'post')

    # Community.Community_AddMember_JSON
    def community_add_member(self, comId, memberId, memberType, auth=True):
        params = {'ComID': comId, 'MemberID': memberId, 'MemberType': memberType}
        return api.call('Community_AddMember_JSON', params, auth, 'post')

    # Community.Community_DeleteMember_JSON
    def community_delete_member(self, comId, memberId, auth=True):
        params = {'ComID': comId, 'MemberID': memberId}
        return api.call('Community_DeleteMember_JSON', params, auth, 'post')

    # Community.Community_UpdateMember_JSON
    def community_update_member(self, comId, memberId, memberType, auth=True):
        params = {'ComID': comId, 'MemberID': memberId, 'MemberType': memberType}
        return api.call('Community_UpdateMember_JSON', params, auth, 'post')

    # Community.Community_Create_JSON
    def community_create(self, title, description, accessType, defaultForum, defaultWorkbin, categoryId, tags, auth=True):
        params = {'Title': title, 'Description': description, 'AccessType': accessType, 'DefaultForm': defaultForum, 'DefaultWorkbin': defaultWorkbin, 'CategoryID': categoryId, 'Tags': tags}
        return api.call('Community_Create_JSON', params, auth, 'post')

    # Community.Community_Update_JSON
    def community_update(self, title, description, accessType, defaultForum, defaultWorkbin, categoryId, tags, displayMembersTo, openingDate, expiryDate, auth=True):
        params = {'Title': title, 'Description': description, 'AccessType': accessType, 'DefaultForm': defaultForum, 'DefaultWorkbin': defaultWorkbin, 'CategoryID': categoryId, 'Tags': tags, 'DisplayMembersTo': displayMembersTo, 'OpeningDate': openingDate, 'ExpiryDate': expiryDate}
        return api.call('Community_Update_JSON', params, auth, 'post')

    # Community.Community_GetTask
    def community_get_task(self, taskId, auth=True):
        params = {'TaskID': taskId}
        return api.call('Community_GetTask', params, auth)

    # Community.Community_GetAllTasks
    def community_get_all_tasks(self, comId, auth=True):
        params = {'ComID': comId}
        return api.call('Community_GetAllTasks', params, auth)

    # Community.Community_GetSubTask
    def community_get_sub_task(self, taskId, auth=True):
        params = {'TaskID': taskId}
        return api.call('Community_GetSubTask', params, auth)

    # Community.Community_CreateTask_JSON
    def community_create_task(self, taskId, taskName, taskDescription, parentTaskId, taskStatus, taskPriority, taskDueDate, auth=True):
        params = {'TaskID': taskId, 'TaskName': taskName, 'TaskDescription': taskDescription, 'ParentTaskID': parentTaskId, 'TaskStatus': taskStatus, 'TaskPriority': taskPriority, 'TaskDueDate': taskDueDate}
        return api.call('Community_CreateTask_JSON', params, auth, 'post')

    # Community.Community_UpdateTask_JSON
    def community_update_task(self, taskId, taskName, taskDescription, parentTaskId, taskStatus, taskPriority, taskDueDate, auth=True):
        params = {'TaskID': taskId, 'TaskName': taskName, 'TaskDescription': taskDescription, 'ParentTaskID': parentTaskId, 'TaskStatus': taskStatus, 'TaskPriority': taskPriority, 'TaskDueDate': taskDueDate}
        return api.call('Community_UpdateTask_JSON', params, auth, 'post')

    # Community.Community_DeleteTask_JSON
    def community_delete_task(self, taskId, auth=True):
        params = {'TaskID': taskId}
        return api.call('Community_DeleteTask_JSON', params, auth, 'post')

    # Community.Community_CreateComment_JSON
    def community_create_comment(self, taskId, comment, auth=True):
        params = {'TaskID': taskId, 'Comment': comment}
        return api.call('Community_CreateComment_JSON', params, auth, 'post')

    # Community.Community_UpdateComment_JSON
    def community_update_comment(self, commentId, comment, auth=True):
        params = {'CommentID': commentId, 'Comment': comment}
        return api.call('Community_UpdateComment_JSON', params, auth, 'post')

    # Community.Community_DeleteComment_JSON
    def community_delete_comment(self, commentId, auth=True):
        params = {'CommentID': commentId}
        return api.call('Community_DeleteComment_JSON', params, auth, 'post')

    # Community.Community_GetComment
    def community_get_comment(self, commentId, auth=True):
        params = {'CommentID': commentId}
        return api.call('Community_GetComment', params, auth) 

    # Community.Community_GetAllComments
    def community_get_all_comments(self, taskId, auth=True):
        params = {'TaskID': taskId}
        return api.call('Community_GetAllComments', params, auth) 

    # Non-standard API method, replacement for Community.DownloadFile
    def community_download_file(id, auth=True):
        return api.download_file(id, 'community', auth)
