from django.http import JsonResponse
from django.db.models import Avg, Count, Min, Max, Sum
from .models import MarketStats, VancouverHouse
from util.codes import *
import datetime

def market_trends(request):
    '''
    Get market trends over time
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "Success", "data": {}}
        
        # Get time range from request
        req_dict = request.session.get("req_dict", {})
        start_date = req_dict.get('start_date')
        end_date = req_dict.get('end_date', datetime.date.today())
        
        # Get market trends
        trends = MarketStats.objects.filter(
            date__range=[start_date, end_date]
        ).values('date', 'neighborhood').annotate(
            avg_price=Avg('avg_price'),
            total_listings=Sum('total_listings')
        ).order_by('date')
        
        msg['data']['trends'] = list(trends)
        return JsonResponse(msg)

# Add more market statistics views... 