import os
import sys
import requests
from bs4 import BeautifulSoup


def get_page(url):
    if 'arhivach' not in url:
        sys.exit()
    # Смена протокола на HTTP
    if url.startswith('http://'):
        pass
    elif url.startswith('https://'):
        url = url.replace('https://', 'http://')
    else:
        url = 'http://' + url
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print('Получен код состояния: ' + str(page.status_code))
    return page.text


def parse_thread(html, media_type):
    soup = BeautifulSoup(html, 'lxml')
    parsed_elements = soup.find_all('a', {'class': 'img_filename'})
    links = []
    filtered_links = []
    for elem in parsed_elements:
        links.append(elem['href'])
    for i in links:
        if not i.endswith(('.webm', '.mp4')):
            filtered_links.append(i)
    if media_type == 'images':
        return filtered_links
    if media_type == 'all':
        return links
    sys.exit()


def download_media(url_list):
    if not os.path.exists('media'):
        os.mkdir('media')
    for i in url_list:
        filename = i.split('/')[-1]
        data = requests.get(i).content
        with open('./media/' + filename, 'wb') as file:
            file.write(data)
        print(f'Загружено {url_list.index(i) + 1} из {len(url_list)}')


def main():
    thread_url = input('Ссылка на тред\n> ')
    only_img = input('\nСкачать только изображения? (y, n)\n> ')
    thread_html = get_page(thread_url)
    if only_img == 'y':
        media_links = parse_thread(thread_html, 'images')
    elif only_img == 'n':
        media_links = parse_thread(thread_html, 'all')
    else:
        sys.exit()
    links_number = len(media_links)
    print('Количество медиафайлов: ' + str(links_number), end='\n\n')
    if links_number != 0:
        download_media(media_links)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nСкрипт прерван пользователем')
    except requests.ConnectionError:
        print('\nОшибка подключения к серверу')
