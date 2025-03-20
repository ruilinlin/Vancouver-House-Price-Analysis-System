from django.http import JsonResponse
from django.db.models import Q, Avg, Count, Sum
from django.core.paginator import Paginator
from .models import VancouverHouse, MarketStats
from util.codes import *
from util.auth import Auth
from util import message as mes
import datetime

def vancouver_house_list(request):
    '''
    Get list of properties
    Returns a filtered list of real estate properties
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": []}
        req_dict = request.session.get("req_dict", {})

        # Build filter conditions
        filters = Q()
        if req_dict.get('neighborhood'):
            filters &= Q(neighborhood=req_dict['neighborhood'])
        if req_dict.get('property_type'):
            filters &= Q(property_type=req_dict['property_type'])
        if req_dict.get('price_min'):
            filters &= Q(price__gte=req_dict['price_min'])
        if req_dict.get('price_max'):
            filters &= Q(price__lte=req_dict['price_max'])

        # Get results
        houses = VancouverHouse.objects.filter(filters)
        msg['data'] = [house.to_dict() for house in houses]
        
        return JsonResponse(msg)

def vancouver_house_page(request):
    '''
    Get paginated list of properties
    Returns paginated results with filtering options
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", 
               "data": {"current_page": 1, "total_pages": 1, "total": 1, "page_size": 10, "list": []}}
        
        req_dict = request.session.get("req_dict", {})
        
        # Build filter conditions
        filters = Q()
        if req_dict.get('neighborhood'):
            filters &= Q(neighborhood=req_dict['neighborhood'])
        if req_dict.get('property_type'):
            filters &= Q(property_type=req_dict['property_type'])
        if req_dict.get('price_min'):
            filters &= Q(price__gte=req_dict['price_min'])
        if req_dict.get('price_max'):
            filters &= Q(price__lte=req_dict['price_max'])

        # Get paginated results
        page = int(req_dict.get('page', 1))
        page_size = int(req_dict.get('page_size', 10))
        
        start = (page-1) * page_size
        houses = VancouverHouse.objects.filter(filters)
        total = houses.count()
        
        if start > total:
            start = 0
            page = 1
            
        results = houses[start:start + page_size]
        
        msg['data']['list'] = [house.to_dict() for house in results]
        msg['data']['current_page'] = page
        msg['data']['total_pages'] = total // page_size + (1 if total % page_size > 0 else 0)
        msg['data']['total'] = total
        msg['data']['page_size'] = page_size
        
        return JsonResponse(msg)

def vancouver_house_info(request, id_):
    '''
    Get basic property information
    Returns basic details of a specific property
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": {}}
        
        try:
            house = VancouverHouse.objects.get(id=id_)
            msg['data'] = house.to_dict()
        except VancouverHouse.DoesNotExist:
            msg['code'] = other_code
            msg['msg'] = "Property not found"
            
        return JsonResponse(msg)

def vancouver_house_detail(request, id_):
    '''
    Get detailed property information
    Returns comprehensive details of a property with view tracking
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": {}}
        
        try:
            house = VancouverHouse.objects.get(id=id_)
            # Increment view count
            house.view_count += 1
            house.save()
            
            msg['data'] = house.to_dict()
        except VancouverHouse.DoesNotExist:
            msg['code'] = other_code
            msg['msg'] = "Property not found"
            
        return JsonResponse(msg)

def vancouver_house_save(request):
    '''
    Save new property
    Creates a new property listing
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": {}}
        req_dict = request.session.get("req_dict")

        try:
            house = VancouverHouse.objects.create(**req_dict)
            msg['data'] = house.to_dict()
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = str(e)
            
        return JsonResponse(msg)

def vancouver_house_update(request):
    '''
    Update property information
    Updates an existing property listing
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": {}}
        req_dict = request.session.get("req_dict")

        try:
            house = VancouverHouse.objects.get(id=req_dict.get('id'))
            for key, value in req_dict.items():
                if hasattr(house, key):
                    setattr(house, key, value)
            house.save()
            msg['data'] = house.to_dict()
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = str(e)
            
        return JsonResponse(msg)

def vancouver_house_delete(request):
    '''
    Delete property
    Removes a property listing
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success"}
        req_dict = request.session.get("req_dict")

        try:
            ids = req_dict.get("ids")
            if isinstance(ids, str):
                ids = [int(id_) for id_ in ids.split(',')]
            VancouverHouse.objects.filter(id__in=ids).delete()
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = str(e)
            
        return JsonResponse(msg)

def vancouver_house_search(request):
    '''
    Advanced property search
    Provides advanced search functionality with multiple criteria
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": []}
        req_dict = request.session.get("req_dict", {})

        filters = Q()
        # Add search criteria
        if req_dict.get('keyword'):
            keyword = req_dict['keyword']
            filters |= Q(title__icontains=keyword)
            filters |= Q(address__icontains=keyword)
            filters |= Q(neighborhood__icontains=keyword)
            
        # Add other filters
        if req_dict.get('price_range'):
            min_price, max_price = req_dict['price_range']
            filters &= Q(price__gte=min_price) & Q(price__lte=max_price)
            
        if req_dict.get('property_types'):
            filters &= Q(property_type__in=req_dict['property_types'])
            
        if req_dict.get('bedrooms'):
            filters &= Q(bedrooms=req_dict['bedrooms'])
            
        # Get results
        houses = VancouverHouse.objects.filter(filters)
        msg['data'] = [house.to_dict() for house in houses]
        
        return JsonResponse(msg)
