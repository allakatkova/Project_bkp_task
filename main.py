from pprint import pprint
import requests

DIR_BACKUP_YD = '/backup_VK_photo/'
TOKENS_FILE = 'tokens.txt'
URL_VK = 'https://api.vk.com/method/'


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        url_files_list = 'https://cloud-api.yandex.net:443/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url_files_list, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path, link):
        url_upload = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "url": link, "disable_redirects": "false"}
        response = requests.post(url_upload, headers=headers, params=params)
        return response

    def upload(self, folder_path, list_files):
        count_file = 0
        for filename, url_file in list_files.items():
            disk_file_path = folder_path + filename
            href_upload = self._get_upload_link(disk_file_path=disk_file_path, link=url_file)
            href_upload.raise_for_status()
            count_file += 1
            if href_upload.status_code == 202:
                pprint(f'Сохранена {count_file} фотография из {len(list_files)} под именем {filename}')
        print('Выполнено! Бэкап фотографий создан успешно.')


class VkDownloader:
    def __init__(self, token: str, userid: str):
        self.token = token
        self.userid = userid

    def get_info_photos_album(self, count_photo=5):
        url = URL_VK + 'photos.get'
        params = {
            'owner_id': self.userid,
            'album_id': 'profile',
            'extended': '1',
            'count': count_photo,
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        return res.json()

    def get_photos_data(self, info_photos_album):
        list_file_for_backup = {}
        list_photo_data = info_photos_album['response']['items']
        for photo in list_photo_data:
            max_size = 0
            url_max_size = ''
            # определить фото в максимальном качестве разрешения
            for size in photo['sizes']:
                if size['height'] >= max_size:
                    max_size = size['height']
                    url_max_size = size['url']
            file_name = str(photo['likes']['count'])
            date_photo = photo['date']
            # если количество лайков одинаково, то добавить дату загрузки.
            if list_file_for_backup.get(file_name) is not None:
                file_name = f"{file_name}_{date_photo}"
            file_name += '.jpg'
            list_file_for_backup[file_name] = url_max_size
        return list_file_for_backup


def get_tokens(tokens_file):
    tokens_from_file = {}
    with open(tokens_file, 'rt', encoding='utf-8') as file:
        tokens_from_file.update({'YD': file.readline()[:-1]})
        tokens_from_file.update({'VK': file.readline()[:-1]})
    return tokens_from_file


if __name__ == '__main__':

    # userid_vk = input('Введите ID пользователя ВКонтакте: ')
    userid_vk = '24669426'

    tokens_list = get_tokens(TOKENS_FILE)
    # token_yd = input('Введите token Я.Диск: ')
    token_yd = tokens_list['YD']

    downloader_from_vk = VkDownloader(tokens_list['VK'], userid_vk)
    info_photos_album = downloader_from_vk.get_info_photos_album()
    names_files_with_urls = downloader_from_vk.get_photos_data(info_photos_album)

    uploader = YaUploader(token_yd)
    uploader.upload(DIR_BACKUP_YD, names_files_with_urls)
