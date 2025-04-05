print("0")
import praw
import pandas as pd
import time
import os
from datetime import datetime

# --- Reddit API Setup ---

secret = os.environ.get("SECRET") # how to get: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
client_id = os.environ.get("CLIENT_ID")
user_agent = os.environ.get("USER_AGENT")
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent=user_agent
)
# reddit = praw.Reddit(
#     client_id='Km3RG-Lpgs_EomrtCTlILg',
#     client_secret='3_OaI082ccco6zPDD2twpUTn8JQs0w',
#     user_agent='script:praw_scrape_data:v1.0 (by u/thenormsofink)'
# )

def to_timestamp(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())

def get_fullname_from_url(url):
    submission = reddit.submission(url=url)
    print(submission.fullname)
    if submission.fullname.startswith('t3_'):
      return submission.fullname[3:]
    return submission.fullname

def extract_submission_metadata(submission):
    return {
    'author': str(getattr(submission, 'author', None)),
    'author_flair_text': getattr(submission, 'author_flair_text', None),
    'created_utc': getattr(submission, 'created_utc', None),
    'distinguished': getattr(submission, 'distinguished', None),
    'edited': getattr(submission, 'edited', None),
    'id': getattr(submission, 'id', None),
    'is_self': getattr(submission, 'is_self', None),
    'is_original_content': getattr(submission, 'is_original_content', None),
    'locked': getattr(submission, 'locked', None),
    'num_comments': getattr(submission, 'num_comments', None),
    'over_18': getattr(submission, 'over_18', None),
    'poll_data': getattr(submission, 'poll_data', None),
    'score': getattr(submission, 'score', None),
    'spoiler': getattr(submission, 'spoiler', None),
    'stickied': getattr(submission, 'stickied', None),
    'title': getattr(submission, 'title', None),
    'upvote_ratio': getattr(submission, 'upvote_ratio', None),
    'hidden': getattr(submission, 'hidden', None),
    'user_reports': getattr(submission, 'user_reports', None),
    'can_mod_post': getattr(submission, 'can_mod_post', None),
    'mod_note': getattr(submission, 'mod_note', None),
    'banned_by': getattr(submission, 'banned_by', None),
    'author_flair_type': getattr(submission, 'author_flair_type', None),
    'likes': getattr(submission, 'likes', None),
    'banned_at_utc': getattr(submission, 'banned_at_utc', None),
    'view_count': getattr(submission, 'view_count', None),
    'archived': getattr(submission, 'archived', None),
    'pinned': getattr(submission, 'pinned', None),
    'mod_reason_by': getattr(submission, 'mod_reason_by', None),
    'removal_reason': getattr(submission, 'removal_reason', None),
    'report_reasons': getattr(submission, 'report_reasons', None),
    'mod_reports': getattr(submission, 'mod_reports', None),
    'flair': getattr(submission, 'link_flair_text', None),
    'mod': getattr(submission, 'mod', None),
    'selftext': getattr(submission, 'selftext', None),
}


def extract_comments(submission):
    submission.comments.replace_more(limit=None)
    all_comments = []
    for c in submission.comments.list():
        all_comments.append({
            'submission_id': submission.id,
            'comment_id': c.id,
            'author_is_blocked': getattr(c, 'author_is_blocked', None),
            'comment_type': getattr(c, 'comment_type', None),
            'mod_reason_by': getattr(c, 'mod_reason_by', None),
            'banned_by': getattr(c, 'banned_by', None),
            'author_flair_type': getattr(c, 'author_flair_type', None),
            'likes': getattr(c, 'likes', None),
            'user_reports': getattr(c, 'user_reports', None),
            'banned_at_utc': getattr(c, 'banned_at_utc', None),
            'mod_reason_title': getattr(c, 'mod_reason_title', None),
            'archived': getattr(c, 'archived', None),
            'collapsed_reason_code': getattr(c, 'collapsed_reason_code', None),
            'no_follow': getattr(c, 'no_follow', None),
            'author': str(c.author),
            'can_mod_post': getattr(c, 'can_mod_post', None),
            'created_utc': c.created_utc,
            'send_replies': getattr(c, 'send_replies', None),
            'parent_id': c.parent_id,
            'score': c.score,
            'approved_by': getattr(c, 'approved_by', None),
            'mod_note': getattr(c, 'mod_note', None),
            'all_awardings': getattr(c, 'all_awardings', None),
            'collapsed': getattr(c, 'collapsed', None),
            'body': c.body,
            'edited': c.edited,
            'downs': getattr(c, 'downs', None),
            'distinguished': c.distinguished,
            'stickied': c.stickied,
            'score_hidden': getattr(c, 'score_hidden', None),
            'report_reasons': getattr(c, 'report_reasons', None),
            'author_flair_text': c.author_flair_text,
            'treatment_tags': getattr(c, 'treatment_tags', None),
            'controversiality': getattr(c, 'controversiality', None),
            'depth': getattr(c, 'depth', None),
            'flair_text': getattr(c, 'flair_text', None),
            'link_id': getattr(c, 'link_id', None),
            'subreddit_name_prefixed': getattr(c, 'subreddit_name_prefixed', None),
            'author_flair_background_color': getattr(c, 'author_flair_background_color', None),
            'collapsed_because_crowd_control': getattr(c, 'collapsed_because_crowd_control', None),
        })
    return all_comments

def save_checkpoints(sub_data, comment_data, subreddit):
    pd.DataFrame(sub_data).to_csv(f'/users/Preethi/social_computing/checkpoint_submissions_{subreddit}.csv', index=False)
    pd.DataFrame(comment_data).to_csv(f'/users/Preethi/social_computing/checkpoint_comments_{subreddit}.csv', index=False)
    print(f"💾 Checkpoint saved ({len(sub_data)} submissions, {len(comment_data)} comments)")

def save_final(sub_data, comment_data, subreddit, cutoff_date):
    pd.DataFrame(sub_data).to_csv(f'/users/Preethi/social_computing/{subreddit}_until_{cutoff_date}_submissions.csv', index=False)
    pd.DataFrame(comment_data).to_csv(f'/users/Preethi/social_computing/{subreddit}_until_{cutoff_date}_comments.csv', index=False)
    print(f"✅ Final saved: {len(sub_data)} submissions, {len(comment_data)} comments")

def crawl_submissions(subreddit_name, start_url, cutoff_date, checkpoint_every=10000):
    after = get_fullname_from_url(start_url)
    cutoff_ts = to_timestamp(cutoff_date)
    print("2")
    submission_data, comment_data = [], []
    seen_ids = set()

    # Resume if checkpoint exists
    sub_cp = f'/users/Preethi/social_computing/checkpoint_submissions_{subreddit_name}.csv'
    com_cp = f'/users/Preethi/social_computing/checkpoint_comments_{subreddit_name}.csv'
    if os.path.exists(sub_cp):
        submission_data = pd.read_csv(sub_cp).to_dict('records')
        seen_ids = set([s['id'] for s in submission_data])
        comment_data = pd.read_csv(com_cp).to_dict('records')
        after = 't3_' + submission_data[-1]['id']
        print(f"📦 Resuming from checkpoint with {len(submission_data)} submissions")

    count = len(submission_data)
    print("3")
    while True:
        try:
            posts = list(reddit.subreddit(subreddit_name).new(limit=1000, params={'after': after}))
            if not posts:
                print("✅ No more posts.")
                break

            for post in posts:
                if post.id in seen_ids:
                    continue
                if post.created_utc < cutoff_ts:
                    print("⏹ Reached cutoff timestamp.")
                    save_checkpoints(submission_data, comment_data, subreddit_name)
                    return submission_data, comment_data

                sub_meta = extract_submission_metadata(post)
                submission_data.append(sub_meta)
                seen_ids.add(post.id)

                comment_data.extend(extract_comments(post))
                after = post.fullname
                if after.startswith('t3_'):
                    after = after[3:]
                count += 1

                if count % checkpoint_every == 0:
                    save_checkpoints(submission_data, comment_data, subreddit_name)
                print("4")
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            print("⏳ Retrying in 10s...")
            time.sleep(10)

    save_checkpoints(submission_data, comment_data, subreddit_name)
    return submission_data, comment_data

def main():
    subreddits = {
        'Autism' : 'https://www.reddit.com/r/autism/comments/14mch6v/i_absolutely_hate_the_hiring_process/',
        # 'ChronicPain' : 'https://www.reddit.com/r/ChronicPain/comments/14rrkbl/anyone_taking_opioids_for_chronic_pain/',
        # 'MentalHealth' : 'https://www.reddit.com/r/mentalhealth/comments/14lx624/a_lot_of_nights_i_never_want_to_sleep_and_i_dont/'
        # 'Autism' : 'https://www.reddit.com/r/autism/comments/1jpg4bk/working_on_an_oc_animatic_for_a_school_project/',
        # 'interestingasfuck': 'https://www.reddit.com/r/interestingasfuck/comments/15f0l11/the_salt_cathedral_in_poland/',
        # 'thatsinsane': 'https://www.reddit.com/r/ThatsInsane/comments/15fegr6/consecutive_backflips/',
        # 'malefashionadvice': 'https://www.reddit.com/r/malefashionadvice/comments/15rwsr1/daily_questions_ask_and_answer_here_15_august_2023/'
    }
    # cutoff_date = '2025-04-01'
    cutoff_date = '2023-05-24'

    for sub, url in subreddits.items():
        print(sub)
        submissions, comments = crawl_submissions(sub, url, cutoff_date)
        save_final(submissions, comments, sub, cutoff_date)

if __name__ == "__main__":
    print("1")
    main()
