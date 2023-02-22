import requests

n, k = map(int, input('Ввведите n, k: ').split())
requests.get(f'http://localhost:5000/updateData/{n}/{k}/')   # изменяет параметры сервера организаторов
data = requests.get('http://localhost:5000/getData').json()     # получает данные с сервера
requests.post('http://localhost:8000/api/AddNewData/', json=data)