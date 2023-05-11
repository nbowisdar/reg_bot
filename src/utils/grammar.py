import asyncio
from pprint import pprint

import aiohttp
url = 'https://speller.yandex.net/services/spellservice.json/checkText'


async def correct_text(text) -> str:
    async with aiohttp.ClientSession() as client:
        params = {'text': text, 'options': 6}
        headers = {'Content-Type': 'application/json'}
        async with client.get(url, params=params, headers=headers) as resp:
            data = await resp.json()

    if data:
        corrected_text = text
        for mistake in reversed(data):
            corrected_text = corrected_text[:mistake['pos']] + mistake['s'][0] + corrected_text[
                                                                            mistake['pos'] + mistake['len']:]

        return corrected_text
    else:
        return text


def shrink_word(word: str) -> str:
    if len(word) > 30:
        word = word[:27] + "..."
    return word
