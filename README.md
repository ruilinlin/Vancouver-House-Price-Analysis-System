# Vancouver Real Estate Analytics Platform 

A comprehensive real estate analytics platform for Vancouver housing market, built with Django.

## Overview

This platform provides real-time analytics, market trends, and detailed property information for the Vancouver real estate market. It includes features such as property listing management, market statistics, and automated data collection.

## Features

- **Property Management**
  - Real-time property listings
  - Detailed property information
  - Advanced search and filtering
  - Property view tracking

- **Market Analytics**
  - Market trend analysis
  - Neighborhood statistics
  - Price predictions
  - Interactive data visualization

- **User System**
  - User authentication
  - Role-based access control
  - User activity tracking
  - Customizable user preferences

- **Data Collection**
  - Automated web scraping from:
    - Realtor.ca
    - REW.ca
    - Zillow.com
  - Data validation
  - Regular updates
  - Historical data tracking

## Tech Stack

- **Backend**: Django 3.x
- **Database**: MySQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Web Scraping**: Scrapy
- **API**: RESTful

## Project Structure

Django/
├── main/                   # Main application
│   ├── models.py          # Database models (VancouverHouse, MarketStats, etc.)
│   ├── vancouver_house_v.py # Property views
│   ├── market_stats_v.py  # Market statistics views
│   ├── system_info_v.py   # System information views
│   ├── users_v.py         # User management views
│   ├── urls.py            # URL configurations
│   └── utils/             # Utility functions
├── spider/                # Web scraping components
├── templates/             # HTML templates
└── static/               # Static files