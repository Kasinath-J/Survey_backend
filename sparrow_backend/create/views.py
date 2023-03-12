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
import requests

from .mlmodels.summarizer import summarizer_fn
from .mlmodels.polarity import polarity_fn
from .mlmodels.keywords import keywords_fn

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
    
def train(gid):
    
    ret = {}
    l = Layout.objects.filter(gsheetId=gid)
    json={}
    
    if len(l)!=1:
        return None

    json = l[0].format
    
    response = fetchGSheet(gid)
    if "values" not in response:
        return None
    
    response = response['values']
    qnans = {}
    
    for i in nested_lookup('elements', json):
        for j in i:
            qnans[j['name']] = {
                "name":j["name"],
                "type":j["type"],
                "qn":j["title"],
                "res":[],
            }
    # qnans['title'] = {json['format']['title']}
    for i in response:
        try:
            i = ast.literal_eval(i[0])
            for key in i:
                qnans[key]["res"].append(i[key])
        except:
            pass

    for qn in qnans:
        if qnans[qn]['type']=="comment":
            actual_qn = qnans[qn]['qn'].upper()
            query = "REVIEW"
            if query in actual_qn:
                (rating_count,positive,negative) = polarity_fn(qnans[qn]["res"])
                qnans[qn]['polarity'] = rating_count
                qnans[qn]['positive_keywords'] = keywords_fn(positive)
                qnans[qn]['negative_keywords'] = keywords_fn(negative)
                qnans[qn]['comment_type'] = "bi"
            else:
                temp = keywords_fn(qnans[qn]["res"])
                qnans[qn]['keywords'] = temp
                qnans[qn]['summarize'] = summarizer_fn(qnans[qn]["res"])
                qnans[qn]['comment_type'] = "uni"

    return qnans


class LayoutTrain(APIView):
    def post(self, request, format=None):
        gid = request.data['gid']
        l = Layout.objects.filter(gsheetId=gid)
        if len(l)==1:
            qnans = train(gid)
            l[0].train = qnans
            l[0].save()
            return Response({"msg":"success"})
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
        l = Layout.objects.filter(gsheetId=gid)
        qnans = None
        if len(l)==1:
            if l[0].train==None:
                qnans = train(gid)
                l[0].train = qnans
                l[0].save()
            else:
                qnans = l[0].train
        return Response(qnans)
    
