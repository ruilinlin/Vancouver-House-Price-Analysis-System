import scrapy
from ..items import VancouverHouseItem  # 注意这里改用新的Item类
import re
import json
from datetime import datetime

class VancouverHouseSpider(scrapy.Spider):
    name = 'vancouver_house'  # 爬虫名称，用于运行爬虫时识别
    # REW.ca的搜索页面URL
    base_url = 'https://www.rew.ca/properties/search/results'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 可以在这里初始化一些变量
        self.search_params = {
            'initial_search_method': 'criteria',
            'query': 'Vancouver, BC',
            'searchable_id': '361',
            'searchable_type': 'Geography'
        }

    def start_requests(self):
        """
        爬虫的入口点，生成初始请求
        """
        # 构建初始URL
        url = f"{self.base_url}?{self.get_query_string()}&page=1"
        
        # 添加headers模拟浏览器行为
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        """
        解析列表页面
        """
        # 获取所有房产列表项
        listings = response.css('div.listingCard')
        
        for listing in listings:
            item = VancouverHouseItem()
            
            # 提取基本信息
            item['title'] = self.clean_text(listing.css('.listingCard-title::text').get())
            item['price'] = self.clean_text(listing.css('.listingCard-price::text').get())
            item['address'] = self.clean_text(listing.css('.listingCard-address::text').get())
            
            # 获取详情页URL
            detail_url = listing.css('a.listingCard-link::attr(href)').get()
            if detail_url:
                full_url = response.urljoin(detail_url)
                item['source'] = full_url
                
                # 请求详情页
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_detail,
                    meta={'item': item}
                )

        # 处理分页
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse
            )

    def parse_detail(self, response):
        """
        解析详情页面
        """
        item = response.meta['item']
        
        # 提取详细信息
        item['living_area'] = self.extract_area(
            response.css('.propertyDetails-feature-living-area::text').get()
        )
        item['property_type'] = self.clean_text(
            response.css('.propertyDetails-type::text').get()
        )
        item['bedrooms'] = self.extract_number(
            response.css('.propertyDetails-feature-beds::text').get()
        )
        item['bathrooms'] = self.extract_number(
            response.css('.propertyDetails-feature-baths::text').get()
        )
        item['neighborhood'] = self.clean_text(
            response.css('.propertyDetails-neighborhood::text').get()
        )
        item['listed_date'] = self.clean_text(
            response.css('.propertyDetails-date::text').get()
        )
        
        yield item

    def clean_text(self, text):
        """
        清理文本数据
        """
        if text:
            return text.strip()
        return ''

    def extract_area(self, text):
        """
        提取面积数字
        """
        if text:
            match = re.search(r'[\d,]+', text)
            if match:
                return match.group().replace(',', '')
        return ''

    def extract_number(self, text):
        """
        提取数字
        """
        if text:
            match = re.search(r'[\d.]+', text)
            if match:
                return match.group()
        return ''

    def get_query_string(self):
        """
        构建查询参数
        """
        return '&'.join([f"{k}={v}" for k, v in self.search_params.items()]) 