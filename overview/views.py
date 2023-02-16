from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from datetime import datetime as dt
from pymongo import MongoClient
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail



# Create your views here.

def read_data_from_json(dpath='overview/static/itemsdata.json'):

    with open(dpath) as f:
        data = json.load(f)
    return data


def connect_mongo(db_name='test'):
    client=MongoClient('mongodb+srv://test_db_user:wy1d3VNenoBmkfx5@cluster0.ohz7z5a.mongodb.net/?retryWrites=true&w=majority')
    db=client[db_name]

    return client,db


@api_view(['GET'])
def overview(request):
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    data=list()
    for item in all_items:
        item['_id']= str(item['_id'])
        data.append(item)

    client.close()
    return Response(data)    


@api_view(['GET'])
def category_data(request):
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    catg_data = dict()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['category'] in catg_data:
            [catg_data[item['category']]].append(item)
        else:
            catg_data[item['category']]=(item)
    client.close()        
    return Response(catg_data)            


@api_view(['GET'])
def date_wise_data(request):
    date = request.GET.get('date')
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    date_data = list()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['date']==date:
            date_data.append(item)  
    client.close()        
    return Response((date_data))        


@api_view(['GET'])
def date_catg_wise_data(request):
    date, catg = request.GET.get('date'), request.GET.get('catg')
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    date_catg_data = list()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['date'] == date and item['category'] == catg:
            date_catg_data.append(item)
    client.close()        
    return Response(date_catg_data)         


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

    client,db = connect_mongo()
    collection = db['items']

    new_item = request.data['item']
    collection.insert_one(new_item)

    send_mail(
        'New Add item', #Subject
        f":{new_item}",  #body
        'rachitsingh06938@gmail.com',  #username
        ['mukeshsingh08082002@gmail.com'], #jis pe mail send karna hai
        fail_silently=False,
    )
    print("send email successfully")
    new_item["_id"]=str(new_item["_id"])
    client.close() 
    return Response({'added_item':new_item})


@api_view(['PATCH'])
def update_item(request):

    client,db = connect_mongo()
    collection = db['items']
    
    update_item= request.data.get('update_item')
    id=update_item['_id']
    del update_item['_id']

    result=collection.update_one({'_id':ObjectId(id)},{"$set":update_item})
    client.close()
    return Response(result.modified_count) 


@api_view(['GET']) # Date ke item ka maximum price.
def date_max_itm_price(request):
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    max=0
    itm=''
    date= request.GET.get('date')
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['date']==date and int(item['price'])>max:
            max=int(item['price'])
            itm=item['item']
            category=item['category']
    client.close()        
    return Response({category:{'item':itm,'Maximum_Price':max}})


@api_view(['GET']) #Count item and price
def count_itm(request):
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    count_dict=dict()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['item'] in count_dict:
            count_dict[item['item']]['count']+=1
            count_dict[item['item']]['price']+=int(item['price'])
        else:
            count_dict[item['item']]={'count':1,'price':int(item['price'])}
    client.close()             
    return Response(count_dict)
                                   
@api_view(['GET']) #Count item_price and latest_date
def cunt_itm_price(request):
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    latest_date=dict()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['item'] in latest_date:
            latest_date[item['item']]['count']+=1
            latest_date[item['item']]['price']+=int(item['price'])
            latest_date[item['item']]['date']=max(dt.strptime(latest_date[item['item']]['date'],'%Y-%m-%d'),
                                                   dt.strptime(item['date'],'%Y-%m-%d')).strftime('%Y-%m-%d')
        else:
            latest_date[item['item']]={'count':1,'price':int(item['price']),
                                        'date':item['date']}
    client.close()                                    
    return Response(latest_date)                                                                               


@api_view(['GET']) # latest_date and item
def latest_date(request):
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['date']<=dt.strftime(dt.today(),'%Y-%m-%d'):
            l_d={item['date']:[{'item':item['item'],'price':item['price']}]}
    client.close()        
    return Response(l_d)
                                      

@api_view(['GET']) #Particular_date_data
def Particular_date_data(request):
    date = request.GET.get('date')
    client,db = connect_mongo()
    collection = db['items']

    all_items=collection.find()
    parti_det=dict()
    for item in all_items:
        item['_id']= str(item['_id'])
        if item['date']==date:
            if item['date'] in parti_det:
                parti_det[item['date']]['item'].append([item['item']])
                parti_det[item['date']]['total_item']+=1
                parti_det[item['date']]['total_price']+=int(item['price'])
            else:
                parti_det[item['date']]={'total_item':1,
                                          'total_price':int(item['price']),
                                         'item':[item['item']],}
    client.close()                                     
    return Response(parti_det)                                         


@api_view(['GET'])
def filter_catg(request):#filter_catg
    catg = request.data.get('catg_filter',[])
    if not catg:
        return Response({"error": "category data not received"})

    client, db = connect_mongo()
    collection = db['items']
    result = {}
    
    all_items = collection.find({'category': {'$in': catg}})
    for item in all_items:
        item['_id'] = str(item['_id'])
        result[item['_id']] = item
        
    client.close()
    return Response(result)

