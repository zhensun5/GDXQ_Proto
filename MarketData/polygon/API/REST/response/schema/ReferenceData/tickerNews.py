from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class Publisher:
    name: str
    homepage_url: str
    logo_url: str
    favicon_url: str

@dataclass
class Insight:
    ticker: str
    sentiment: str
    sentiment_reasoning: str

@dataclass
class NewsArticle:
    id: str
    publisher: Publisher
    title: str
    author: str
    published_utc: str
    article_url: str
    tickers: List[str]
    image_url: str
    description: str
    keywords: List[str]
    insights: List[Insight] = field(default_factory=list)

@dataclass
class TickerNewsResponse:
    results: List[NewsArticle] = field(default_factory=list)
    status: str
    request_id: str
    count: int
    next_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional['TickerNewsResponse']:
        if data.get('status') != 'OK':
            print(f"Error: Response status is {data.get('status')}")
            return None

        if 'results' not in data or not data['results']:
            print("Warning: No results found in the response.")
            return None

        return cls(
            results=[
                NewsArticle(
                    id=article.get('id', ''),
                    publisher=Publisher(**article.get('publisher', {})),
                    title=article.get('title', ''),
                    author=article.get('author', ''),
                    published_utc=article.get('published_utc', ''),
                    article_url=article.get('article_url', ''),
                    tickers=article.get('tickers', []),
                    image_url=article.get('image_url', ''),
                    description=article.get('description', ''),
                    keywords=article.get('keywords', []),
                    insights=[
                        Insight(**insight) for insight in article.get('insights', [])
                    ]
                ) for article in data.get('results', [])
            ],
            status=data.get('status', ''),
            request_id=data.get('request_id', ''),
            count=data.get('count', 0),
            next_url=data.get('next_url')
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self.results:
            print("Warning: No news data available to convert to DataFrame.")
            return pd.DataFrame()

        articles_list = [
            {
                "id": article.id,
                "publisher_name": article.publisher.name,
                "title": article.title,
                "author": article.author,
                "published_utc": article.published_utc,
                "article_url": article.article_url,
                "tickers": ', '.join(article.tickers),
                "image_url": article.image_url,
                "description": article.description,
                "keywords": ', '.join(article.keywords),
                "insights": ', '.join([f"{insight.ticker}: {insight.sentiment}" for insight in article.insights])
            }
            for article in self.results
        ]

        df = pd.DataFrame(articles_list)
        df['published_utc'] = pd.to_datetime(df['published_utc'])
        return df

# # Usage example
# response_data = {
#     "results": [
#         {
#             "id": "63cf23b5100b890399aca1af17c52d58f5a6e4ab7b175641e864a919e2876bc5",
#             "publisher": {
#                 "name": "Benzinga",
#                 "homepage_url": "https://www.benzinga.com/",
#                 "logo_url": "https://s3.polygon.io/public/assets/news/logos/benzinga.svg",
#                 "favicon_url": "https://s3.polygon.io/public/assets/news/favicons/benzinga.ico"
#             },
#             "title": "S&P 500 Could Reach 6,300 In 12 Months, Says Goldman Sachs, Driven By 'Strong AI Demand' And 'Margin Expansion'",
#             "author": "Piero Cingari, Benzinga Staff Writer",
#             "published_utc": "2024-10-07T13:34:27Z",
#             "article_url": "https://www.benzinga.com/markets/equities/24/10/41207490/s-p-500-could-reach-6-300-in-12-months-says-goldman-sachs-driven-by-strong-ai-demand-and-margin-",
#             "tickers": ["AAPL", "BMY", "CELGr"],
#             "image_url": "https://cdn.benzinga.com/files/images/story/2024/10/07/Wall-Street-bull_1.png?width=1200&height=800&fit=crop",
#             "description": "Goldman Sachs raised its 12-month S&P 500 target to 6,300, citing stronger corporate earnings and robust AI demand as key drivers. AI and semiconductor recovery are expected to boost margins.",
#             "keywords": ["S&P 500", "Goldman Sachs", "AI", "Margin Expansion"],
#             "insights": [
#                 {
#                     "ticker": "AAPL",
#                     "sentiment": "positive",
#                     "sentiment_reasoning": "Goldman Sachs highlighted the ongoing strength in mega-cap tech firms, including Apple, which have consistently delivered quarterly earnings surprises."
#                 },
#                 {
#                     "ticker": "BMY",
#                     "sentiment": "positive",
#                     "sentiment_reasoning": "Goldman Sachs expects expenses related to high R&D charges in the healthcare sector, including companies like Bristol-Myers Squibb, to moderate in 2025, leading to margin gains."
#                 },
#                 {
#                     "ticker": "CELGr",
#                     "sentiment": "positive",
#                     "sentiment_reasoning": "Goldman Sachs expects expenses related to high R&D charges in the healthcare sector, including companies like Bristol-Myers Squibb, to moderate in 2025, leading to margin gains."
#                 }
#             ]
#         }
#         # ... (other articles)
#     ],
#     "status": "OK",
#     "request_id": "015fe402d1ecc314002e1e9a3504ec85",
#     "count": 10,
#     "next_url": "https://api.polygon.io/v2/reference/news?cursor=YXA9MjAyNC0xMC0wNFQxNiUzQTA1JTNBNTRaJmFzPWU1NGE1YTQyMTFiNjEzZDQ3ZjYyNGRkOTI5ZjNkYzRhNjAyN2ExMzQ5M2UzMmJhNTUxMGZjMjIwOWM0NDFiOTEmb3JkZXI9ZGVzY2VuZGluZyZ0aWNrZXI9QUFQTA"
# }

# parsed_response = TickerNewsResponse.from_dict(response_data)
# if parsed_response:
#     df = parsed_response.to_dataframe()
#     print(df)
# else:
#     print("Failed to parse response.")