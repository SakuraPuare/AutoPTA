import asyncio
from functools import partial
from multiprocessing import Pool

from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

import apis
from config import ACCOUNT, GENERICS_PROMPT, LANG, LLM_ARGS, PASSWORD, QUEUE
from llms.request_llms.bridge_chatgpt import predict_no_ui_long_connection
from models import Account, Exam, Problem, ProblemSet


def watch_dog(fun, *args, **kwargs):
    try:
        return fun(*args, **kwargs)
    except Exception as e:
        tqdm.write(f'Error: {e}')
        return watch_dog(fun, *args, **kwargs)


def generate_answer(problem: Problem, lang: str) -> str:
    if not problem.content:
        return ''

    prompt = f"""{GENERICS_PROMPT}\n请使用{lang}\
语言完成以下题目：\n\n```markdown\n{problem.content}\n```"""
    answer = watch_dog(predict_no_ui_long_connection,
                       inputs=prompt, llm_kwargs=LLM_ARGS, history=[], sys_prompt="程序员")
    if answer.startswith('```'):
        answer = '\n'.join(answer.split('\n')[1:-1])
    return (problem.id, answer)


async def submit_answer(problem: Problem, exam: Exam, lang: str):
    answer = generate_answer(problem, lang)
    await apis.post_submission(exam.id, problem.id, answer[-1], lang)


async def main():
    problem_sets = [ProblemSet(data) for data in await apis.get_all_problem_sets()]
    available_problem_sets = [
        problem_set for problem_set in problem_sets if problem_set.status == 'PROCESSING']
    problem_set = available_problem_sets[9]
    exam = Exam(await apis.get_exam_info(problem_set.id))
    problems_not_passed = await apis.get_not_passed_problems(problem_set.id, exam.id)

    pool = Pool(QUEUE)
    answers = list(tqdm(iterable=(pool.imap(partial(generate_answer, lang=LANG), problems_not_passed)),
                        total=len(problems_not_passed), desc='生成答案'))
    for problem, answer in zip(sorted(problems_not_passed), sorted(answers)):
        await apis.post_submission(exam.id, problem.id, answer[-1], LANG)

    # tasks = [submit_answer(problem, exam, LANG)
    #          for problem in problems_not_passed]
    # for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='提交答案'):
    #     await task

if __name__ == '__main__':
    asyncio.run(apis.login(ACCOUNT, PASSWORD))

    asyncio.run(main())
    pass
