import asyncio

from tqdm import tqdm

import http_
from constant import COMPYLER
from models import Problem
from utils import is_cn_phone, is_email


async def login(username: str, password: str):
    url = 'https://passport.pintia.cn/api/users/sessions'
    data = {
        "password": password,
        "rememberMe": True,
    }
    if is_email(username):
        data['email'] = username
    elif is_cn_phone(username):
        data['phone'] = username
    resp = await http_.post(url, json=data)
    if resp.text and resp.text == '{"error":{"code":"GATEWAY_WRONG_CAPTCHA","message":"验证码错误"}}':
        tqdm.write('验证码错误')
        import ui
        cookies = ui.validate_login(username, password)
        from httpx import Cookies
        http_cookies = Cookies()
        for cookie in cookies:
            http_cookies.set(cookie['name'], cookie['value'])
        http_.Session.set_cookies(http_cookies)
        return
    assert resp.status_code == 200
    http_.Session.set_cookies(resp.cookies)


async def check_login() -> bool:
    import http_
    http_.Session._load_from_local()
    url = 'https://pintia.cn/api/users/profile'
    resp = await http_.get(url)
    if resp.status_code == 200:
        return True
    return False


async def get_user_info() -> dict:
    url = 'https://pintia.cn/api/u/current'
    resp = await http_.get(url)
    return resp.json()


async def get_problem_sets():
    url = 'https://pintia.cn/api/problem-sets'
    resp = await http_.get(url)
    return resp.json().get('problemSets', [])


async def get_problem_sets_always():
    url = 'https://pintia.cn/api/problem-sets/always-available'
    resp = await http_.get(url)
    return resp.json().get('problemSets', [])


async def get_all_problem_sets():
    return await get_problem_sets() + await get_problem_sets_always()


async def get_exam_info(problem_set_id: str):
    url = f'https://pintia.cn/api/problem-sets/{problem_set_id}/exams'
    resp = await http_.get(url)
    return resp.json().get('exam', {})


async def get_exam_problem_list(problem_set_id: str, exam_id: str):
    url = 'https://pintia.cn/api/problem-sets/' + \
        f'{problem_set_id}/exam-problem-list?exam_id={exam_id}' + \
        '&problem_type=PROGRAMMING'
    resp = await http_.get(url)
    return resp.json().get('problemSetProblems', [])


async def get_exam_problem_status(problem_set_id: str):
    url = f'https://pintia.cn/api/problem-sets/{
        problem_set_id}/exam-problem-status'
    resp = await http_.get(url)
    return resp.json().get('problemStatus', [])


async def get_exam_problem_detail(problem_set_id: str, problem_id: str):
    url = f'https://pintia.cn/api/problem-sets/{
        problem_set_id}/exam-problems/{problem_id}'
    resp = await http_.get(url)
    return resp.json().get('problemSetProblem', {})


async def get_all_problems(problem_set_id: str, exam_id: str):
    problem_list = await get_exam_problem_list(problem_set_id, exam_id)
    problem_status = await get_exam_problem_status(problem_set_id)
    problems = [Problem.from_data(data) for data in problem_list]
    [problem.update_status(status)
     for problem, status in zip(problems, problem_status)]
    tasks = [
        get_exam_problem_detail(problem_set_id, problem.id)
        for problem in problems
    ]
    problems_detail = []
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='获取题目详情'):
        detail = await task
        problems_detail.append(detail)
    [
        problem.update_detail(detail)
        for problem, detail in zip(problems, problems_detail)
    ]
    return problems


async def get_not_passed_problems(problem_set_id: str, exam_id: str):
    problem_list = await get_exam_problem_list(problem_set_id, exam_id)
    problem_status = await get_exam_problem_status(problem_set_id)
    problems = [Problem.from_data(data) for data in problem_list]
    [problem.update_status(status)
     for problem, status in zip(problems, problem_status)]
    problems = [
        problem for problem in problems if problem.problem_submission_status != 'PROBLEM_ACCEPTED'][:50]
    tasks = [
        get_exam_problem_detail(problem_set_id, problem.id)
        for problem in problems
    ]
    problems_detail = []
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='获取题目详情'):
        detail = await task
        problems_detail.append(detail)
    [
        problem.update_detail(detail)
        for problem, detail in zip(problems, problems_detail)
    ]
    return problems


async def post_submission(exam_id: str, problem_id: str, code: str, lang: str):
    url = f'https://pintia.cn/api/exams/{exam_id}/submissions'
    data = {
        'details': [
            {
                'problemId': '0',
                'problemSetProblemId': problem_id,
                'programmingSubmissionDetail': {
                    'program': code,
                    'compiler': COMPYLER.get(lang, 'C++'),
                },
            },
        ],
        'problemType': 'PROGRAMMING',
    }
    resp = await http_.post(url, json=data)
    return resp
