from datetime import datetime, timedelta,timezone
import os
import requests
from dotenv import load_dotenv
from uagents import Agent, Context

load_dotenv()

class FacebookWrapper:
    """
    FacebookWrapper class for managing Facebook page comments moderation.
    """

    def __init__(self, access_token, page_name):
        """
        Initialize the FacebookWrapper instance.

        Args:
            access_token (str): Facebook user access token.
            page_name (str): Name of the Facebook page.
        """
        self.page_name = page_name
        self.access_token = access_token
        self.page_id = None
        self.page_access_token = None

    def get_all_pages(self):
        """
        Retrieve all Facebook pages associated with the user.

        Returns:
            str: Information message indicating the running status.
        """
        url = f"https://graph.facebook.com/me/accounts?access_token={self.access_token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            pages = data.get("data", [])
        except (requests.RequestException, ValueError) as e:
            return f"Error occurred while retrieving pages: {str(e)}"
        
        if self.page_name:
            pages = [page for page in pages if page.get("name") == self.page_name]
            if not pages:
                return f"No page found with name: {self.page_name}"
            page = pages[0]
            self.page_access_token = page.get("access_token")
            self.page_id = page.get("id")
            self.get_latest_post_comments()
            return f"Running for page: {self.page_name}"
        
        else:
            for page in pages:
                self.page_access_token = page.get("access_token")
                self.page_id = page.get("id")
                print(f"Analyzer run for page: {page['name']}")
            
            return "Running on all pages"

    def get_latest_post_comments(self):
        """
        Retrieve and analyze the comments on the latest post of the Facebook page.
        """
        url = f"https://graph.facebook.com/{self.page_id}/posts?access_token={self.page_access_token}"
        post_limit = int(os.environ.get("POST_LIMIT", 0))
        if post_limit > 0:
            url = f"https://graph.facebook.com/{self.page_id}/posts?limit={post_limit}&access_token={self.page_access_token}" 

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data.get("data"):
                return "No new posts to analyze"
            post_ids = [data["data"][i]["id"] for i in range(len(data["data"]))]
            for post_id in post_ids:
                self.get_comments_by_post_id(post_id)
            
        except (requests.RequestException, ValueError) as e:
            return f"Error occurred while retrieving post comments: {str(e)}"

    def get_comments_by_post_id(self, post_id):
        """
        Retrieve and analyze the comments on a specific post.

        Args:
            post_id (str): ID of the post.

        Returns:
            str: Information message indicating the analysis status.
        """
        url = f"https://graph.facebook.com/{post_id}/comments?access_token={self.page_access_token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            comments = data.get("data", [])
            if not comments:
                return "No comments to analyze"
            filter_comments = self._get_filtered_comments(comments=comments)
            if not filter_comments:
                return "No new comments to analyze"
            for comment in filter_comments:
                if self.should_hide_comment(comment.get("message")):
                    print("Hiding comment:", comment)
                    self.hide_comment(comment.get("id"))

        except (requests.RequestException, ValueError) as e:
            return f"Error occurred while retrieving comments for post {post_id}: {str(e)}"
        
        return "Comments analyzed"

    def _get_filtered_comments(self, comments):
        """
        Filter comments based on the specified timestamp.

        Args:
            comments (list): List of comments.

        Returns:
            list: Filtered comments.
        """
        minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=comments_since)
        filtered_comments = []
        for comment in comments:
            created_time = datetime.strptime(comment['created_time'], "%Y-%m-%dT%H:%M:%S%z")
            created_time_aware = created_time.replace(tzinfo=timezone.utc)
            if created_time_aware >= minutes_ago:
                filtered_comments.append(comment)
        
        return filtered_comments

    def should_hide_comment(self, comment_text):
        """
        Check if a comment should be hidden based on its content.

        Args:
            comment_text (str): Text of the comment.

        Returns:
            bool: True if the comment should be hidden, False otherwise.
        """
        offensive_words = os.environ.get("OFFENSIVE_WORD").split(",")
        return any(word in comment_text.lower() for word in offensive_words)

    def hide_comment(self, comment_id):
        """
        Hide a comment using the Facebook Graph API.

        Args:
            comment_id (str): ID of the comment.
        """
        url = f"https://graph.facebook.com/{comment_id}?is_hidden=true&access_token={self.page_access_token}"
        try:
            response = requests.post(url)
            response.raise_for_status()
            print("Comment hidden:", comment_id)
        except (requests.RequestException, ValueError) as e:
            print(f"Error occurred while hiding comment {comment_id}: {str(e)}")


alice = Agent(name="Vivek", seed="Vivek Agent recovery phrase")
access_token = os.environ.get("ACCESS_TOKEN")
page = os.environ.get("PAGE",None)
comments_since = int(os.environ.get("COMMENTS_SINCE_MIN", 1))

@alice.on_interval(period=comments_since*60.0)
async def analyze_post_comments(ctx: Context):
    print("Start......")
    app = FacebookWrapper(access_token=access_token, page_name=page)
    ctx.logger.info(app.get_all_pages())
    print("Ending.....")


if __name__ == "__main__":
    alice.run()
