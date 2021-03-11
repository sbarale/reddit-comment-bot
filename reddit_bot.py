import praw
import config
import time
import os
import comments.yoda as yoda


def bot_login():
    print("Logging in...")
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="The Reddit Commenter v1.0")
    print("Logged in!")

    return r


def run_bot(r, comments_replied_to, exclusion_list):
    print("Searching last 1,000 comments")

    for comment in r.subreddit('mycomfortlevel').comments(limit=1000):
        if comment.id not in comments_replied_to \
                and comment.author != r.user.me() \
                and not comment.author.is_mod \
                and not comment.author.is_employee \
                and comment.author not in exclusion_list:

            if "opt-out" in comment.body:
                print("Removing user " + comment.author.id)
                append_file("unsubscribed_authors.txt", comment.author.id)
                break

            print("Found comment to work on: " + comment.id)
            response = yoda.talk(comment.body)
            if response:
                comment.reply(build_reply(comment,response))
                print("Replied to comment " + comment.id)
                print("with " + response)
                comments_replied_to.append(comment.id)
                append_file("comments_replied_to.txt", comment.id)

        else:
            print("Comment " + comment.id + " has either been replied to or is one of mines")
        time.sleep(2)

    print("Search Completed.")

    print(comments_replied_to)

    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds...
    time.sleep(10)


def append_file(name, content):
    if not os.path.isfile(name):
        with open(name, "w") as f:
            f.write(content + "\n")
    else:
        with open(name, "a") as f:
            f.write(content + "\n")


def get_file(name):
    if not os.path.isfile(name):
        content = []
    else:
        with open(name, "r") as f:
            content = f.read()
            content = content.split("\n")
            # content = filter(None, content)

    return content


def build_reply(comment, response):
    response = "**" + response + "**"
    response += "\n\n-*" + comment.author.name + "*"
    response += "\n\n\n\n\n\n\n\n^(Commands: 'opt-out')"
    return response


r = bot_login()
replied_comments = get_file("comments_replied_to.txt")
print(replied_comments)
ignore_list = get_file("unsubscribed_authors.txt")
print(ignore_list)

while True:
    run_bot(r, replied_comments, ignore_list)
