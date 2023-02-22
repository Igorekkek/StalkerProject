import requests
import os
from threading import Thread

def server1():
    os.system('python backend/manage.py runserver')

def server2():
    os.system('python organizers_server.py')

Thread(target=server1).start()
Thread(target=server2).start()

# print('Сервера запущенны')
requests.get('http://localhost:5000/updateData/10/13/')   # изменяет параметры сервера организаторов
data = requests.get('http://localhost:5000/getData').json()     # получает данные с сервера
requests.post('http://localhost:8000/api/AddNewData/', json=data)   # отправляет данные на наш сервер

