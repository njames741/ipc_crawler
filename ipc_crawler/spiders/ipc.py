# -*- coding: utf-8 -*-
import scrapy
from ipc_crawler.items import IpcCrawlerItem

class IpcSpider(scrapy.Spider):
	name = 'ipc'	#執行時的名稱
	allowed_domains = ['tipo.gov.tw'] #允許爬取的網域
	start_urls = ['https://www.tipo.gov.tw/sp.asp?xdurl=mp/lpipcFull.asp&version=201901&ctNode=7231&mp=1']
	#起始的網址



	def parse(self, response):
		for i in response.xpath('//*[@id="ipcTable"]/tr'):

			yield scrapy.Request('https://www.tipo.gov.tw/' + i.xpath('th/a[1]/@href').extract()[0], self.parse_level2)
			# break

	def parse_level2(self, response):
		# ipcItem = response.meta['item']
		table = response.xpath('//*[@id="ipcTable"]/tr')
		for i in range(1,len(table)):
			number = table[i].xpath('th/a[1]/text()').extract()
			description = table[i].xpath('td/text()').extract()


		# for i in response.xpath('//*[@id="ipcTable"]/tr'):
		# 	number = i.xpath('th/a[1]/text()').extract()
		# 	description = i.xpath('td/text()').extract()
		# 	if not number:	#過濾掉第一個，因為第一個是上層number
		# 		continue
			# print(number[0])
			# print(description[0])
			yield scrapy.Request('https://www.tipo.gov.tw/' + table[i].xpath('th/a[1]/@href').extract()[0], self.parse_level3)
			# break

	def parse_level3(self, response):
		table = response.xpath('//*[@id="ipcTable"]/tr')
		for i in range(2,len(table)):
			number = table[i].xpath('th/a[1]/text()').extract()
			description = table[i].xpath('td/text()').extract()

			# print(number[0])
			# print(description[0])
			yield scrapy.Request('https://www.tipo.gov.tw/' + table[i].xpath('th/a[1]/@href').extract()[0], self.parse_level4)
			# break

	def parse_level4(self, response):
		ipcItem = IpcCrawlerItem()
		count = 0
		table = response.xpath('//*[@id="ipcTable"]/tr')

		level3_description = table[2].xpath('td/text()').extract()[0]
		level4_description = ""
		for i in range(3,len(table)):
			number = table[i].xpath('th/a[1]/text()').extract()[0]
			if not table[i].xpath('td/text()').extract():  #有兩個(A61L 12/00和A61K 125/00)沒有description
				continue
			description = table[i].xpath('td/text()').extract()[0]

			if table[i].css('tr.em').extract():
				level4_description = description
				ipcItem['number'] = number
				ipcItem['description'] = level3_description + "→" +description
			else:
				ipcItem['number'] = number
				ipcItem['description'] = level3_description + "→" + level4_description + "→" + description
				
			yield ipcItem

			# count += 1
			# if count == 100:
			# 	break