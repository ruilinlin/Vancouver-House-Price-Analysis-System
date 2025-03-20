#coding:utf-8
__author__ = "ila"
from django.db import models

from .model import BaseModel

from datetime import datetime



class Users(BaseModel):
    """Admin Users Model"""
    __tablename__ = 'users'
    
    username = models.CharField(max_length=100, verbose_name='Username')
    password = models.CharField(max_length=100, verbose_name='Password')
    role = models.CharField(max_length=100, verbose_name='Role')
    email = models.EmailField(max_length=100, null=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Time')

    class Meta:
        db_table = 'users'
        verbose_name = verbose_name_plural = 'Admin Users'

class VancouverHouse(BaseModel):
    """Vancouver Real Estate Data Model"""
    __tablename__ = 'vancouver_houses'
    
    __authTables__ = {}
    __authPeople__ = 'no'
    __sfsh__ = 'no'
    __authSeparate__ = 'no'
    __thumbsUp__ = 'yes'  # Enable likes functionality
    __intelRecom__ = 'yes'  # Enable intelligent recommendations
    __browseClick__ = 'yes'  # Enable view count tracking
    __foreEndListAuth__ = 'no'
    __foreEndList__ = 'yes'  # Show in frontend without login
    __isAdmin__ = 'no'

    # Basic Info
    source = models.CharField(max_length=255, null=True, verbose_name='Source URL')
    title = models.CharField(max_length=255, null=True, verbose_name='Property Title')
    cover_image = models.TextField(null=True, verbose_name='Main Image URL')
    
    # Property Details
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Price (CAD)')
    property_type = models.CharField(max_length=50, null=True, verbose_name='Property Type')
    bedrooms = models.IntegerField(null=True, verbose_name='Bedrooms')
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, verbose_name='Bathrooms')
    living_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Living Area (sq ft)')
    
    # Location
    address = models.CharField(max_length=255, null=True, verbose_name='Address')
    neighborhood = models.CharField(max_length=100, null=True, verbose_name='Neighborhood')
    postal_code = models.CharField(max_length=7, null=True, verbose_name='Postal Code')
    
    # Market Info
    status = models.CharField(max_length=20, default='active', verbose_name='Listing Status')
    listed_date = models.DateField(null=True, verbose_name='Listed Date')
    days_on_market = models.IntegerField(null=True, verbose_name='Days on Market')
    
    # Engagement Metrics
    view_count = models.IntegerField(default=0, verbose_name='View Count')
    like_count = models.IntegerField(default=0, verbose_name='Like Count')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Time')

    class Meta:
        db_table = 'vancouver_houses'
        verbose_name = verbose_name_plural = 'Vancouver Real Estate'

class MarketStats(BaseModel):
    """Vancouver Real Estate Market Statistics"""
    __tablename__ = 'market_stats'

    date = models.DateField(verbose_name='Statistics Date')
    neighborhood = models.CharField(max_length=100, verbose_name='Neighborhood')
    avg_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Average Price')
    median_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Median Price')
    total_listings = models.IntegerField(null=True, verbose_name='Total Listings')
    avg_days_on_market = models.IntegerField(null=True, verbose_name='Average Days on Market')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Record Creation Time')

    class Meta:
        db_table = 'market_stats'
        verbose_name = verbose_name_plural = 'Market Statistics'

class SystemInfo(BaseModel):
    """System Information and Configuration"""
    __tablename__ = 'system_info'

    title = models.CharField(max_length=255, verbose_name='System Title')
    subtitle = models.CharField(max_length=255, verbose_name='System Subtitle')
    content = models.TextField(verbose_name='System Content')
    image1 = models.TextField(null=True, verbose_name='Main Image')
    image2 = models.TextField(null=True, verbose_name='Secondary Image')
    image3 = models.TextField(null=True, verbose_name='Additional Image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Time')

    class Meta:
        db_table = 'system_info'
        verbose_name = verbose_name_plural = 'System Information'
