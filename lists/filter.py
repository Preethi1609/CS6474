# Input files
all_subreddits_file = "all_subreddits.txt"
participating_file = "scraped_participating.txt"
non_participating_file = "non_participating1.txt"

# Read all subreddits in original order
with open(all_subreddits_file, "r", encoding="utf-8") as f:
    all_subreddits = [line.strip().lower() for line in f.readlines()]

# Read participating subreddits as a set for fast lookup
with open(participating_file, "r", encoding="utf-8") as f:
    participating_subreddits = {line.strip().lower() for line in f.readlines()}

# Filter subreddits that are NOT in participating list
non_participating = [sub for sub in all_subreddits if sub not in participating_subreddits]

# Write to the output file without sorting
with open(non_participating_file, "w", encoding="utf-8") as f:
    for subreddit in non_participating:
        f.write(subreddit + "\n")

print(f"✅ Done! Saved {len(non_participating)} non-participating subreddits to {non_participating_file}.")
