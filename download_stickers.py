import asyncio
import os
from typing import List

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

CATEGORIES = (
    'animals',
    'entertainment',
    'education',
    'food',
    'games-apps',
)
MAX_PAGES = 10
BASE_DOWNLOAD_DIR = '/home/fns/workspace/telegram-stickers/stickers'


class StickerDownloader:
    BASE_URL = 'https://telegramchannels.me/stickers'

    def __init__(self, categories: List[str], max_pages: int, base_download_dir: str):
        self._categories = categories
        self._max_pages = max_pages
        self._base_download_dir = base_download_dir
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def download_stickers(self):
        futures = (
            self._download_stickers_from_category(category=category)
            for category in self._categories
        )

        await asyncio.gather(*futures)

    async def _download_stickers_from_category(self, category: str):
        path = os.path.join(self._base_download_dir, category)
        if not os.path.exists(path):
            os.mkdir(path)

        futures = (
            self._download_stickers_from_page(category=category, page=page)
            for page in range(1, self._max_pages + 1)
        )

        await asyncio.gather(*futures)

    async def _download_stickers_from_page(self, category: str, page: int):
        params = {
            'category': category,
            'sort': 'rating',
            'page': page,
        }
        response = await self._session.get(self.BASE_URL, params=params)
        html = await response.text()

        soup = BeautifulSoup(html, features='html.parser')
        urls = (
            sticker_pack.find(class_='is-clickable is-block has-text-grey-darker')['href']
            for sticker_pack in soup.find_all(class_='card media-card')
        )

        futures = (
            self._download_sticker_pack(category=category, url=url)
            for url in urls
        )
        await asyncio.gather(*futures)

    async def _download_sticker_pack(self, category: str, url: str):
        response = await self._session.get(url)
        html = await response.text()

        soup = BeautifulSoup(html, features='html.parser')
        title = soup.title.string
        pack_name = title.split('-')[0].strip()

        path = os.path.join(self._base_download_dir, category, pack_name)

        if not os.path.exists(path):
            os.mkdir(path)

        thumbnails = soup.find_all(class_='light-link')
        futures = (
            self._download_thumbnail(
                url=thumbnail.img['data-src'],
                download_path=os.path.join(path, f'{pack_name}_{i}.png')
            )
            for i, thumbnail in enumerate(thumbnails)
        )
        await asyncio.gather(*futures)

    async def _download_thumbnail(self, url: str, download_path: str):
        file = await aiofiles.open(download_path, mode='wb')
        response = await self._session.get(url)
        await file.write(await response.read())
        await file.close()


async def main():
    async with StickerDownloader(categories=['food'], max_pages=1, base_download_dir=BASE_DOWNLOAD_DIR) as downloader:
        await downloader.download_stickers()


if __name__ == '__main__':
    asyncio.run(main())
