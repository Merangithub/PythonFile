import requests, pymongo
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost',27017)
zhoujielun = client['zhoujielun']
tb_word = zhoujielun['tb_word']

#待构造歌词目录页
#一个目录页有48个歌词页面的地址
startUrl = 'https://www.90lrc.cn/geshou/100360.html?id=100360&page='

#目录页地址
contentsPageUrl = []

#所有歌词地址
wordUrls = []

#构造所有目录页
def buildContentsUrl():
	for i in range(5):
		contentsPageUrl.append(startUrl + str(i))
		print('第' + str(i) + '个目录地址是：' + contentsPageUrl[i])
	del contentsPageUrl[0]
	print('目录页构造完毕!')

# 获取目录页中所有歌词地址
def getAllWordUrls(urls):
	for url in urls:
		html = requests.get(url)
		html.encoding = 'utf-8'
		# print(html.text)
		soup = BeautifulSoup(html.text, 'lxml')

		oldWordUrls = soup.select('div.rec > ul > li > a')
		#网页获取的歌词url为：/geci/97730.html
		#而完整的歌词url为：https://www.90lrc.cn/geci/97730.html
		count = 0
		for newWordUrls in oldWordUrls:
			wordUrls.append('https://www.90lrc.cn' + newWordUrls.get('href'))
			print('当前获取的歌词地址为：' + wordUrls[count])
			count += 1


def getWord(urls):
	for url in urls:
		html = requests.get(url)
		html.encoding = 'utf-8'
		# print(html.text)
		soup = BeautifulSoup(html.text, 'lxml')

		#歌词
		word = soup.select('p#txt')[0].get_text()

		#歌名
		songName = soup.select('h1')[0].get_text()[1:-3]

		print(url)

		# print(word)
		print(songName)
		data = {
			'word':word,
			'songName':songName,
			'url':url
		}
		tb_word.insert_one(data)

# 1、构造目录页
buildContentsUrl()

# 2、获取目录页中所有歌词地址
getAllWordUrls(contentsPageUrl)

# 3、解析歌词
getWord(wordUrls);

