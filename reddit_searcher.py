import os
import datetime
from typing import List
import praw

class RedditSearcher:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_API_KEY'),
            user_agent='my user agent'
        )

    def search_subreddits(self, search_strings: List[str], subreddits: List[str]=['all']):
        data = []
        for subreddit in subreddits:
            for search_string in search_strings:
                posts_found_in_subreddit = 0
                for submission in self.reddit.subreddit(subreddit).search(f"{search_string}", limit=15):
                    data.append({
                        'id': submission.id,
                        'title': submission.title,
                        'url': submission.url,
                        'selftext': submission.selftext,
                        'score': submission.score,
                        'created_utc': datetime.datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                        'author': submission.author.name,
                        'subreddit': submission.subreddit.display_name
                    })
                    posts_found_in_subreddit += 1
                print(f"Searching for {search_string} in {subreddit}, found {posts_found_in_subreddit} posts")

        print(f"Total posts found: {len(data)}")
        # Deduplicate according to id, keep the rest of the data
        data = list({d['id']: d for d in data}.values())
        print(f"Deduplicated to {len(data)} posts")

        return data
