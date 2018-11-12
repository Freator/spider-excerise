# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

def download_page(url):
	headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"}
	# 查看UserAgent：在Chrome地址栏输入：about:version,或者通过各浏览器自带的UserAgent修改功能查看当前浏览器UserAgent设置情况
	r = requests.get(url, headers=headers) #增加headers，模拟浏览器(<1>)
	return r.text
	
def get_content(html,page):
	output = """第{}页 作者:{} 性别:{} 年龄:{} 点赞:{} 评论:{}\n{}\n---------\n""" #最终输出格式<2>
	soup = BeautifulSoup(html,'html.parser')
	con = soup.find(id = 'content-left') #annotation<3>
	con_list = con.find_all('div',class_='article')
	for i in con_list:
		author = i.find('h2').string #get the name of author
		content = i.find('div',class_='content').find('span').get_text() #get the content
		stats = i.find('div',class_ = 'stats')
		vote = stats.find('span',class_ = 'stats-vote').find('i',class_ = 'number').string
		comment = stats.find('span',class_ = 'stats-comments').find('i',class_ = 'number').string
		author_info = i.find('div',class_ = 'articleGender') #get the age and gender of author
		if author_info is not None: #some author are anonymouse
			class_list = author_info['class']
			if "womenIcon" in class_list:
				gender = '女'
			elif "manIcon" in class_list:
				gender = '男'
			else:
				gender = 'Whatever'
			age = author_info.string  #get the age
		else:
			gender = '?'
			age = '?'
		save_txt(output.format(page, author, gender, age, vote, comment, content))

def save_txt(*args):
	for i in args:
		with open('qiushibaike.txt','a',encoding = 'utf-8') as f:
			f.write(i)

def main():
	# when we click the https chain,we can see there are many pages,so we construct this url,
	# also,we better use BeautifulSoup to find how many pages exactly in the bottom of the page
	for i in range(1,14):
		url = 'https://qiushibaike.com/text/page/{}'.format(i)
		html = download_page(url)
		get_content(html,i)
		
if __name__ == '__main__':
	main()
	
	
	
'''
<1>参考链接https://blog.csdn.net/wzyaiwl/article/details/81056177
有的时候，我们无法爬取一些网页，会出现403错误，因为这些网页为了防止别人恶意采集其
信息所以进行了一些反爬虫的设置。那么如果我们向爬取这些网页的信息，应该怎么办呢？ 
可以设置一些Headers信息，模拟成浏览器去访问这些网站，此时，就能够解决这个问题了
<2>format输出的一种格式，也可以将三个双引号换成三个单引号
<3>找到内容列表，看到这个 div 下面就是当前页面的内容列表
<4>find与find_all的区别？如果使用find函数，只能找到第一个a标签，下面的a都无法找到，
但是如果用find_all函数，又会把a的child全提取
'''