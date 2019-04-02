import requests
from bs4 import BeautifulSoup


def get_response(url):
    response = requests.get(url)
    return response


def get_data(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        #print(response.json())
        html = response.json()['content_html']
        get_more_videos(response)
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='yt-lockup-content')
    for item in items:
        link = item.find('a').get('href')
        name = item.find('a').get('title')
        print(name, link)


def get_more_videos(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['load_more_widget_html']

    soup = BeautifulSoup(html, 'lxml')
    try:
        url = 'https://www.youtube.com' + soup.find('button', class_='yt-uix-button yt-uix-button-size-default '
                                                                     'yt-uix-button-default load-more-button '
                                                                     'yt-uix-load-more browse-items-load-more-button')\
            .get('data-uix-load-more-href')
    except:
        url = ''
    return url


def main():
    url = 'https://www.youtube.com/user/Azghalore/videos'
    # url = 'https://www.youtube.com/browse_ajax?ctoken=4qmFsgI0EhhVQ2dvR3VBUlRMVk5yUUhkS25nMU8xancaGEVnWjJhV1JsYjNNZ0FEZ' \
    #       '0JlZ0V5dUFFQQ%3D%3D&continuation=4qmFsgI0EhhVQ2dvR3VBUlRMVk5yUUhkS25nMU8xancaGEVnWjJhV1JsYjNNZ0FEZ0JlZ0V5dUF' \
    #       'FQQ%3D%3D&itct=CD8QybcCIhMI3a2T6JOd4QIV8bObCh0F9AhuKJsc'
    #url = 'https://www.youtube.com/browse_ajax?action_continuation=1&amp;continuation=4qmFsgI0EhhVQ2dvR3VBUlRMVk5yUUhkS25nMU8xancaGEVnWjJhV1JsYjNNZ0FEZ0JlZ0V6dUFFQQ%253D%253D'
    while True:
        r = get_response(url)
        get_data(r)
        url = get_more_videos(r)

        if url:
            continue
        else:
            break


if __name__ == "__main__":
    main()
