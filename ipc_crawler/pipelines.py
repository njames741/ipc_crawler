# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re

class IpcCrawlerPipeline(object):
	def open_spider(self, spider):
		self.dict = {}

	def close_spider(self, spider):
		filename = 'test4.json'
		with open(filename,'w') as load_f:
			json.dump(self.dict, load_f, ensure_ascii=False)
			
	def process_item(self, item, spider):
[b,e][.+]
		p = re.compile(r'（.*?）|\[.+\]|\(.*?\)|\(.*?）|（.*?\)')	#去除description中()和[]的內容()
		number = item.get('number')
		description = item.get('description').split("→")

		for i in range(len(description)):
			temp = p.sub(' ', description[i]).replace(" ", "")
			description[i] = temp if temp else description[i]

			if "(" in description[i] or "（" in description[i]:	#過濾掉只有前括號的description
				description[i] = re.split("\(|（",description[i])[0]

		description = " → ".join(description)
		
		
		self.dict[number] = description

		return item
