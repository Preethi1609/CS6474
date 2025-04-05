import praw
import time
import os

# Initialize PRAW with credentials from environment variables
secret = os.environ.get("SECRET") 
client_id = os.environ.get("CLIENT_ID")
user_agent = os.environ.get("USER_AGENT")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent=user_agent
)

# Output file
output_file = "all_subreddits.txt"

# Open file to write subreddit names
subreddit_count = 0

with open(output_file, "w", encoding="utf-8") as file:
    try:
        for subreddit in reddit.subreddits.new(limit=None):  # Fetch all possible subreddits
            file.write(subreddit.display_name + "\n")
            subreddit_count += 1

            # Print progress every 1000 subreddits
            if subreddit_count % 1000 == 0:
                print(f"Fetched {subreddit_count} subreddits...")
                
            # Optional sleep to avoid rate limits
            time.sleep(0.5)  

    except Exception as e:
        print(f"Error: {e}")

print(f"Done! Saved {subreddit_count} subreddits to {output_file}.")
