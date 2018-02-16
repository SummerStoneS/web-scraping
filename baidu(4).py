import random
from selenium import webdriver
import pickle
from PIL import Image
import shutil
import requests
import sys
import numpy as np
import json
from selenium.webdriver.common.action_chains import ActionChains
from contextlib import closing


class DigitsRecognizer:
    def __init__(self):
		patterns = {
			'5111150': 0,
			'1170': 1,
			'2222230': 2,
			'2122250': 3,
			'3222710': 4,
			'5222230': 5,
			'5222220': 6,
			'1112430': 7,
			'5222250': 8,
			'3222260': 9,
		}
		self.tree = self.build(patterns)

	def build(self, patterns):
		"""
		Build a 'decision tree'
		"""
		groups = set(x[0] for x in patterns.keys())
		tree = {}
		for g in groups:
			if g == '0':
				tree[g] = patterns[g]
			else:
				group = {k[1:]: v for k, v in patterns.items() if k[0] == g}
				tree[g] = self.build(group)
		return tree

	def translate(self, series):
		"""
		Find one digit from pattern series
		"""
		tree = None
		for i, ch in enumerate(series):
			if tree is None:
				if ch == '0':
					continue
				tree = self.tree
			tree = tree[ch]
			if isinstance(tree, int):
				yield tree
				tree = None

	def recognize(self, img):
		"""
		Extract the numbers digit by digit from the image
		"""
		width = img.size[0]
		img = np.asarray(img.crop((0, 3, width, 10)).getdata()).reshape(7, width, 3)
		series = np.asarray(((img.mean(-1) / 255) > 0.5).sum(0), dtype=int)
		series = "".join(map(str, series))        # Extract pattern series from the image
		# print(series)
		value = 0
		for digit in self.translate(series):      # Extract digits from the pattern series
			value = value * 10 + digit
		return value


def create_browser(refresh=False):
	options = webdriver.ChromeOptions()            # Headless Chrome
	options.add_argument('headless')                # 运行的时候不要弹窗
	options.add_argument('window-size=1200x600')
	chrome = webdriver.Chrome(chrome_options=options)
	def manually_login():
		new_browser = webdriver.Chrome()
		new_browser.get("https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F")
		input("Please login manually")
		cookies = new_browser.get_cookies()                 # 记录cookies，以后就不用手动登陆了
		with open("cookies.pkl", "wb") as pickle_file:
			pickle.dump(cookies, pickle_file)
		new_browser.close()
		load_cookies()

	def load_cookies():
		with open("cookies.pkl", "rb") as pickle_file:
			cookies = pickle.load(pickle_file)
		chrome.get("http://index.baidu.com")
		for cookie in cookies:
			cookie['domain'] = '.baidu.com'
			chrome.add_cookie(cookie)

	if refresh:
		manually_login()
	else:
		try:
			load_cookies()
		except Exception as e:
			print("Cant automatically login because of {}".format(str(e)))
			manually_login()

	return closing(chrome)



class Catcher:
	def __init__(self, browser):
		self.browser = browser
		self.keys = set()
		self.digits_recognizer = DigitsRecognizer()
		self.sess = self.create_requests_session(browser)

	@staticmethod
	def create_requests_session(browser):
		sess = requests.Session()
		cookies = browser.get_cookies()
		for cookie in cookies:
			sess.cookies.set(cookie['name'], cookie['value'], domain='.baidu.com')
		return sess

	def download_image(self, img_url):
		"""
		Download the image using requests.
		"""
		resp = self.sess.get(img_url, stream=True)		# if False, the response content will be immediately downloaded.
		resp.raw.decode_content = True					# 有的打包下载下来的内容会被压缩，需要对内容解压缩
		with open("img.png", "wb") as fp:
			shutil.copyfileobj(resp.raw, fp)
		try:
			return Image.open("img.png")
		except OSError:
			return self.download_image(img_url)

	def capture(self):
		"""
		Find and recognize value from the page
		"""
		b = self.browser
		wrap = b.find_element_by_css_selector("div.view-table-wrap")
		key = wrap.text[:10]				# 2017-12-28 获取悬浮框上的时间
		if key not in self.keys:
			b.implicitly_wait(0.5)
			img = None
			result = []
			imgvals = b.find_elements_by_xpath('//*[@id="trendPopTab"]/tbody/tr/td[3]/span[@class="imgval"]')
			for imgval in imgvals:
				imgtxt = imgval.find_element_by_tag_name("div")
				if img is None:
					imgurl = imgtxt.value_of_css_property("background-image")[5:-2]
					img = self.download_image(imgurl)
				width = int(imgval.value_of_css_property("width")[:-2])
				offset = -int(imgtxt.value_of_css_property("margin-left")[:-2])
				sub_img = img.crop((offset, 0, offset+width, img.size[1]))
				result.append(sub_img)
			if not result:
				raise ValueError
			result = self.cat(result)
			self.keys.add(key)
			return key, self.digits_recognizer.recognize(result)
		else:
			return None

	@staticmethod
	def cat(result):
		"""
		Concatename images
		"""
		height = max(x.size[1] for x in result)
		width = sum(x.size[0] for x in result)
		new_im = Image.new('RGB', (width, height))
		x = 0
		for img in result:
			new_im.paste(img, (x, 0))
			x += img.size[0]
		return new_im


def shake(browser, control, max_x=None):
	"""
	Move mouse across the canvas to refresh "mousemove" event
	"""
	x = max_x = max_x or control.size['width'] // 2
	action = ActionChains(browser)
	for x in range(1, max_x):
		action = action.move_to_element_with_offset(control, x, 10+random.randrange(20))
	action.perform()
	browser.implicitly_wait(1)
	if not browser.find_elements_by_css_selector("div.viewbox"):
		raise RuntimeError("Can't find viewbox")
	return x


def main():
	with create_browser(refresh=False) as phantom:
		phantom.get("http://index.baidu.com/?tpl=trend&word=suv")
		phantom.implicitly_wait(4)
		# 找到要抓数图片的位置
		index_image = phantom.find_elements_by_css_selector("#trend rect")[2]
		# 模拟鼠标滑动悬浮
		shake(phantom, index_image)

		catcher = Catcher(phantom)
		data = []
		x = 1
		for x in range(1, index_image.size['width'], 4):
			ActionChains(phantom).move_to_element_with_offset(index_image, x, 15).perform()
			phantom.implicitly_wait(0.1)
			while 1:
				try:
					info = catcher.capture()
				except ValueError:
					print("Error")
					x = shake(phantom, index_image, x)
					continue
				if info is not None:
					data.append(info)
					print(*info)
				break
	data = dict(data)
	return data

if __name__ == '__main__':
    main()
