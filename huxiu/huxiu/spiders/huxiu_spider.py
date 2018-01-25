import scrapy
from huxiu.items import HuxiuItem


class HuxiuSpider(scrapy.Spider):
    # Spider的名称
    name = 'huxiu'
    # 爬取的url
    start_urls = ['https://www.huxiu.com/channel/104.html']

    def parse(self, response):
        """
        解析页面的响应数据，因为解析的数据比较多，使用yield关键字，将怎个方法作为生成器，迭代获取解析的数据
        :param response: 响应的数据
        :return:
        """
        # 解析列表，获取当前页面所有的列表数据
        for sele in response.xpath('//div[@class="mob-ctt"]'):
            # 创建item对象
            item = HuxiuItem()
            item['link']=sele.xpath('.//h2/a/@href')[0].extract()
            url='https://www.huxiu.com'+item['link']
            print(url)
            yield scrapy.Request(url,callback=self.pares_article)
            # yield item

    def pares_article(self,response):
        for sele in response.xpath('//div[@class="article-section-wrap"]'):
            item = HuxiuItem()
            # 将文本信息，赋值给item
            item['title'] = sele.xpath(".//h1/text()")[0].extract().strip()# 获取到标题的标签的文本数据
            item['author-name'] =sele.xpath('.//*[@id="article229808"]/div[2]/div[2]/div[1]/span/a/text()')[0].extract() # 获取文本数据author-name
            print(item['author-name'])

            # item['abstract'] = sele.xpath('.//div[@class="mob-sub"]/text()')[0].extract()  # 获取到摘要的文本数据
            # yield item

            # yield scrapy.Request(callback=self.pares)