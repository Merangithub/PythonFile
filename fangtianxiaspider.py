from bs4 import BeautifulSoup
import requests

url = 'https://gy.zu.fang.com/house/i32/'

#构造多页的url地址，放在一个元组中
url_list = ['https://gy.zu.fang.com/house/i3{}'.format(str(i)) for i in range(1, 4, 1)]

def get_page(url):
	#获取网页源码
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	titles = soup.select('p.title > a')
	prices = soup.select('p.mt5.alingC > span')
	types = soup.select('dd > p.font15.mt12.bold') 
	# print(titles)
	for titles, prices, types in zip(titles, prices, types):
		data = {
			#获取标签属性里面的内容
			'titles':titles.get('title'),
			'prices':prices.get_text(),
			'types':types.get_text()
		}
		print(data)

for i in url_list:
	get_page(i)