import requests
from bs4 import BeautifulSoup

def get_main_page_articles(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve the main webpage. Status code: {response.status_code}")
        return None

def find_article_links(soup):
    articles = soup.find_all('article', class_='card-top')
    article_links = []
    for article in articles:
        link = article.find('a', class_='card-link')['href']
        article_links.append(link)
    print("Extracted Article Links:", article_links)  # Debugging: print the extracted links
    return article_links

def get_article_details(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        article_soup = BeautifulSoup(response.content, 'html.parser')
        
        # Print the HTML content to identify correct tags
        # print(f"HTML content of {article_url}:\n", article_soup.prettify())  # Uncomment for debugging

        article_title = article_soup.find('h1', id='article-title')
        if article_title:
            article_title = article_title.text.strip()
        else:
            print("Article title not found.")
            return None
        
        article_price = article_soup.find('p', id='article-price')
        if article_price:
            article_price = article_price.text.strip()
        else:
            print("Article price not found.")
            return None

        article_description = article_soup.find('div', id='article-detail')
        if article_description:
            article_description = article_description.text.strip()
        else:
            print("Article description not found.")
            return None

        images = []
        for img in article_soup.select('#image-slider .image-wrap img'):
            images.append(img['data-lazy'])
        
        nickname = article_soup.find('div', id='nickname')
        if nickname:
            nickname = nickname.text.strip()
        else:
            print("Nickname not found.")
            return None

        region = article_soup.find('div', id='region-name')
        if region:
            region = region.text.strip()
        else:
            print("Region not found.")
            return None

        temperature = article_soup.select_one('#temperature-wrap')
        if temperature:
            temperature = temperature.text.strip()
        else:
            print("Temperature not found.")
            return None

        counts_element = article_soup.select_one('#article-counts')
        if counts_element:
            counts_text = counts_element.get_text()
            counts_list = counts_text.split('∙')
            interest_count = counts_list[0].strip().split()[1]  # Extracting the interest count
            view_count = counts_list[2].strip().split()[1]
        else : 
            print("counts_element not found.")
            return None
        return {
            'title': article_title,
            'price': article_price,
            'description': article_description,
            'images': images,
            'nickname': nickname,
            'region': region,
            'temperature': temperature,
            'interest_count' : interest_count,
            'view_count' : view_count
        }
    else:
        print(f"Failed to retrieve the article page. Status code: {response.status_code}")
        return None

def main():
    main_url = "https://www.daangn.com/fleamarket/"
    
    # Get the main page soup
    main_page_soup = get_main_page_articles(main_url)

    if main_page_soup:
        # Find all article links
        article_links = find_article_links(main_page_soup)

        for link in article_links:
            # Construct the full URL of the article
            article_url = f"https://www.daangn.com{link}"

            # Get article details
            article_details = get_article_details(article_url)

            if article_details:
                # Print the extracted details
                print(f"Article Title: {article_details['title']}")
                print(f"Price: {article_details['price']}")
                print(f"Description: {article_details['description']}")
                print(f"Images: {article_details['images']}")
                print(f"Nickname: {article_details['nickname']}")
                print(f"Region: {article_details['region']}")
                print(f"Temperature: {article_details['temperature']}")
                print(f"interest_count: {article_details['interest_count']}")
                print(f"view_count: {article_details['view_count']}")
                print("-" * 40)

if __name__ == "__main__":
    main()
