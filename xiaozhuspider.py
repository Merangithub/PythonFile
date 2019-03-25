import requests, pymongo, time
from bs4 import BeautifulSoup

client=pymongo.MongoClient('localhost',27017)#连接MongoDB数据库
xiaozhu = client['xiaozhu']
tab_xiaozhu_gy = xiaozhu['tab_xiaozhu_gy']

url = 'http://gy.xiaozhu.com/search-duanzufang-p5-0/'
urls = 'http://gy.xiaozhu.com/search-duanzufang-p'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

def get_house_info(url):
	time.sleep(3)
	html = requests.get(url,headers = headers)
	soup = BeautifulSoup(html.text, 'lxml')

	#标题
	titles = soup.select('span.result_title.hiddenTxt')
	#价格
	prices = soup.select('span.result_price > i')
	#详细页面
	detailurls = soup.select('div.result_btm_con.lodgeunitname')
	#评分和评分数
	scores = soup.select('span.commenthref')
	#基本描述
	describes = soup.select('em.hiddenTxt')

	# 由于detailurl是标签里面属性的值，这样才能获取
	# print(detailurls[0].get('detailurl'))

	for title, price, detailurl, score, describe in zip(titles, prices, detailurls, scores, describes):
		data={
			'title':title.get_text(),
			'price':price.get_text(),
			'detailurl':detailurl.get('detailurl'),
			#split是切割字符创，切割后变成两个字符串，strip是去掉左右两边空格
			'score':score.get_text().split('-')[1].strip(),#留下切割后后面那段
			'describe':describe.get_text().split('-')[0].strip()#留下切割后前面那段
		}
		# print(data)
		# 写入数据库
		tab_xiaozhu_gy.insert_one(data)

def get_many_pages_info(startPage, endPage):
	for i in range(startPage, endPage):
		newUrl = urls + str(i) + '-0/'
		get_house_info(newUrl)

get_many_pages_info(1, 10)


