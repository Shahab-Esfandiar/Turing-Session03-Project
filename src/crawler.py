import requests
import random
from typing import List, Dict, Any
from src.exceptions import CrawlerError

class DigikalaCrawler:
    """
    Crawler designed to interact with Digikala's public API to fetch 
    product comments and perform random sampling for unbiased analysis.
    """
    def __init__(self):
        # Base URL for Digikala's product comments API
        self.base_url = "https://api.digikala.com/v1/product/{}/comments/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_comments(self, product_id: int) -> List[str]:
        """
        Fetches up to 200 comments for a given product ID, then applies the sampling logic.
        """
        all_comments = []
        page = 1
        
        try:
            while len(all_comments) < 200:
                url = self.base_url.format(product_id) + f"?page={page}"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    break
                    
                data = response.json()
                comments_data = data.get("data", {}).get("comments", [])
                
                # If no more comments are available on this page
                if not comments_data:
                    break
                    
                for comment in comments_data:
                    body = comment.get("body")
                    if body and len(body.strip()) > 5: # Ignore very short/empty comments
                        all_comments.append(body.strip())
                        
                    if len(all_comments) == 200:
                        break
                        
                page += 1

            return self._sample_comments(all_comments)

        except Exception as e:
            raise CrawlerError(f"Failed to crawl Digikala API: {str(e)}") from e

    def _sample_comments(self, comments: List[str]) -> List[str]:
        """
        Applies the specific sampling business logic:
        - If >= 200 comments: Randomly select 100.
        - If < 200 comments: Randomly select all.
        """
        total_fetched = len(comments)
        if total_fetched == 0:
            return []
            
        if total_fetched >= 200:
            sample_size = 100
        else:
            sample_size = total_fetched
            # Ensure at least 1 comment is selected if there are any
            sample_size = max(1, sample_size)
            
        sampled = random.sample(comments, sample_size)
        print(f"📊 Crawler Stats: Fetched {total_fetched} valid comments. Randomly sampled {sample_size} for analysis.")
        return sampled