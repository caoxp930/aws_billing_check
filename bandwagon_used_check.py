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
    # service_args = ['--proxy=127.0.0.1:1080','--proxy-type=socks5' ]
    #driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    return driver

def login():
    driver.get('https://kiwivm.64clouds.com/')
    driver.find_element_by_name('login').send_keys(serverIP)
    driver.find_element_by_name('password').send_keys(pwd)
    driver.find_element_by_class_name('vecontrolButton').click()
    time.sleep(1.5)
    driver.get('https://kiwivm.64clouds.com/kiwi-main-controls.php')
    content = driver.page_source
    print content
    return content
    time.sleep(6)
    driver.quit()

def analysis_data():
    psaa
if __name__=='__main__':
    serverIP, pwd = '67.216.211.14','katios'
    # driver = initial()
    # login()
    a='<tbody><tr><td style="width:13%;background:#00a000;height:8px;vertical-align:middle"></td><td style="width:87%"></td></tr></tbody></table></span><font color="#a0a0a0">1.4/11 GB</font></td></tr><tr><td>Bandwidth usage:<br /><font color="#a0a0a0">Resets: 2017-10-26</font></td><td><span class="indicator"><table cellspacing="0" cellpadding="0" style="width:100;border:1px solid #00a000"><tbody><tr><td style="width:2%;background:#00a000;height:8px;vertical-align:middle"></td><td style="width:98%"></td></tr></tbody></table></span><font color="#a0a0a0">11.6/550 GB </font>'
    pattern = '>Resets: (\d{4}-\d{2}-\d{2})<.*>(\d*\.?\d*/\d*) GB'
    info = re.search(pattern,a)
    print info.groups()



