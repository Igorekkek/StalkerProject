import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .utils import find_anomally, swans_visualization
import requests

class AddNewDataView(APIView):
    def post(self, request):
        # print(request.data, sep='\n')

        for det in request.data:
            obj = Detector.objects.create(idd=det['id'], x=det['coords'][0], y=det['coords'][1])
            for swan in det['swans']:
                swan_obj, _ = Swan.objects.get_or_create(idd=swan['id'])
                obj.swans.add(swan_obj)
        
        for obj in Swan.objects.all():
            if not (obj.int0 is None):
                continue

            local_data = []
            for det in request.data:
                for swan in det['swans']:
                    if obj.idd == swan['id']:
                        local_data.append([swan['rate'], det['coords'][0], det['coords'][1]])
                        break
            if local_data.__len__() < 3:
                raise ValueError('ейс минус 3, ухух')
            obj.x, obj.y, obj.int0 = find_anomally(*local_data[0], *local_data[1], *local_data[2])
            obj.save()
            
        swans_visualization(Swan.objects.all())
        return Response({'post' : 'ok'})
