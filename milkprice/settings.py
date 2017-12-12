# -*- coding: utf-8 -*-

# Scrapy settings for milkprice project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'milkprice'

SPIDER_MODULES = ['milkprice.spiders']
NEWSPIDER_MODULE = 'milkprice.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'milkprice (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "__jdv=122270672|direct|-|none|-|1508217466206; ipLoc-djd=1-72-2799-0; qrsc=3; mt_xid=V2_52007VwMaUlldUl0bThFsV2EDFwUIXAFGSE8cDhliBxoAQVBTWBpVGFsEYFNFUl9fVA4eeRpdBWEfElNBWFtLH0ESXQJsARRiX2hSah9LEFQFZAERUm1YV1wY; __utmt=1; __jda=122270672.1915416569.1504066326.1508323320.1508331046.11; __jdb=122270672.6.1915416569|11.1508331046; __jdc=122270672; rkv=V0300; xtest=6213.cf6b6759; __utma=122270672.1235159963.1508331360.1508331360.1508331360.1; __utmb=122270672.8.10.1508331360; __utmc=122270672; __utmz=122270672.1508331360.1.1.utmcsr=jd.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __jdu=1915416569; 3AB9D23F7A4B3C9B=YBKXAWL3CHATLPIKHFPS7Q7OZLJMHHW3MBIKIQE352BVRMV63M5NEKI4W4PTWAZQ4DNUZ7DONMB2B4GF3POLT5WEVE",
    "Host": "search.jd.com",
    "Referer": "https://search.jd.com/Search?keyword=%E5%A9%B4%E5%84%BF%E5%A5%B6%E7%B2%89&enc=utf-8&wq=%E5%A9%B4%E5%84%BF%E5%A5%B6%E7%B2%89&pvid=4f65084adcea4f1d8822260a99df1a7f",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'milkprice.middlewares.MilkpriceSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#         'milkprice.rotate_useragent.RotateUserAgentMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'milkprice.pipelines.MilkpriceItemCsvPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
