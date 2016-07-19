from . import api

class Poll():
    # Poll.Polls
    def polls(self, courseId, pollId, titleOnly=False, auth=True):
        params = {'CourseID': courseId, 'PollID': pollId, 'TitleOnly': titleOnly}
        return api.call('Polls', params, auth)

    # Poll.Poll_SubmitVote_JSON
    def poll_submit_vote(self, pollId, pollQuestionId, pollQuestionOptionId, otherText, auth=True):
        params = {'PollID': pollId, 'PollQuestionID': pollQuestionId, 'PollQuestionOptionID': pollQuestionOptionId, 'OtherText': otherText}
        return api.call('Poll_SubmitVote_JSON', params, auth, 'post')

    # Poll.Poll_GetVotedUser
    def poll_get_voted_user(self, pollId, pollQuestionId, pollQuestionOptionId, auth=True):
        params = {'PollID': pollId, 'PollQuestionID': pollQuestionId, 'PollQuestionOptionID': pollQuestionOptionId}
        return api.call('Poll_GetVotedUser', params, auth)

    # Poll.Poll_GetVotedUser_Other
    def poll_get_voted_user_other(self, pollId, pollQuestionId, auth=True):
        params = {'PollID': pollId, 'PollQuestionID': pollQuestionId}
        return api.call('Poll_GetVotedUser_Other', params, auth)
