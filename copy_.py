import asyncio
import json

from tqdm import tqdm

import apis
import http_
from config import ACCOUNT, PASSWORD
from models import Exam, ProblemSet


async def download_answer():
    problem_sets = [ProblemSet(data) for data in await apis.get_all_problem_sets()]
    available_problem_sets = [
        problem_set for problem_set in problem_sets if problem_set.status == 'PROCESSING']
    problem_set = available_problem_sets[0]
    exam = Exam(await apis.get_exam_info(problem_set.id))

    problem_all = await apis.get_all_problems(problem_set.id, exam.id)

    solution_dict = {}
    for problem in tqdm(problem_all):
        answer = await apis.get_problem_last_submission(problem_set.id, problem.id)
        solution_dict[problem.id] = answer

    with open(f'solution/{problem_set.id}.json', 'w') as f:
        json.dump(solution_dict, f, indent=4, ensure_ascii=False)


async def upload_answer():
    problem_sets = [ProblemSet(data) for data in await apis.get_all_problem_sets()]
    available_problem_sets = [
        problem_set for problem_set in problem_sets if problem_set.status == 'PROCESSING']
    problem_set = available_problem_sets[0]
    exam = Exam(await apis.get_exam_info(problem_set.id))

    # problem_not_passed = await apis.get_not_passed_problems(problem_set.id, exam.id)
    problem_not_passed = await apis.get_all_problems(problem_set.id, exam.id)

    with open(f'solution/{problem_set.id}.json', 'r') as f:
        solution_dict = json.load(f)

    for problem in tqdm(problem_not_passed):
        data = solution_dict.get(problem.id)
        if not data:
            continue

        url = f'https://pintia.cn/api/exams/{exam.id}/submissions'
        payload = {
            'details': [
                data
            ],
            'problemType': 'PROGRAMMING',
        }
        await http_.post(url, json=payload)

    # for _, data in tqdm(solution_dict.items()):
    #     url = f'https://pintia.cn/api/exams/{exam.id}/submissions'
    #     payload = {
    #         'details': [
    #             data
    #         ],
    #         'problemType': 'PROGRAMMING',
    #     }
    #     await http_.post(url, json=payload)


if __name__ == "__main__":
    asyncio.run(apis.login(ACCOUNT, PASSWORD))

    # asyncio.run(download_answer())
    asyncio.run(upload_answer())
    pass
