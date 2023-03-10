import asyncio
import time
import json
import datetime

from src.parser.artist_data_parser import get_artists_data
from src.parser.genre_page_data_parser import get_id_name_genres_of_artist


def get_all_regions(data):
    all_regions = []
    for artist_id in data:
        if 'Regions' in data[artist_id]:
            regions = data[artist_id]['Regions'].keys()
            all_regions.extend(regions)
    return list(set(all_regions))


async def main():
    start_time = time.time()
    data = {}
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    tasks = []

    counter = 0
    for i in range(1):
        if i == 0:
            url = 'https://music.yandex.ru/genre/%D1%80%D1%8D%D0%BF%20%D0%B8%20%D1%85%D0%B8%D0%BF-%D1%85%D0%BE%D0%BF/artists'
            for key, value in get_id_name_genres_of_artist(url).items():
                data[key] = value
        else:
            url = f'https://music.yandex.ru/genre/%D1%80%D1%8D%D0%BF%20%D0%B8%20%D1%85%D0%B8%D0%BF-%D1%85%D0%BE%D0%BF/artists?page={i}'
            for key, value in get_id_name_genres_of_artist(url).items():
                data[key] = value
        counter = counter + 1
    print('Информация по страницам собрана \n')

    ids = list(data.keys())

    for idd in ids:
        tasks.append(asyncio.create_task(get_artists_data(f'https://music.yandex.ru/artist/{idd}/info')))
        await asyncio.sleep(0.1)
        time.sleep(0.1)
    results = await asyncio.gather(*tasks)

    for idd, result in zip(ids, results):
        result['date'] = date_today
        data[idd].update(result)

    final_data = {}

    for key, value in data.items():
        final_data[key] = value

    """"with open('../data/test.json', 'r') as f:
        existing_data = json.load(f)

    for key, value in data.items():
        existing_data[key] = value"""

    all_regions = get_all_regions(final_data)

    with open('../data/regions.json', 'w', encoding="utf-8") as f:
        json.dump(all_regions, f, ensure_ascii=False, indent=4)

    with open(f'../data/{date_today}_rap_{counter}_page.json', 'w', encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    end_time = time.time()

    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} сек.')


if __name__ == '__main__':
    asyncio.run(main())
