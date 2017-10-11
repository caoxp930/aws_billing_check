#coding=utf-8


import re
import time
import sendmail
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def initial():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13"
    )
    service_args = ['--proxy=127.0.0.1:1080','--proxy-type=socks5' ]
    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    # options = webdriver.ChromeOptions()
    # options.add_argument('disable-infobars')
    # driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    return driver

# options = webdriver.ChromeOptions()
# options.add_argument('disable-infobars')
# driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.Chrome()
# service_args = ['--proxy=127.0.0.1:1080', '--proxy-type=socks5', ]
# driver = webdriver.PhantomJS(service_args=service_args)
# driver=webdriver.PhantomJS()


def login_aws():
    year,month = time.localtime()[0],time.localtime()[1]
    driver.get('https://console.aws.amazon.com/billing/home#/bill?year=%s&month=%s'%(year,month))
    a=0
    while a<10:
        try:
            time.sleep(1.5)
            driver.find_element_by_id('resolving_input').send_keys(account)
            driver.find_element_by_id('next_button').click()
            time.sleep(2)
            driver.find_element_by_id('ap_signin1a_pagelet_title')
            driver.find_element_by_id('ap_password').send_keys(pwd)
            driver.find_element_by_id('signInSubmit-input').click()
            driver.save_screenshot('test.png')
            time.sleep(2)
            print 'initial login success'
            return 0
        except:
            time.sleep(1.5)
            a+=1
            #print 'loading'
    return 1

def get_info():
    if login_status == 0:
        a = 0
        while a < 10:
            try:
                element = driver.find_element_by_class_name('icon-plus')
                js = "var q=document.documentElement.scrollTop=100000"
                driver.execute_script(js)
                time.sleep(1)
                driver.save_screenshot('total_billing.png')
                element.click()
                print 'success loading'
                return driver.page_source
            except:
                #print 'loading'
                a += 1
                time.sleep(1)
    else:
        print 'login failed , process stoped'
        driver.quit()
        exit()

def analysis_data():
    pattern =ur'<span class="ng-binding">AWS 服务费</span> <div class="awsui-util-f-r"> <span class="ng-binding">\$(\d*\.\d*)</span> <!-- ngIf: account.fxPaymentInfo.fxEnabled -->'
    info = re.search(pattern,page_source).groups()
    total_billing=info[0]
    print 'Total_Billing：',total_billing
    if float(total_billing) > 0:
        sendmail.send_mail(sender, pwd, recipient, u'费用-$%s'%total_billing, u'费用-$%s'%total_billing)
    pattern = ur'<span class="ng-binding">Bandwidth</span>.*\$(\d*\.\d*)</div> </div> <hr class="region-border-bottom".* <div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-3 awsui-util-t-r ng-binding">' \
             ur'(\d*\.\d*) GB</div> <div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-2 awsui-util-t-r ng-binding">\$(\d*\.\d*)</div>.*' \
             ur'data transfer out under the monthly global free tier</div> <div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-3 awsui-util-t-r ng-binding">(\d*\.\d*) GB</div> ' \
             ur'<div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-2 awsui-util-t-r ng-binding">\$(\d*\.\d*)</div> </div><!-- end ngRepeat: lineitem in instanceLineItemGroup.lineItems -->' \
             ur'<div ng-repeat="lineitem in instanceLineItemGroup.lineItems" class="awsui-row fs-16px ng-scope"> <div class="c-xxs-6 c-xs-6 c-s-6 c-m-6 c-l-7 ng-binding">' \
             ur'\$0.000 per GB - regional data transfer under the monthly global free tier</div> <div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-3 awsui-util-t-r ng-binding">(\d*\.\d*) GB' \
             ur'</div> <div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-2 awsui-util-t-r ng-binding">\$(\d*\.\d*)</div> </div><!-- end ngRepeat: lineitem in instanceLineItemGroup.lineItems -->'
    info=re.search(pattern,page_source).groups()
    # print info
    in_transfer, in_transfer_billing,out_transfer,out_transfer_billing,Bandwidth,Bandwidth_billing = info[1],info[2],info[3],info[4],info[5],info[6]
    print 'IN：', in_transfer,' GB --', in_transfer_billing
    if int(float(in_transfer)) % 5 == 3:
        sendmail.send_mail(sender, pwd, recipient, u'IN已用-%sGB'%in_transfer, u'IN已用-%sGB,费用$%s'%(in_transfer,in_transfer_billing))
    print 'OUT：',   out_transfer,' GB --', out_transfer_billing
    if int(float(out_transfer)) % 5 == 3:
        sendmail.send_mail(sender, pwd, recipient, u'OUT已用-%sGB'%out_transfer, u'OUT已用-%sGB,费用$%s'%(out_transfer,out_transfer_billing))
    print 'Band：', Bandwidth,' GB --',Bandwidth_billing
    if int(float(Bandwidth)) % 5 == 3:
        sendmail.send_mail(sender, pwd, recipient, u'TOTAL已用-%sGB'%Bandwidth, u'TOTAL已用-%sGB,费用$%s'%(Bandwidth,Bandwidth_billing))
    pattern = ur' <!-- ngRepeat: lineitem in instanceLineItemGroup.lineItems --><div ng-repeat="lineitem in instanceLineItemGroup.lineItems" ' \
              ur'class="awsui-row fs-16px ng-scope"> <div class="c-xxs-6 c-xs-6 c-s-6 c-m-6 c-l-7 ng-binding">\$0.00 per GB-month of General Purpose \(SSD\)' \
              ur' provisioned storage under monthly free tier</div> <div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-3 awsui-util-t-r ng-binding">(\d*\.\d*) GB-Mo</div> ' \
              ur'<div class="c-xxs-3 c-xs-3 c-s-3 c-m-3 c-l-2 awsui-util-t-r ng-binding">' \
              ur'\$(\d*\.\d*)</div> </div><!-- end ngRepeat:'
    info = re.search(pattern, page_source).groups()
    SSD,SSD_billing = info[0],info[1]
    print 'SSD used',SSD ,' GB --',SSD_billing
    if int(float(SSD)) % 5 == 3:
        sendmail.send_mail(sender, pwd, recipient, u'SSD已用-%sGB'%SSD, u'SSD已用-%sGB,费用$%s'%(SSD,SSD_billing))
    # js = "var q=document.body.scrollTop=100000"
    # driver.execute_script(js)
    # driver.save_screenshot('test.png')
    # print page_source
    content=u'''Total_Billing：%s,<br> IN： %s GB -- %s<br>OUT：   %s GB -- %s<br>
    Band： %s GB --%s<br>SSD used %s GB -- %s'''\
            %(total_billing,in_transfer,in_transfer_billing,out_transfer,out_transfer_billing,Bandwidth,Bandwidth_billing,SSD,SSD_billing)

    sendmail.send_mail(sender, pwd, recipient, 'AWS Billing',content)


if __name__ == '__main__':
    print '--',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'--'
    account,pwd = '亚马逊账号','密码'
    sender, pwd, recipient = '发件人邮箱', '邮箱认证密码', '收件人',
    driver = initial()
    login_status = login_aws()
    page_source = get_info()
    try:
        analysis_data()
    except:
        print 'login failed , process stoped'
        driver.quit()
        exit()
    time.sleep(5)

    driver.quit()


