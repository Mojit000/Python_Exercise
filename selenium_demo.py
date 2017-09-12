from selenium import webdriver


browser = webdriver.PhantomJS()
browser.get('http://www.qq.com')
print(browser.title)
