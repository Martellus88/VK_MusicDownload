import os
import sys
import requests

import vk_api
from vk_api import audio


PATH = os.path.normpath('music/')



def auth():
    try:
        vk_session = vk_api.VkApi(login=input('Введите логин: '), password=input('Введите пароль: '))
        vk_session.auth()
        vk_audio = vk_api.audio.VkAudio(vk_session)
    except vk_api.VkApiError as exc:
        print(exc)
    except KeyboardInterrupt:
        print('\nЗавершение работы.')
    else:
        return vk_audio


def downloader(track):
    full_name = f"{track['artist']}-{track['title']}.mp3"
    print(f'\n--- Скачивается: {full_name} ---')
    r = requests.get(track['url'])
    if r.status_code == 200:
        print('Сохранение на диск...')
        with open(full_name, 'wb') as output_file:
            output_file.write(r.content)
        print(f'--- Аудиозапись: {full_name} сохранена. ---')
    else:
        print('Не удалось установить соединение с сайтом. Попробуйте позже.')
        sys.exit()
                
def download_all_tracks(track_list):
    for track in track_list:
        downloader(track)

def download_by_track_name(track_list):
    track_name = input('\nДля выхода из программы введите - <q>\nВведите название аудиозаписи: ').lower()
    for track in track_list:
        if track_name == 'q':
            break
        if track['title'].lower() == track_name or track['title'].lower().startswith(track_name[:3]):
            downloader(track)
            track_name = input('\nДля выхода из программы введите - <q>\nВведите название аудиозаписи: ')



def main():
    try:
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        os.chdir(PATH)

        vk_audio_class = auth()
        track_list = vk_audio_class.get_iter(owner_id = input('Введите id пользователя: '))

        n = input('\nВыберите режим скачивания: 1 - скачать всю библиотеку, 2 - скачать по названию аудиозаписи\n> ')
        if n == '1':
            download_all_tracks(track_list)
        elif n == '2':
            download_by_track_name(track_list)
        else:
            sys.exit()
    except KeyboardInterrupt:
        print('\nЗавершение работы.')
    except (AttributeError, NameError):
        print('\nВы ввели неверные данные.')



if __name__ == '__main__':
    main()
