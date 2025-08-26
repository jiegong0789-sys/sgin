from bs4 import BeautifulSoup
import requests


def scrape_latest_news_from_x6d():
    """
    此函数用于从 https://x6d.com/ 爬取最新的内容。
    它会查找所有标记为'new'的列表项，并提取标题、链接和日期。
    """
    base_url = "https://x6d.com"

    # 1. 发送网络请求获取最新的HTML内容
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # 确保请求成功
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"无法获取网页内容: {e}")
        return

    # 2. 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 3. 查找包含最新文章的列表
    # 根据HTML结构，最新内容位于id为'newslist'的div中，且列表项的class为'new'
    news_list = soup.find('div', id='newslist')

    if not news_list:
        print("未找到ID为 'newslist' 的内容区域。")
        return

    latest_articles = news_list.find_all('li', class_='new')

    if not latest_articles:
        print("未找到标记为 'new' 的最新文章。")
        return

    # 4. 遍历提取到的文章列表并打印信息
    print("--- x6d.com 每日最新内容 ---")
    for article in latest_articles:
        # 提取链接和标题
        link_tag = article.find('a')
        if link_tag:
            title = link_tag.get_text(strip=True)
            # 将相对链接转换为绝对链接
            relative_link = link_tag['href']
            full_link = base_url + relative_link

            # 提取日期
            date_tag = article.find('span')
            date = date_tag.get_text(strip=True) if date_tag else "无日期"

            print(f"标题: {title}")
            print(f"链接: {full_link}")
            print(f"日期: {date}")
            print("-" * 20)


if __name__ == "__main__":
    scrape_latest_news_from_x6d()
