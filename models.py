import asyncio
import datetime


class ProblemSet:
    def __init__(self, data: dict):
        self.id = data.get('id', '')
        self.name = data.get('name', '')
        self.type = data.get('type', '')
        self.time_type = data.get('timeType', '')
        self.status = data.get('status', '')
        self.organization_name = data.get('organizationName', '')
        self.owner_nickname = data.get('ownerNickname', '')
        self.manageable = data.get('manageable', False)\
            # '2024-07-05T03:00:00Z'
        self.create_at = datetime.datetime.strptime(
            data.get('createAt', ''), '%Y-%m-%dT%H:%M:%SZ')
        self.update_at = datetime.datetime.strptime(
            data.get('updateAt', ''), '%Y-%m-%dT%H:%M:%SZ')
        self.scoring_rule = data.get('scoringRule', '')
        self.organization_type = data.get('organizationType', '')
        self.owner_id = data.get('ownerId', '')
        self.start_at = datetime.datetime.strptime(
            data.get('startAt', ''), '%Y-%m-%dT%H:%M:%SZ')
        self.end_at = datetime.datetime.strptime(
            data.get('endAt', ''), '%Y-%m-%dT%H:%M:%SZ')
        self.duration = data.get('duration', 0)
        self.problem_set_config = data.get('problemSetConfig', {})
        self.owner_organization_id = data.get('ownerOrganizationId', '')
        self.stage = data.get('stage', '')
        self.feature = data.get('feature', '')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __ne__(self, other):
        return self.id != other.id


class Exam:
    def __init__(self, data: dict):
        self.id = data.get('id', '')
        self.score = data.get('score', 0)
        self.start_at = datetime.datetime.strptime(
            data.get('startAt', ''), '%Y-%m-%dT%H:%M:%SZ')
        self.end_at = datetime.datetime.strptime(
            data.get('endAt', ''), '%Y-%m-%dT%H:%M:%SZ')
        self.accept_count = data.get('acceptCount', 0)
        self.exam_config = data.get('examConfig', {})
        self.student_user = data.get('studentUser', {})
        self.problem_set_id = data.get('problemSetId', '')
        self.user_id = data.get('userId', '')
        self.ended = data.get('ended', False)
        self.status = data.get('status', '')
        self.reset_status = data.get('resetStatus', False)
        self.adjust_amount = data.get('adjustAmount', 0)
        self.adjusted_score = data.get('adjustedScore', 0)

    def __str__(self):
        return f'{self.student_user["name"]}'

    def __repr__(self):
        return f'{self.student_user["name"]}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __ne__(self, other):
        return self.id != other.id


class Problem:
    def __init__(self):
        self.id = ''
        self.label = ''
        self.score = 0
        self.deadline = datetime.datetime.now()
        self.accept_count = 0
        self.submit_count = 0
        self.title = ''
        self.type = ''
        self.difficulty = 0
        self.compiler = ''
        self.problem_status = ''
        self.problem_set_id = ''
        self.problem_pool_index = 0
        self.index_in_problem_pool = 0
        self.problem_submission_status = ''
        self.content = ''
        self.problem_id = ''

    @classmethod
    def from_data(cls, data: dict):
        self = cls()
        self.id = data.get('id', '')
        self.label = data.get('label', '')
        self.score = data.get('score', 0)
        self.deadline = datetime.datetime.strptime(
            data.get('deadline', '1970-01-01T00:00:00Z'), '%Y-%m-%dT%H:%M:%SZ')
        self.accept_count = data.get('acceptCount', 0)
        self.submit_count = data.get('submitCount', 0)
        self.title = data.get('title', '')
        self.type = data.get('type', '')
        self.difficulty = data.get('difficulty', 0)
        self.compiler = data.get('compiler', '')
        self.problem_status = data.get('problemStatus', '')
        self.problem_set_id = data.get('problemSetId', '')
        self.problem_pool_index = data.get('problemPoolIndex', 0)
        self.index_in_problem_pool = data.get('indexInProblemPool', 0)
        self.problem_submission_status = data.get(
            'problemSubmissionStatus', '')
        return self

    def update_status(self, data: dict):
        self.problem_submission_status = data.get(
            'problemSubmissionStatus', '')

    def update_detail(self, data: dict):
        self.content = data.get('content', '')
        self.problem_id = data.get('problemId', '')

    def __str__(self):
        return f'{self.label}'

    def __repr__(self):
        return f'{self.label} {self.title}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __ne__(self, other):
        return self.id != other.id
