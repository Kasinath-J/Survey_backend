from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from .models import Layout
from .serializers import LayoutSerializer
from rest_framework import status
from .GSheet.createg import newGSheet
from .GSheet.addg import addGSheet
from .GSheet.fetchg import fetchGSheet
from nested_lookup import nested_lookup
import ast # to convert string to dict


class LayoutList(APIView):
    def get(self, request, format=None):
        Layouts = Layout.objects.all()
        serializer = LayoutSerializer(Layouts, many=True)
        return Response(serializer.data)

class LayoutCreate(APIView):
    def post(self, request, format=None):
        l = Layout(format=request.data)
        l.title = request.data['format']['title']
        l.gsheetId = newGSheet(request.data['format']['title'])
        l.save()
        return Response({"msg":"success"})
    
class LayoutSearch(APIView):
    def post(self, request, format=None):
        l = Layout.objects.filter(gsheetId=request.data['gid'])
        if len(l)==1:
            return Response(l[0].__dict__['format'])
        return Response({"msg":"error"})
    
class LayoutResponse(APIView):
    def post(self, request, format=None):
        gid = request.data['gid']
        l = Layout.objects.filter(gsheetId=gid)
        if len(l)==1:
            # return Response(l[0].__dict__['format'])
            data = l[0].format
            addGSheet(gid,request.data['results'],data)
        return Response({"msg":"success"})
    
class LayoutAnalyse(APIView):
    def post(self, request, format=None):
        gid = request.data['gid']
        ret = {}
        l = Layout.objects.filter(gsheetId=gid)
        json={}
        
        if len(l)!=1:
            return Response({"msg":"error1"})

        json = l[0].format
        
        response = fetchGSheet(gid)
        if "values" not in response:
            return Response({"msg":"error2"})
        
        response = response['values']
        qnans = {}
        
        for i in nested_lookup('elements', json):
            for j in i:
                qnans[j['name']] = {
                    "type":j["type"],
                    "qn":j["title"],
                    "res":[],
                }

        for i in response:
            try:
                i = ast.literal_eval(i[0])
                for key in i:
                    qnans[key]["res"].append(i[key])
            except:
                pass

        # print(qnans)
        for qn in qnans:
            if qnans[qn]['type']=="comment":
                # qnans[qn]['keywords'] = keywords_fn(qnans[qn]["res"])
                # qnans[qn]['summarize'] = summarize_fn(qnans[qn]["res"])
                # qnans[qn]['polarity'] = polarity_fn(qnans[qn]["res"])
                # qnans[qn]['topic_modelling'] = topic_modelling_fn(qnans[qn]["res"])
                print(qnans[qn])

        return Response(qnans)
    
