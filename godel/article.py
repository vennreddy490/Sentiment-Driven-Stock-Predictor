import requests
from lxml import etree


class Article:
    def __init__(
        self,
        ticker: str,
        providerName: str,
        key: str,
        publicationTime: str,
        title: str,
        description: str,
    ):
        """Constructs a new instance of Article and stores the
        article's provider name, key, publication time, title,
        and description.

        Args:
            ticker (str): The ticker this article is related to.
            providerName (str): Name of the publisher or news outlet.
            key (str): Unique identifier to retrieve the full article.
            publicationTime (str): Date and time when the article was published.
            title (str): Title of the article.
            description (str): A brief blurb describing the article.

        Returns:
            None
        """
        self.ticker = ticker
        self.providerName = providerName
        self.key = key
        self.publicationTime = publicationTime
        self.title = title
        self.description = description
        self.xmlArticle = None
        self.articleText = None

    def __repr__(self) -> str:
        """Prints out the Article's ticker, title, key, and provider
        for debugging purposes.

        Args:
            None

        Returns:
            str: Neatly organized string describing the Article.
        """
        return f"Article(ticker={self.ticker}, title={self.title}, key={self.key}, providerName={self.providerName})"

    def pullArticle(self) -> etree._Element | None:
        """Fetches the article's content using its key,
        parses it using etree, from lxml, and returns
        the root object.

        Args:
            None

        Returns:
            etree._Element | None: Returns None if there is an error
            fetching the article, or etree._Element if parsing is
            successful.
        """
        if self.xmlArticle != None:
            return self.xmlArticle

        try:
            response = requests.get(
                f"https://api.godelterminal.com/api/news/content/{self.key}"
            )

            if response.status_code != 200:
                return None

            root = etree.fromstring(response.text)

            self.xmlArticle = root
            self.articleText = " ".join(root.xpath(".//nitf/body//text()")).strip()
            return root
        except:
            return None
