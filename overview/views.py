from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# Create your views here.

def read_data_from_json(dpath='overview/static/test.json'):

    with open(dpath) as f:
        data = json.load(f)
    return data


@api_view(['GET'])
def overview(request):
    data = read_data_from_json()

    return Response(data)


@api_view(['GET'])
def category_data(request):
    data = read_data_from_json()

    catg_data = dict()
    for item in data:
        if item['category'] in catg_data:
            catg_data[item['category']].append(item)
        else:

            catg_data[item['category']] = [item]

    return Response(catg_data)


@api_view(['GET'])
def date_wise_data(request):
    date = request.GET.get('date')

    data = read_data_from_json()
    date_data = list()
    for item in data:
        if item['date'] == date:
            date_data.append(item)

    return Response(date_data)


@api_view(['GET'])
def date_catg_wise_data(request):
    date, catg = request.GET.get('date'), request.GET.get('catg')

    data = read_data_from_json()
    date_data = list()
    for item in data:
        if item['date'] == date and item['category'] == catg:
            date_data.append(item)

    return Response(date_data)


@api_view(['POST'])
def add_new_item(request):
    data = read_data_from_json()
    new_item = {
        "_id": len(data)+1,
        "item": "Vimbar",
        "category": "daily use",
        "price": "1000",
        "date": "2022-12-30"
    },
    data.append(new_item)
    with open('overview/static/itemsdata.json', 'w') as f:
        f.write(json.dumps(data))
    return Response(new_item)


@api_view(['POST'])
def add_item(request):
    data = read_data_from_json()
    new_item = request.data['item']
    data.append(new_item)
    with open('overview/static/itemsdata.json', 'w') as f:
        f.write(json.dumps(data))
    return Response(new_item)

@api_view(['PATCH'])
def update_item(request):
    data = read_data_from_json()
    idx,upd_name = request.data['idx'],request.data['name']

    item = data[idx]
    item['item'] = upd_name

    with open('overview/static/itemsdata.json', 'w') as f:
        f.write(json.dumps(data))
    return Response(data[idx])
