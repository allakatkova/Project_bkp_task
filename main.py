from pprint import pprint

DIR_BACKUP_YD = '/backup_VK_photo/'
TOKENS_FILE = 'tokens.txt'


def get_tokens(tokens_file):
    tokens_from_file = {}
    with open(tokens_file, 'rt', encoding='utf-8') as file:
        tokens_from_file.update({'YD': file.readline()[:-1]})
        tokens_from_file.update({'VK': file.readline()[:-1]})
    return tokens_from_file


if __name__ == '__main__':

    tokens_list = get_tokens(TOKENS_FILE)
    pprint(tokens_list)
