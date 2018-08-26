import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# path of the .csv file in which the data are stored
CSV_PATH = "yt_data.csv"


with open(CSV_PATH, 'r') as csvfile:
    data = list(csv.reader(csvfile))
    dates, views, likes, dislikes = zip(*data)

    dates = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]

    new_dates = [dates[0]]
    mean_views = [0]
    mean_likes = [0]
    mean_dislikes = [0]

    month = dates[0].month
    year = dates[0].year
    vids_in_month = 1

    for i, date in enumerate(dates):
        if date.month != month or date.year != year:
            mean_views[len(mean_views) - 1] /= vids_in_month
            mean_likes[len(mean_likes) - 1] /= vids_in_month
            mean_dislikes[len(mean_dislikes) - 1] /= vids_in_month

            month = date.month
            year = date.year

            new_dates.append(date)
            mean_views.append(0)
            mean_likes.append(0)
            mean_dislikes.append(0)

            vids_in_month = 0

        vids_in_month += 1
        mean_views[len(mean_views) - 1] += int(views[i])
        mean_likes[len(mean_likes) - 1] += int(likes[i])
        mean_dislikes[len(mean_dislikes) - 1] += int(dislikes[i])

    likes_dislikes_ratio = [mean_likes[i] / mean_dislikes[i] for i in range(len(mean_likes))]

    fig, ax1 = plt.subplots()
    ax1.plot(new_dates, mean_views, 'g-', label='views')
    ax1.legend()

    ax2 = ax1.twinx()
    ax2.plot(new_dates, mean_likes, 'b:', label='likes')
    ax2.plot(new_dates, mean_dislikes, 'r:', label='dislikes')
    ax2.legend()

    """
    ax3 = ax1.twinx()
    ax3.plot(new_dates, likes_dislikes_ratio, 'y--', label='ratio')
    ax3.legend()
    """

    plt.gcf().autofmt_xdate()
    plt.show()
