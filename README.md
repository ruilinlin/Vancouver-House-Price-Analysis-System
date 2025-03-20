SPIDER
对于温哥华房产数据，我们可以选择几个主要的房产网站来爬取：
Realtor.ca (加拿大最大的房产网站)
REW.ca (温哥华地区专业房产网站)
3. Zillow.com (也覆盖温哥华地区)

django

模型结构:
BaseModel - 基础模型类，提供了通用的CRUD操作方法
config - 配置表模型
users - 管理员表模型
yonghu - 用户表模型
xinfangxinxi - 房价数据模型
systemintro - 系统介绍模型
2. 视图结构:
config_v.py - 配置相关视图
users_v.py - 管理员相关视图
schema_v.py - 数据库模式相关视图
Yonghu_v.py - 用户相关视图
Xinfangxinxi_v.py - 房价数据相关视图
Systemintro_v.py - 系统介绍相关视图
3. 主要功能:
用户认证和权限管理
数据的CRUD操作
文件上传下载
Excel导入导出
数据统计和分析
邮件发送
爬虫集成
4. 特点:
使用了Django的ORM系统
实现了基于类的视图
提供了RESTful风格的API
支持多种数据格式(JSON、Excel等)
集成了Hadoop/Spark功能

