"""     一个用户发送数据的响应时间
        测试多个用户能否都在规定时间内完成发送请求
        能否在稳定的时间内运行一段时间
"""
#输出到日志中
import threading
import requests
import logging
import time
import json
succ=0  #响应成功数
fail=0  #响应失败数

def get_logger():
    logger=logging.getLogger("threading_test")
    logger.setLevel(logging.DEBUG)#级别
    fh=logging.FileHandler("threading.log")
    fmt='%(asctime)s-%(threadName)s-%(levelname)s-%(message)s'
    formatter=logging.Formatter(fmt)#定义输出格式
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
def post_value(url,name,value,apikey,logger):
    global succ
    global fail
    payload=[{'Name':name,'Value':value}]
    try:
        r=requests.post(url,headers=apikey,data=str(payload),timeout=0.10)
        logger.debug("Recive time %f" %(r.elapsed.total_seconds()))
        succ=succ+1
        logger.debug("Succseful %d" % succ)
    except Exception as e:
        logger.debug(e)
        fail=fail+1
        logger.debug("Failed %d" % fail)
if __name__=='__main__':
    logger=get_logger()
    apiurl = "http://www.lewei50.com/api/V1/gateway/UpdateSensors/01"
    #apiheader = {'userkey': '00757a1f7cd34dea88dc52b34aec9d98'}
    apiheaders=[{'userkey': '00757a1f7cd34dea88dc52b34aec9d98'},{'userkey': '00757a1f7cd34dea88dc52b34aec9d98'}]
    names=['D_On-Off','Soil_Humt']
    for i in range(2):
        test_thread=threading.Thread(target=post_value,name=names[i],args=(apiurl,names[i],20,apiheaders[i],logger))
        test_thread.start()
