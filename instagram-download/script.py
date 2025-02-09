from instagrapi import Client

client = Client()

username = "factsdailyy"
user = client.user_info_by_username(username).dict()
print(f"Info of '{username}': {user}")

clips = client.user_clips_v1(username["pk"], amount=1)
print(f"Reels: {clips[0].dict()}")