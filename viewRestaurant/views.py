from django.shortcuts import render
from viewRestaurant.models import Resid
from django.core import serializers


from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import csv
import folium 
import gmplot
import collections
from operator import *
def index(request):
    
        
    Resid.objects.all().delete()
    csvFilePath = "restaurantsa9126b3.csv"
    reader = csv.DictReader(open(csvFilePath))
    frontend_content={}
    for raw in reader:
        name=str(raw['Restaurant Name'])
        color=str(raw['Rating color']).lower().split()
        if len(color)>1:
            color=str("light"+  color[1]) 
        color="".join(map(str,color))      
        frontend_content[int(raw['Restaurant ID'])]={'name':name,'Votes':int(raw['Votes']),'Cuisines':str(raw['Cuisines']),'AverageCostfortwo':int(raw['Average Cost for two']),'Currency':str(raw['Currency']),'HasTablebooking':str(raw['Has Table booking']),'HasOnlinedelivery':str(raw['Has Online delivery']),'Aggregaterating':float(raw['Aggregate rating']),'Ratingcolor':color,'Ratingtext':raw['Rating text']}
    result = collections.OrderedDict(sorted(frontend_content.items(), key=lambda t:t[1]["name"]))
    if request.method == "POST":
            filter_dict={}
            filters = str(request.POST['ResName']).lower().split(",")
            if filters[0] == 'votes':
                result = collections.OrderedDict(sorted(frontend_content.items(), key=lambda t:t[1]["Votes"],reverse=True))  
            if filters[0] == 'rating':
                result = collections.OrderedDict(sorted(frontend_content.items(), key=lambda t:t[1]["Aggregaterating"],reverse=True))
            if filters[0] == 'costfortwo':
                result = collections.OrderedDict(sorted(frontend_content.items(), key=lambda t:t[1]["AverageCostfortwo"]))
            if filters[0]=='cuisines':
                for x in frontend_content.items():
                    if ("".join(map(str,filters[1]))).lower() in x[1]['Cuisines'].lower():
                        filter_dict[x[0]]=x[1]
                        result = collections.OrderedDict(sorted(filter_dict.items(), key=lambda t:t[1]["name"]))
                        print(result)
    return render(request,'index.html',{"frontend_items":result})

def show(request):
    key = Resid.objects.all()
    keys_dict={}
    data_ready_for_json = list( Resid.objects.values())
    val=data_ready_for_json[0]['resid']
    csvFilePath = "restaurant_addc9a1430.csv"
    reader = csv.DictReader(open(csvFilePath))
    for raw in reader:
        if int(raw['Restaurant ID'])==val:
            new={'CountryCode':raw['Country Code'],'City':raw['City'],'Address':raw['Address'],'Locality':raw['Locality Verbose'],'Longitude':float(raw['Longitude']),'Latitude':float(raw['Latitude']),'RestaurantName':"S"}
            keys_dict[data_ready_for_json[0]['resid']]=new
    csvFilePath = "restaurantsa9126b3.csv"
    reader = csv.DictReader(open(csvFilePath))
    for raw in reader:
        if int(raw['Restaurant ID'])==val:
            name=str(raw['Restaurant Name'])
    keys_dict[val]['RestaurantName']=name
    return render(request,'show.html',{'keysdict':keys_dict})

def showkey(request,show_key):
    # print(show_key)
    Resid.objects.create(resid=show_key)
    return HttpResponseRedirect("/show")

def showres(request):
    keys_dict={}
    csvFilePath = "restaurantsa9126b3.csv"
    reader = csv.DictReader(open(csvFilePath))
    if request.method == "POST":
            restaurant = str(request.POST['ResName']).lower()
            for raw in reader:
                if str(raw['Restaurant Name']).lower()==restaurant:
                    val=int(raw['Restaurant ID'])
                    csvFilePath = "restaurant_addc9a1430.csv"
                    reader = csv.DictReader(open(csvFilePath))
                    for raw in reader:
                        if int(raw['Restaurant ID'])==val:
                            new={'CountryCode':raw['Country Code'],'City':raw['City'],'Address':raw['Address'],'Locality':raw['Locality Verbose'],'Longitude':float(raw['Longitude']),'Latitude':float(raw['Latitude']),'RestaurantName':restaurant.upper()}
                    keys_dict[val]=new

    return render(request,'show.html',{'keysdict':keys_dict})   
    
    

    
    

    