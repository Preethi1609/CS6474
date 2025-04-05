import praw
import os
import time
import json
import prawcore

# Initialize PRAW with your credentials
secret = os.environ.get("SECRET") # how to get: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
client_id = os.environ.get("CLIENT_ID")
user_agent = os.environ.get("USER_AGENT")
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent=user_agent
)

# Input and output files
# input_file = "scraped_participating.txt"
# output_file = "participating_info.json"

input_file = "all_subreddits_full.txt"
output_file = "all_subreddits_info.json"

# List to store subreddit data
subreddit_data = []

def fetch_subreddit_info(subreddit_name):
    """Fetch detailed subreddit information and handle errors."""
    try:
        sub = reddit.subreddit(subreddit_name)
        
        data = {
            "name": sub.display_name,
            "title": sub.title,
            "description": sub.public_description,
            "subscribers": sub.subscribers,
            "active_users": sub.active_user_count,
            "subreddit_age": int(time.time()) - int(sub.created_utc),  # Age in seconds
            "nsfw": sub.over18,
            "ad_friendly": sub.advertiser_category is not None,  # Checks if ad category exists
            # "default": sub.is_default,  # ✅ FIXED: Correct default subreddit check
            "num_moderators": len(list(sub.moderator())),
            "comments_per_moderator": sub.comment_score_hide_mins,  # Approximation
            "removed_content_fraction": sub.allow_images,  # Approximation (no direct API)
            "automod": any("automoderator" in mod.name.lower() for mod in sub.moderator()),  # Detects AutoMod
            "moderator_social_capital": sub.wiki_edit_age,  # Proxy for social capital
            "user_social_capital": sub.user_is_moderator,  # Boolean
            "economic_capital": sub.wiki_edit_count,  # Proxy for contribution
            "cultural_capital": sub.allow_videos  # Proxy for cultural openness
        }
        return data
    
    except prawcore.exceptions.Forbidden:
        print(f"❌ Skipping {subreddit_name} (403 Forbidden - Private or Banned)")
        return None
    except prawcore.exceptions.NotFound:
        print(f"❌ Skipping {subreddit_name} (404 Not Found - Might be deleted)")
        return None
    except Exception as e:
        print(f"⚠️ Error fetching {subreddit_name}: {e}")
        return None

# Read subreddit names from file
with open(input_file, "r", encoding="utf-8") as file:
    subreddits = [line.strip() for line in file.readlines()]

# Fetch data for each subreddit
for count, subreddit_name in enumerate(subreddits, start=1):
    info = fetch_subreddit_info(subreddit_name)
    if info:
        subreddit_data.append(info)

    # Print progress
    if count % 10 == 0:
        print(f"✅ Processed {count}/{len(subreddits)} subreddits...")

    # Prevent rate-limiting
    time.sleep(1)  

# Save data to JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(subreddit_data, f, indent=4)

print(f"✅ Done! Saved subreddit data to {output_file}")
