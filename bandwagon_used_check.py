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
    # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    driver = webdriver.PhantomJS(desired_capabilities=dcap,)
    # options = webdriver.ChromeOptions()
    # options.add_argument('disable-infobars')
    # driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    return driver

def login():
    driver.get('https://kiwivm.64clouds.com/')
    driver.find_element_by_name('login').send_keys(serverIP)
    driver.find_element_by_name('password').send_keys(login_pwd)
    driver.find_element_by_class_name('vecontrolButton').click()
    time.sleep(5)
    # print 1234
    driver.get('https://kiwivm.64clouds.com/kiwi-main-controls.php')
    # print 56
    content = driver.page_source
    # print content
    return content


def analysis_data():
    # print content
    pattern = '>Resets: (\d{4}-\d{2}-\d{2})<.*>(\d*\.?\d*)/(\d*) GB'
    #print type(content)
    info = re.search(pattern,str(content))
    deadline ,used = info.groups()[0], info.groups()[1]
    print '已用 %s GB'% used
    sendmail.send_mail(sender, pwd, recipient, 'BWG used %s GB' % used , '%s到期,已用%sGB'%(deadline, used))
    print 'email send'


if __name__=='__main__':
    print '--', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '--'
    serverIP, login_pwd = 'ip', 'pwd'
    sender, pwd, recipient = 'sender@xxx.com', 'pwd', 'recipient@xxx.com',
    try:
        driver = initial()
        content = login()
        analysis_data()

        driver.quit()
        print 'check success'
    except:
        # time.sleep(100)
        print 'check failed'
        driver.quit()



