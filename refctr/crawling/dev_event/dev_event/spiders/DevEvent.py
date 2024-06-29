from ..requirements import *

sys.path.append(os.getcwd())

class DevcontestSpider(scrapy.Spider):
    name = "DevEvent"
    
    start_urls = [
        "https://dev-event.vercel.app/events"
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def extract_first_url(self, element):
        parts = element.split(',')
        first_part = parts[0].rstrip(" 640w").lstrip()
        return first_part

    def parse(self, response):
        self.driver.get(response.url)

        # 페이지가 로드될 때까지 기다립니다.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section[1]/section/div/div/div[2]/div'))
        )
        selenium_response = Selector(text=self.driver.page_source)

        contests = selenium_response.xpath('//*[@id="__next"]/main/section[1]/section/div/div/div[2]/div')
        print(f"Number of trends found: {len(contests)}")

        futures = []
        for contest in contests:
            future = self.executor.submit(self.parse_contest, contest)
            futures.append(future)

        for future in as_completed(futures):
            result = future.result()
            if result:
                yield result

    def parse_contest(self, contest):
        img_src = contest.xpath('div/a/div/div[1]/span/img/@srcset').get()
        if img_src:
            url = contest.xpath('div/a/@href').get()
            img_url = "https://dev-event.vercel.app" + self.extract_first_url(img_src)
            title = contest.xpath('div/a/div/div[2]/div[1]/div[2]/div[1]//text()').get()
            host = contest.xpath('div/a/div/div[2]/div[1]/div[1]/div/span//text()').get()
            period = contest.xpath('div/a/div/div[2]/div[2]/span/div/span[2]//text()').get()
            tags = contest.xpath('div/a/div/div[2]/div[2]/div//text()').getall()
                
            tit_dic = {}
            tit_dic['title'] = title
            tit_dic['url'] = url
            tit_dic['img_url'] = img_url
            tit_dic['host'] = host
            tit_dic['period'] = period
            tit_dic['tags'] = ", ".join(tags)

            return tit_dic
        return None

    def closed(self, reason):
        self.executor.shutdown(wait=True)
        self.driver.quit()
