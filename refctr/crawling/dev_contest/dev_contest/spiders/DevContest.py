from ..requirements import *

sys.path.append(os.getcwd())

class DevcontestSpider(scrapy.Spider):
    name = "DevContest"
    
    start_urls = [
        "https://www.wevity.com/index.php?c=find&s=1&gub=1&cidx=21"
    ]
    
    def parse(self, response):
        elements = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div[3]/div/ul/li')
        for elem in elements:
            dday_ing = elem.xpath('div[3]/span//text()').get()
            if dday_ing and dday_ing.strip() != '마감':
                elem_url = elem.xpath('div[1]/a/@href').get()
                if elem_url:
                    full_url = response.urljoin(elem_url)
                    yield scrapy.Request(url=full_url, callback=self.parse_detail, meta={'contest_url': full_url, 'status': dday_ing.strip()})

    def parse_detail(self, response):
        url = response.meta['contest_url']
        title = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6//text()').get()
        img_url = "https://www.wevity.com/" + response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img/@src').get()
        
        tit_dic = {}
        tit_dic['title'] = title
        tit_dic['url'] = url
        tit_dic['img_url'] = img_url
        tit_dic['status'] = response.meta['status']

        # 분야
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[1]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        if len(output_list) > 1:
            tit_dic['category'] = output_list[1]

        # 응모대상
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[2]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        if len(output_list) > 1:
            tit_dic['target'] = output_list[1]

        # 주최/주관
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[3]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        if len(output_list) > 1:
            tit_dic['host'] = output_list[1]

        # 후원/협찬
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[4]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        print()
        if len(output_list) > 1:
            if output_list[0]:
                tit_dic['sponsor'] = output_list[1]
        else:
            tit_dic['sponsor'] = " "

        # 접수 기간
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[5]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        if len(output_list) > 2:
            tit_dic['period'] = output_list[1]
            tit_dic['d-day'] = output_list[2]

        # 총 상금
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[6]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        if len(output_list) > 1:
            tit_dic['total_prize'] = output_list[1]
        else:
            tit_dic['total_prize'] = " "

        # 1등 상금
        tit = response.xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[7]//text()').getall()
        output_list = [item.strip() for item in tit if item.strip()]
        if len(output_list) > 1:
            tit_dic['first_prize'] = output_list[1]
        else:
            tit_dic['first_prize'] = " "

        yield tit_dic
