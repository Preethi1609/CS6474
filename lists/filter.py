# Input files
all_subreddits_file = "all_subreddits_full.txt"
participating_file = "scraped_participating.txt"
non_participating_file = "non_participating.txt"

# Read all subreddits
with open(all_subreddits_file, "r", encoding="utf-8") as f:
    all_subreddits = {line.strip().lower() for line in f.readlines()}

# Read participating subreddits
with open(participating_file, "r", encoding="utf-8") as f:
    participating_subreddits = {line.strip().lower() for line in f.readlines()}

# Find subreddits not in participating list
non_participating = all_subreddits - participating_subreddits

# Write to the output file
with open(non_participating_file, "w", encoding="utf-8") as f:
    for subreddit in sorted(non_participating):
        f.write(subreddit + "\n")

print(f"✅ Done! Saved {len(non_participating)} non-participating subreddits to {non_participating_file}.")
