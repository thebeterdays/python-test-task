import requests
import json
import os
import datetime

currentDateTime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

todos = requests.get('https://json.medrating.org/todos/')
users = requests.get('https://json.medrating.org/users/')

tasks = json.loads(todos.text)
allUsers = json.loads(users.text)

if not os.path.exists('tasks'):
    os.mkdir("tasks")

dir = os.path.abspath(os.curdir) + '/tasks/'

def writeTxt(user):
    user_file_path = dir + user['username'] + ".txt"
    if os.path.exists(user_file_path):
        os.rename(user_file_path, dir + 'old_' + user['username'] + '_' + currentDateTime + ".txt")
    open(user_file_path, "w")
    file_object = open(user_file_path, 'w')
    completedTasks = []
    notCompletedTasks = []
    for user_task_lenght in user['tasks']:
        data = user['tasks'][user_task_lenght]['title'][:48] + (user['tasks'][user_task_lenght]['title'][48:] and '...')
        if user['tasks'][user_task_lenght]['completed']:
            completedTasks.append(data)
        else:
            notCompletedTasks.append(data)
    lines = [
                'Отчёт для ' + user['company']['name'] + '.',
                user['name'] + ' <' + user['email'] + '> ' + currentDateTime,
                'Всего задач : ' + str(len(user['tasks'])),
                '',
                'Завершённые задачи:(' + str(len(completedTasks)) + '):'
            ] + completedTasks + [
                '',
                'Оставшиеся задачи:(' + str(len(notCompletedTasks)) + '): '
            ] + notCompletedTasks
    with file_object as file:
        for line in lines:
            file.write(line + '\n')

for user in allUsers:
    i = 0
    user['tasks'] = {}
    for task in tasks:
        if 'userId' in task and user['id'] == task['userId']:
            user['tasks'][str(i)] = task
            i += 1
    writeTxt(user)
