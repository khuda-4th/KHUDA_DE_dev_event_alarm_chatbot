from ..requirements import *

sys.path.append(os.getcwd())

class DevtrendSpider(scrapy.Spider):
    name = "DevTrend"
    
    start_urls = [
        "https://velog.io/trending/day"
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def parse(self, response):
        self.driver.get(response.url)

        # 페이지가 로드될 때까지 기다립니다.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="html"]/body/div/div[2]/div[2]/div/div[2]/main/ul/li'))
        )

        selenium_response = Selector(text=self.driver.page_source)

        trends = selenium_response.xpath('//*[@id="html"]/body/div/div[2]/div[2]/div/div[2]/main/ul/li')
        print(f"Number of trends found: {len(trends)}")

        futures = []
        for trend in trends:
            future = self.executor.submit(self.parse_trend, trend)
            futures.append(future)

        for future in as_completed(futures):
            result = future.result()
            if result:
                yield result

    def parse_trend(self, trend):
        title = trend.xpath('div[1]/a/h4//text()').get()
        user = trend.xpath('div[2]/a/span/b/text()').get()
        img = trend.xpath('a/div/img/@src').get()
        url = trend.xpath('div[1]/a//@href').get()
        user_url = trend.xpath('div[2]/a/@href').get()
        user_img = trend.xpath('div[2]/a/img/@src').get()
        print(f"title: {title}")
        print(f"user: {user}")
        print(f"img: {img}")
        print(f"url: {url}")
        print(f"user_url: {user_url}")
        print(f"user_img: {user_img}")

        if not title or not url or not img or user_img:
            return None

        doc = {
            'title': title,
            'user': user if user else "unknown",
            'img': img,
            'url': url,
            'user_url': "https://velog.io/" + user_url if user_url else "unknown",
            'user_img': user_img if user_img else "https://velog.io/imgaes/user-thumbnail.png"
        }

        return doc
            
    def closed(self, reason):
        self.executor.shutdown(wait=True)
        self.driver.quit()

