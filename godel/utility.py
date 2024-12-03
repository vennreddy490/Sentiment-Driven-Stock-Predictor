from typing import Dict
from .article import Article


def articleSerializer(obj: Article) -> Dict[str, str | None]:
    return {
        "ticker": obj.ticker,
        "providerName": obj.providerName,
        "key": obj.key,
        "publicationTime": obj.publicationTime,
        "title": obj.title,
        "description": obj.description,
        "articleText": obj.articleText,
    }
