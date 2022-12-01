from pprint import pprint
import requests

DIR_BACKUP_YD = '/backup_VK_photo/'
TOKENS_FILE = 'tokens.txt'
URL_VK = 'https://api.vk.com/method/'


def get_tokens(tokens_file):
    tokens_from_file = {}
    with open(tokens_file, 'rt', encoding='utf-8') as file:
        tokens_from_file.update({'YD': file.readline()[:-1]})
        tokens_from_file.update({'VK': file.readline()[:-1]})
    return tokens_from_file


def get_userid_vk():
    # раскомментировать в готовой программе      !!!!!!!!!!!!!!!!!!!!!
    # user_id = input('Введите идентификатор (ID) пользователя: ')
    user_id = '24669426'
    return user_id


def get_list_photos_album(userid, token, count_photo=5):
    url = URL_VK + 'photos.get'
    params = {
        'owner_id': userid,
        'album_id': 'profile',
        'extended': '1',
        'count': count_photo,
        'access_token': token,
        'v': '5.131'
    }
    res = requests.get(url, params=params)
    return res.json()


if __name__ == '__main__':
    userid_vk = get_userid_vk()
    tokens_list = get_tokens(TOKENS_FILE)
    info = get_list_photos_album(userid_vk, tokens_list['VK'])
    pprint(info)
