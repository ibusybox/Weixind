#!/usr/bin/env python
# coding=utf8

import json
from lxml import etree

'''
weixinzhifu msg output format:
{
    "FromUserName": "",
    "MsgType": 49,
    "NewMsgId": 1021540418019223303,
    "MsgId": 1021540418019223303,
    "ToUserName": ""
    "Url": "https://wx.tenpay.com/cgi-bin/mmpayweb-bin/jumpuserroll?trans_id=4009152001201702241119461424&amp;accid=085e9858e604cdb58be8d40ef",
    "Text": "",
    "CreateTime": 1487911417,
    "Payment": {
    }
}
'''


class WeixinMsgParser:
    def __init__(self):
        self.paymentFuncs = {
            'weixinzhifu': self._getPaymentFromWeixinzhifu
        }

    def parse(self, msgStr, sender):
        originMsg = json.loads(msgStr)
        self.msg = {}
        self.msg["FromUserName"] = originMsg["FromUserName"]
        self.msg["MsgType"] = originMsg["MsgType"]
        self.msg["NewMsgId"] = originMsg["NewMsgId"]
        self.msg["MsgId"] = originMsg["MsgId"]
        self.msg["ToUserName"] = originMsg["ToUserName"]
        self.msg["Url"] = originMsg["Url"]
        self.msg["Text"] = originMsg["Text"]
        self.msg["CreateTime"] = originMsg["CreateTime"]

        self.msg['Payment'] = self._getPayment(originMsg["Content"], sender)

    def getMsg(self):
        return self.msg

    def _getPayment(self, content, sender):
        payment = {}
        payment[u'支付方式'] = ''
        payment[u'商品详情'] = 0
        payment[u'收款单位'] = ''
        payment[u'日期时间'] = ''
        payment[u'交易单号'] = ''
        paymentFunc = self.paymentFuncs.get(sender)
        if sender is None:
            raise "Unknown sender: %s" % sender
        payment = paymentFunc(payment, content)
        return payment

    '''
        付款金额：￥19.00
        商品详情：潘多拉杭州餐厅kc08消费,20170224124335123121908
        支付方式：广发银行
        交易单号：4009152001201702241119461424
        你购买的商品已支付成功，查看详情了解更多信息
    '''
    def _getPaymentFromWeixinzhifu(self, payment, content):
        root = etree.XML(content)
        des = root.xpath('/msg/appmsg/des/text()')[0]
        desLines = des.split('\n')
        rmb = u'￥'
        for line in desLines:
            line = line.strip().strip('\n')
            if not line:
                continue
            kv = line.split(u'：')
            if len(kv) != 2:
                continue
            for k in payment.keys():
                if kv[0] == k:
                    # 从商品详情获取交易时间
                    if u'商品详情' == k:
                        payment[k] = kv[1].split(',')[0]
                        payment[u'日期时间'] = kv[1].split(',')[1]
                    else:
                        payment[k] = kv[1].strip().strip(rmb)
        return payment

if __name__ == '__main__':
    f = '/Users/mao/Desktop/Mao/workspace/1021540418019223303.json'
    with open(f, 'rb') as fp:
        msg = fp.read()
    p = WeixinMsgParser()
    p.parse(msg, 'weixinzhifu')
    with open('/Users/mao/Desktop/Mao/workspace/1.json', 'w+') as fp:
        fp.write(json.dumps(p.getMsg()))
