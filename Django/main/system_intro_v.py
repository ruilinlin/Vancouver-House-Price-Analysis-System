#coding:utf-8
__author__ = "ila"
import base64, copy, logging, os, sys, time, xlrd, json, datetime, configparser
from django.http import JsonResponse
from django.apps import apps
from django.db.models.aggregates import Count,Sum
from .models import SystemInfo
from util.codes import *
from util.auth import Auth
from util.common import Common
import util.message as mes
from django.db import connection
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q, Avg
from util.baidubce_api import BaiDuBce
from .config_model import config

from dj2.settings import executor
from util.spark_func import spark_read_mysql






def systemintro_register(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")


        error = SystemInfo.createbyreq(SystemInfo, SystemInfo, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = "用户已存在,请勿重复注册!"
        return JsonResponse(msg)

def systemintro_login(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")

        datas = SystemInfo.getbyparams(SystemInfo, SystemInfo, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg)
        try:
            __sfsh__= SystemInfo.__sfsh__
        except:
            __sfsh__=None

        if  __sfsh__=='是':
            if datas[0].get('sfsh')!='yes':
                msg['code']=other_code
                msg['msg'] = "account locked, please contact admin for approval!"
                return JsonResponse(msg)
                
        req_dict['id'] = datas[0].get('id')


        return Auth.authenticate(Auth, SystemInfo, req_dict)


def systemintro_logout(request):
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "登出成功",
            "code": 0
        }

        return JsonResponse(msg)


def systemintro_resetPass(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}

        req_dict = request.session.get("req_dict")

        columns=  SystemInfo.getallcolumn( SystemInfo, SystemInfo)

        try:
            __loginUserColumn__= SystemInfo.__loginUserColumn__
        except:
            __loginUserColumn__=None
        username=req_dict.get(list(req_dict.keys())[0])
        if __loginUserColumn__:
            username_str=__loginUserColumn__
        else:
            username_str=username
        if 'mima' in columns:
            password_str='mima'
        else:
            password_str='password'

        init_pwd = '123456'
        recordsParam = {}
        recordsParam[username_str] = req_dict.get("username")
        records=SystemInfo.getbyparams(SystemInfo, SystemInfo, recordsParam)
        if len(records)<1:
            msg['code'] = 400
            msg['msg'] = 'user not found'
            return JsonResponse(msg)

        eval('''SystemInfo.objects.filter({}='{}').update({}='{}')'''.format(username_str,username,password_str,init_pwd))
        
        return JsonResponse(msg)



def systemintro_session(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}

        req_dict={"id":request.session.get('params').get("id")}
        msg['data']  = SystemInfo.getbyparams(SystemInfo, SystemInfo, req_dict)[0]

        return JsonResponse(msg)


def systemintro_default(request):

    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        req_dict.update({"isdefault":"是"})
        data=SystemInfo.getbyparams(SystemInfo, SystemInfo, req_dict)
        if len(data)>0:
            msg['data']  = data[0]
        else:
            msg['data']  = {}
        return JsonResponse(msg)

def systemintro_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  SystemInfo.getallcolumn( SystemInfo, SystemInfo)

        #当前登录用户所在表
        tablename = request.session.get("tablename")


            #authColumn=list(__authTables__.keys())[0]
            #authTable=__authTables__.get(authColumn)

            # if authTable==tablename:
                #params = request.session.get("params")
                #req_dict[authColumn]=params.get(authColumn)

        '''__authSeparate__此属性为真，params添加userid，后台只查询个人数据'''
        try:
            __authSeparate__=SystemInfo.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="yes":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        #当项目属性hasMessage为"是"，生成系统自动生成留言板的表messages，同时该表的表属性hasMessage也被设置为"是",字段包括userid（用户id），username(用户名)，content（留言内容），reply（回复）
        #接口page需要区分权限，普通用户查看自己的留言和回复记录，管理员查看所有的留言和回复记录
        try:
            __hasMessage__=SystemInfo.__hasMessage__
        except:
            __hasMessage__=None
        if  __hasMessage__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict["userid"]=request.session.get("params").get("id")



        # 判断当前表的表属性isAdmin,为真则是管理员表
        # 当表属性isAdmin="是",刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
        __isAdmin__ = None

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        # 当前表也是有管理员权限的表
        if  __isAdmin__ == "是" and 'SystemInfo' != 'forum':
            if req_dict.get("userid") and 'SystemInfo' != 'chat':
                del req_dict["userid"]

        else:
            #非管理员权限的表,判断当前表字段名是否有userid
            if tablename!="users" and 'SystemInfo'[:7]!='discuss'and "userid" in SystemInfo.getallcolumn(SystemInfo,SystemInfo):
                req_dict["userid"] = request.session.get("params").get("id")

        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为"是"，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=SystemInfo.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __isAdmin__ == "是":
            try:
                del req_dict['userid']
                # tablename=request.session.get("tablename")
                # if tablename=="users":
                    # del req_dict['userid']
                
            except:
                pass
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break


        q = Q()

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =SystemInfo.page(SystemInfo, SystemInfo, req_dict, request, q)

        return JsonResponse(msg)

def systemintro_autoSort(request):
    '''
    smart recommendation function
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in SystemInfo.getallcolumn(SystemInfo,SystemInfo):
            req_dict['sort']='clicknum'
        elif "browseduration"  in SystemInfo.getallcolumn(SystemInfo,SystemInfo):
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = SystemInfo.page(SystemInfo,SystemInfo, req_dict)

        return JsonResponse(msg)


def systemintro_list(request):
    '''
    前台分页
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if req_dict.__contains__('vipread'):
            del req_dict['vipread']

        #获取全部列名
        columns=  SystemInfo.getallcolumn( SystemInfo, SystemInfo)
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=SystemInfo.__foreEndList__
        except:
            __foreEndList__=None

        if __foreEndList__=="前要登":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass
        #forrEndListAuth
        try:
            __foreEndListAuth__=SystemInfo.__foreEndListAuth__
        except:
            __foreEndListAuth__=None


        #authSeparate
        try:
            __authSeparate__=SystemInfo.__authSeparate__
        except:
            __authSeparate__=None

        if __foreEndListAuth__ =="yes" and __authSeparate__=="yes":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params",{"id":0}).get("id")

        tablename = request.session.get("tablename")
        if tablename == "users" and req_dict.get("userid") != None:#判断是否存在userid列名
            del req_dict["userid"]
        else:
            __isAdmin__ = None

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                if m.__tablename__==tablename:

                    try:
                        __isAdmin__ = m.__isAdmin__
                    except:
                        __isAdmin__ = None
                    break

            if __isAdmin__ == "yes":
                if req_dict.get("userid"):
                    # del req_dict["userid"]
                    pass
            else:
                #非管理员权限的表,判断当前表字段名是否有userid
                if "userid" in columns:
                    try:
                        pass
                    except:
                            pass
        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为"是"，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=SystemInfo.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __foreEndListAuth__=="yes":
            try:
                del req_dict['userid']
            except:
                pass
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        
        if SystemInfo.__tablename__[:7]=="discuss":
            try:
                del req_dict['userid']
            except:
                pass


        q = Q()

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = SystemInfo.page(SystemInfo, SystemInfo, req_dict, request, q)

        return JsonResponse(msg)

def systemintro_save(request):
    '''
    后台新增
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys():
            del req_dict['clicktime']
        tablename=request.session.get("tablename")
        __isAdmin__ = None
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break


        #获取全部列名
        columns=  SystemInfo.getallcolumn( SystemInfo, SystemInfo)
        if tablename!='users' and req_dict.get("userid")!=None and 'userid' in columns  and __isAdmin__!='yes':
            params=request.session.get("params")
            req_dict['userid']=params.get('id')


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']

        error= SystemInfo.createbyreq(SystemInfo,SystemInfo, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def systemintro_add(request):
    '''
    前台新增
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        #获取全部列名
        columns=  SystemInfo.getallcolumn( SystemInfo, SystemInfo)
        try:
            __authSeparate__=SystemInfo.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="yes":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        try:
            __foreEndListAuth__=SystemInfo.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="no":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params").get("id")


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']
        error= SystemInfo.createbyreq(SystemInfo,SystemInfo, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)

def systemintro_thumbsup(request,id_):
    '''
     点赞：表属性thumbsUp[是/否]，刷表新增thumbsupnum赞和crazilynum踩字段，
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=SystemInfo.getbyid(SystemInfo,SystemInfo,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = SystemInfo.updatebyparams(SystemInfo,SystemInfo, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def systemintro_info(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = SystemInfo.getbyid(SystemInfo,SystemInfo, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
        #浏览点击次数
        try:
            __browseClick__= SystemInfo.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="yes"  and  "clicknum"  in SystemInfo.getallcolumn(SystemInfo,SystemInfo):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}
            ret=SystemInfo.updatebyparams(SystemInfo,SystemInfo,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)

def systemintro_detail(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =SystemInfo.getbyid(SystemInfo,SystemInfo, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")

        #浏览点击次数
        try:
            __browseClick__= SystemInfo.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="yes"   and  "clicknum"  in SystemInfo.getallcolumn(SystemInfo,SystemInfo):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}

            ret=SystemInfo.updatebyparams(SystemInfo,SystemInfo,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = retfo
        return JsonResponse(msg)


def systemintro_update(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if req_dict.get("mima") and "mima" not in SystemInfo.getallcolumn(SystemInfo,SystemInfo) :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in SystemInfo.getallcolumn(SystemInfo,SystemInfo) :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass


        error = SystemInfo.updatebyparams(SystemInfo, SystemInfo, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def systemintro_delete(request):
    '''
    批量删除
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        error=SystemInfo.deletes(SystemInfo,
            SystemInfo,
             req_dict.get("ids")
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def systemintro_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= SystemInfo.getbyid(SystemInfo, SystemInfo, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=SystemInfo.updatebyparams(SystemInfo,SystemInfo,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)

def systemintro_importExcel(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}

        excel_file = request.FILES.get("file", "")
        file_type = excel_file.name.split('.')[1]
        
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            table = data.sheets()[0]
            rows = table.nrows
            
            try:
                for row in range(1, rows):
                    row_values = table.row_values(row)
                    req_dict = {}
                    SystemInfo.createbyreq(SystemInfo, SystemInfo, req_dict)
                    
            except:
                pass
                
        else:
            msg = {
                "msg": "file type error",
                "code": 500
            }
                
        return JsonResponse(msg)

def systemintro_sendemail(request):
    if request.method in ["POST", "GET"]:
        req_dict = request.session.get("req_dict")

        code = random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
        to = []
        to.append(req_dict['email'])

        send_mail('用户注册', '您的注册验证码是【'+''.join(code)+'】，请不要把验证码泄漏给其他人，如非本人请勿操作。', 'yclw9@qq.com', to, fail_silently = False)

        cursor = connection.cursor()
        cursor.execute("insert into emailregistercode(email,role,code) values('"+req_dict['email']+"','用户','"+''.join(code)+"')")

        msg = {
            "msg": "send success",
            "code": 0
        }

        return JsonResponse(msg)

def systemintro_autoSort2(request):
    return JsonResponse({"code": 0, "msg": '',  "data":{}})

# （按值统计）时间统计类型
def systemintro_value(request, xColumnName, yColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}
        
        where = ' where 1 = 1 '
        sql = ''
        if timeStatType == '日':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM SystemInfo {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d') LIMIT 10".format(xColumnName, yColumnName, where, '%Y-%m-%d')

        if timeStatType == '月':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM SystemInfo {2} GROUP BY DATE_FORMAT({0}, '%Y-%m') LIMIT 10".format(xColumnName, yColumnName, where, '%Y-%m')

        if timeStatType == '年':
            sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM SystemInfo {2} GROUP BY DATE_FORMAT({0}, '%Y') LIMIT 10".format(xColumnName, yColumnName, where, '%Y')

        func_name = sys._getframe().f_code.co_name
        table_name = func_name.split('_')[0]
        json_filename=f'{table_name}_value_{xColumnName}_{yColumnName}.json'
        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'] = L
        executor.submit(spark_read_mysql, f"({sql}) {table_name}", json_filename)
        return JsonResponse(msg)

# 按值统计
def systemintro_o_value(request, xColumnName, yColumnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}
        
        where = ' where 1 = 1 '
        
        sql = "SELECT {0}, sum({1}) AS total FROM SystemInfo {2} GROUP BY {0} LIMIT 10".format(xColumnName, yColumnName, where)
        func_name = sys._getframe().f_code.co_name
        table_name = func_name.split('_')[0]
        json_filename =  f'{table_name}_o_value_{xColumnName}_{yColumnName}.json'
        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'] = L
        executor.submit(spark_read_mysql, f"({sql}) {table_name}", json_filename)
        return JsonResponse(msg)

# （按值统计）时间统计类型(多)
def systemintro_valueMul(request, xColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": []}

        req_dict = request.session.get("req_dict")

        where = ' where 1 = 1 '
        
        for item in req_dict['yColumnNameMul'].split(','):
            sql = ''
            if timeStatType == '日':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM SystemInfo {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d') LIMIT 10".format(xColumnName, item, where, '%Y-%m-%d')

            if timeStatType == '月':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM SystemInfo {2} GROUP BY DATE_FORMAT({0}, '%Y-%m') LIMIT 10".format(xColumnName, item, where, '%Y-%m')

            if timeStatType == '年':
                sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM SystemInfo {2} GROUP BY DATE_FORMAT({0}, '%Y') LIMIT 10".format(xColumnName, item, where, '%Y')

            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'].append(L)
        return JsonResponse(msg)

# （按值统计(多)）
def systemintro_o_valueMul(request, xColumnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": []}

        req_dict = request.session.get("req_dict")
        
        where = ' where 1 = 1 '

        for item in req_dict['yColumnNameMul'].split(','):
            sql = "SELECT {0}, sum({1}) AS total FROM SystemInfo {2} GROUP BY {0} LIMIT 10".format(xColumnName, item, where)
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'].append(L)

        return JsonResponse(msg)






def systemintro_group(request, columnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}
        
        where = ' where 1 = 1 '

        sql = "SELECT COUNT(*) AS total, " + columnName + " FROM SystemInfo " + where + " GROUP BY " + columnName + " LIMIT 10"

        func_name = sys._getframe().f_code.co_name
        table_name = func_name.split('_')[0]

        json_filename=f'{table_name}_group_{columnName}.json'
        if os.path.exists(json_filename)==True:
            with open(json_filename,encoding='utf-8') as f:
                msg['data']=json.load(f)
        else:
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime("%Y-%m-%d")
                    else:
                        pass
                L.append(online_dict)
            msg['data'] = L
        executor.submit(spark_read_mysql, f"({sql}) {table_name}",json_filename)
        return JsonResponse(msg)










def system_info(request):
    '''
    Get system information
    Returns basic system configuration and content
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}
        
        try:
            # Get the latest system info
            info = SystemInfo.objects.latest('created_at')
            msg['data'] = {
                'title': info.title,
                'subtitle': info.subtitle,
                'content': info.content,
                'images': [
                    info.image1,
                    info.image2,
                    info.image3
                ],
                'last_updated': info.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        except SystemInfo.DoesNotExist:
            msg['code'] = other_code
            msg['msg'] = "System information not found"
        
        return JsonResponse(msg)

def system_update(request):
    '''
    Update system information
    Allows admin users to update system content and configuration
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = request.session.get("req_dict")

        try:
            # Check if system info exists
            if SystemInfo.objects.exists():
                info = SystemInfo.objects.latest('created_at')
                
                # Update fields
                for key, value in req_dict.items():
                    if hasattr(info, key):
                        setattr(info, key, value)
                info.save()
            else:
                # Create new system info
                info = SystemInfo.objects.create(**req_dict)
            
            msg['data'] = {
                'id': info.id,
                'title': info.title,
                'subtitle': info.subtitle,
                'content': info.content,
                'updated_at': info.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = str(e)
        
        return JsonResponse(msg)

def system_stats(request):
    '''
    Get system statistics
    Returns key metrics about the Vancouver real estate platform
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "success", "data": {}}
        
        try:
            from .models import VancouverHouse, MarketStats
            
            # Get platform statistics
            msg['data'] = {
                'total_listings': VancouverHouse.objects.count(),
                'active_listings': VancouverHouse.objects.filter(status='active').count(),
                'total_neighborhoods': VancouverHouse.objects.values('neighborhood').distinct().count(),
                'avg_price': VancouverHouse.objects.aggregate(avg_price=Avg('price'))['avg_price'],
                'last_updated': MarketStats.objects.latest('date').date.strftime("%Y-%m-%d") if MarketStats.objects.exists() else None,
                'platform_stats': {
                    'total_users': VancouverHouse.objects.values('user').distinct().count(),
                    'total_views': VancouverHouse.objects.aggregate(total_views=Sum('view_count'))['total_views'],
                    'total_likes': VancouverHouse.objects.aggregate(total_likes=Sum('like_count'))['total_likes']
                }
            }
        except Exception as e:
            msg['code'] = other_code
            msg['msg'] = str(e)
            
        return JsonResponse(msg)

def system_version(request):
    '''
    Get system version information
    Returns current version and deployment details
    '''
    if request.method in ["POST", "GET"]:
            msg = {"code": normal_code, "msg": "success", "data": {}}
        
        try:
            msg['data'] = {
                'version': '2025.1.0',
                'platform': 'Vancouver Real Estate Analytics',
                'last_update': datetime.now().strftime("%Y-%m-%d"),
                'features': [
                    'Real-time market analysis',
                    'Neighborhood statistics',
                    'Price trend predictions',
                    'Interactive property maps'
                ]
            }
        except Exception as e:
            msg['code'] = other_code
            msg['msg'] = str(e)
            
        return JsonResponse(msg)









