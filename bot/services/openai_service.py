# bot/services/openai_service.py
import openai
from typing import List

openai.api_key = 'YOUR_OPENAI_API_KEY'

async def get_rhymes_from_openai(word: str) -> List[str]:
    prompt = f"Подбери слова, которые рифмуются с '{word}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    rhymes = response.choices[0].text.strip().split(',')
    return [rhyme.strip() for rhyme in rhymes]
