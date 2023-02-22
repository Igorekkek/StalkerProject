import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint, uniform

print('<Сервер запущен>')


def gen_data(n=1, k=3):
    pif = lambda x, y, x1, y1 : ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5

    k = max(3, k)
    # Генрирует n аномалий и max(3, k) детекторов.
    # Гарантируется, что каждую аномалию будут замечать как минимум 3 детектора.
    swans = [{'x' : randint(0, 40),
              'y' : randint(0, 30),
              'id' : i,
              'int0' : uniform(0.1, 20),
              'detected_by' : []} for i in range(n)]
    detectors = [{'coords' : [randint(0, 40), randint(0, 30)],
                  'id' : i,
                  'swans' : []} for i in range(k)]
    
    for idx, swan in enumerate(swans):
        while len(swan['detected_by']) < 3:
            idx2 = randint(0, len(detectors) - 1)
            if swan['id'] not in detectors[idx2]['swans']:
                detectors[idx2]['swans'].append(idx)
                swan['detected_by'].append(idx2)
    
    for idx, d in enumerate(detectors):
        new_swans = []
        for swan_id in d['swans']:
            intd = swans[swan_id]['int0'] / (pif(d['coords'][0], d['coords'][1], swans[swan_id]['x'], swans[swan_id]['y']) ** 2)
            new_swans.append( {'id' : swan_id, 'rate' : intd} )
        detectors[idx]['swans'] = new_swans
    return swans, detectors

class SipmleHandler(BaseHTTPRequestHandler):
    '''
    Данные создаются при запуске программы 
    http://localhost:5000/getData/ - получение данных по детекторам (основная функция сервера)
    http://localhost:5000/getSwans/ - аномалии (для дебагинга)
    http://localhost:5000/updateData/n/k - создание новых данных, n - число аномалий,
    k - детекторов (только изменяет, чтобы получить данные нужно отправить запрос на /getData/)
    '''

    swans, detectors = gen_data()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        if self.path.strip('/') in ('getData', 'getSwans'):
            d = {'getData' : bytes( json.dumps(SipmleHandler.detectors), 'utf-8' ),
                 'getSwans' : bytes( json.dumps(SipmleHandler.swans), 'utf-8' )}
            self.wfile.write( d[self.path.strip('/')] )
        elif 'updateData' in self.path:
            try:
                _, n, k = self.path.strip('/').split('/')
                SipmleHandler.swans, SipmleHandler.detectors = gen_data(int(n), int(k))
                self.wfile.write(b'success')
            except Exception as e:
                p = str(e)
                self.wfile.write(bytes(p, 'utf-8'))
        else:
            self.wfile.write(b'error2')

        
https = HTTPServer(('localhost', 5000), SipmleHandler)
https.serve_forever()