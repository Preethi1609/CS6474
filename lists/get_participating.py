import re

def extract_subreddits(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    
    subreddit_pattern = re.compile(r'^r/\w+$')
    
    subreddits = [line.strip() for line in content if subreddit_pattern.match(line.strip())]
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(subreddits))

if __name__ == "__main__":
    file_path = "participating.txt"  # Change this to your file name
    output_file = "scraped_participating.txt"
    extract_subreddits(file_path, output_file)
