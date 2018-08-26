import urllib.request
import re
import csv


# link of first video in the playist of all videos (channel home -> videos -> watch all)
FIRST_VIDEO_LINK = "https://www.youtube.com/watch?v=LJnpwL-2Drc&list=UUOYWgypDktXdb-HfZnSMK6A"

# total number of videos, only for progress bar, not necessary
NB_VIDEOS = 157

# path of the .csv file in which the data will be saved
CSV_PATH = "yt_data.csv"


def print_progress_bar (current_iter, max_iter):
    percentage = 100 * (current_iter / max_iter)
    bar = '█' * int(percentage) + '-' * (100 - int(percentage))
    print('\r |%s| %.2f%% ' % (bar, percentage), end = '\r' if current_iter < max_iter else '\n')


links = [FIRST_VIDEO_LINK]
current = 0
data = []

while current < len(links):
    print_progress_bar(current, NB_VIDEOS - 1)

    fp = urllib.request.urlopen(links[current])
    fcontent = fp.read()
    html = fcontent.decode("utf8").replace(u'\xa0', u' ')
    fp.close()

    regexp_str = """
                    "interactionCount"\ content="(?P<views_count>[0-9]+)"[\S\s]+?   # number of views
                    "datePublished"\ content="(?P<date_published>[0-9-]+)"[\S\s]+?  # publication date
                    like-button-unclicked[\S\s]+?>(?P<likes_count>[0-9 ]+)<[\S\s]+? # number of likes
                    dislike-button-unclicked[\s\S]+?>(?P<dislikes_count>[0-9 ]+)<   # number of dislikes
                 """

    regexp = re.compile(regexp_str, re.VERBOSE)

    match = regexp.search(html)

    if match:
        views = match.group('views_count')
        date = match.group('date_published')
        likes = match.group('likes_count').replace(' ', '')
        dislikes = match.group('dislikes_count').replace(' ', '')

        data += [(date, views, likes, dislikes)]

        next_link_match = re.search(r"""<span class="index">\s+""" + str(len(links) + 1) + """\s+<\/span>\s+<a href="(\S+)" """, html)
        while next_link_match:
            next_link = "https://www.youtube.com" + next_link_match[1]
            links += [next_link]
            next_link_match = re.search(r"""<span class="index">\s+""" + str(len(links) + 1) + """\s+<\/span>\s+<a href="(\S+)" """, html)

    else:
        print("Error: statistics from video n-" + str(current) + " could not be retrieved.")

    current += 1


with open(CSV_PATH, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(data)

    print("Data from %d videos have been written in %s." % (len(data), CSV_PATH))
