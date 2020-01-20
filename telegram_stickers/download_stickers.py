from load_env import load_env
load_env()

import asyncio
import re
from typing import List

import aiohttp
import django
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile


CATEGORIES = [
    'animals',
    'entertainment',
    'education',
    'food',
    'games-apps',
]
MAX_PAGES = 10


class StickerDownloader:
    BASE_URL = 'https://telegramchannels.me/stickers'

    def __init__(self, categories: List[str], max_pages: int):
        self._categories = categories
        self._max_pages = max_pages
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
        futures = (
            self._download_stickers_from_page(category=category, page=page)
            for page in range(1, self._max_pages + 1)
        )

        # TODO we are getting timeouts if running async
        # await asyncio.gather(*futures)
        for future in futures:
            await future

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

        # TODO we are getting timeouts if running async
        # await asyncio.gather(*futures)
        for future in futures:
            await future

    # TODO this method is complex and confusing
    async def _download_sticker_pack(self, category: str, url: str):
        from core.models import Sticker, StickerPack

        response = await self._session.get(url)
        html = await response.text()

        soup = BeautifulSoup(html, features='html.parser')
        title = soup.title.string
        pack_name = title.split('-')[0].strip()

        pattern = re.compile(r't.me/addstickers/.+')
        tme_url = pattern.findall(html)[0]

        thumbnails = soup.find_all(class_='light-link')

        response = await self._session.get(thumbnails[0].img['data-src'])
        buffer = await response.read()
        name = f'{pack_name}_0.png'
        sticker_pack = StickerPack.objects.create(
            name=pack_name,
            category=category,
            thumbnail=ContentFile(buffer, name=name),
            tme_url=tme_url,
        )
        Sticker.objects.create(
            preview=ContentFile(buffer, name=name),
            sticker_pack=sticker_pack,
        )

        for i, thumbnail in enumerate(thumbnails[1:]):
            name = f'{pack_name}_{i}.png'

            response = await self._session.get(thumbnails[i].img['data-src'])
            buffer = await response.read()

            Sticker.objects.create(
                preview=ContentFile(buffer, name=name),
                sticker_pack=sticker_pack,
            )


async def main():
    django.setup()

    async with StickerDownloader(categories=['animals'], max_pages=5) as downloader:
        await downloader.download_stickers()


if __name__ == '__main__':
    asyncio.run(main())
