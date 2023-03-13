import asyncio
import time
import json
import datetime

from src.parser.artist_data_parser import *
from src.parser.genre_page_data_parser import *


# TODO: Вынести в отдельный модуль
def get_all_regions(data):
    all_regions = []
    for artist_id in data:
        if 'Regions' in data[artist_id]:
            regions = data[artist_id]['Regions'].keys()
            all_regions.extend(regions)
    return list(set(all_regions))


async def main():
    start_time = time.time()
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    tasks = []

    genre_list = ['электроника']

    """for i in range(101):
        if i == 0:
            url = 'https://music.yandex.ru/genre/%D1%82%D0%B0%D0%BD%D1%86%D0%B5%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%BC%D1%83%D0%B7%D1%8B%D0%BA%D0%B0/artists'
            for key, value in get_id_name_genres_of_artist(url).items():
                data[key] = value
        else:
            url = f'https://music.yandex.ru/genre/%D1%82%D0%B0%D0%BD%D1%86%D0%B5%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%BC%D1%83%D0%B7%D1%8B%D0%BA%D0%B0/artists?page={i}'
            for key, value in get_id_name_genres_of_artist(url).items():
                data[key] = value
    print('Информация по страницам собрана \n')"""

    data = get_all_data_for_all_pages_and_genres(genre_list)
    ids = list(set(data.keys()))

    for idd in ids:
        tasks.append(asyncio.create_task(get_artists_data(f'https://music.yandex.ru/artist/{idd}/info')))
        await asyncio.sleep(0.08)
        time.sleep(0.1)
    results = await asyncio.gather(*tasks)

    for idd, result in zip(ids, results):
        result['date'] = date_today
        data[idd].update(result)

    final_data = {}

    for key, value in data.items():
        final_data[key] = value

    all_regions = get_all_regions(final_data)

    # TODO: Доделать наименования файлов в соответствии с собранными жанрами и количеством страниц

    with open(f'../data/{date_today}_{genre_list[0]}_page.json', 'w', encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    end_time = time.time()

    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} сек.')


if __name__ == '__main__':
    asyncio.run(main())
