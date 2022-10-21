#!/usr/bin/python3
"""Parse the title of all hot articles,
and print a sorted count of given keywords."""

from audioop import reverse
import requests

headers = {'User-Agent': 'MyAPI/0.0.1'}


def count_words(subreddit, word_list, after="", hot_list=[]):

    subreddit_url = "https://reddit.com/r/{}/hot.json".format(subreddit)

    parameters = {'limit': 100, 'after': after}
    response = requests.get(subreddit_url, headers=headers, params=parameters)

    if response.status_code == 200:

        json_data = response.json()
        if (json_data.get('data').get('dist') == 0):
            return

        for child in json_data.get('data').get('children'):
            title = child.get('data').get('title')
            hot_list.append(title)

        after = json_data.get('data').get('after')
        if after is not None:

            return count_words(subreddit, word_list,
                               after=after, hot_list=hot_list)
        else:
            counter = {}
            for word in word_list:
                word = word.lower()
                if word not in counter.keys():
                    counter[word] = 0
                else:
                    counter[word] += 1
            for title in hot_list:
                title_list = title.lower().split(' ')
                for word in counter.keys():
                    search_word = "{}".format(word)
                    if search_word in title_list:
                        counter[word] += 1
            sorted_counter = dict(
                sorted(counter.items(),
                       key=lambda item: item[1], reverse=True))
            for key, value in sorted_counter.items():
                if value > 0:
                    print("{}: {}".format(key, value))

    else:
        return


if __name__ == '__main__':
    count_words("hello", ['REDDIT', 'german', 'HI', 'whynot'])
    count_words('unpopular', ['down', 'vote', 'downvote',
                              'you', 'her', 'unpopular', 'politics'])
