# -*- utf-8 -*-

from datetime import date, datetime, timedelta
import utilities as utils
from itertools import accumulate
import requests
import random

random.seed(1)

def write_synthetic_headlines(start_date: date, end_date: date, period: int):
    ''' Creates PostgreSQL relation 'synthetic_headlines' containing fields
        RANK, HEADLINE, URL, TIMESTAMP at interval 'period' between 00:00 on
        'start_date' and 00:00 on 'end_date'.

        Args:
            start_date (date): is a datetime.date
            end_date (date): is a datetime.date
            period (int): in minutes

        Returns:
            nothing
    '''

    # 1. Compute the number of headlines to generate.
    start_date = datetime(start_date.year, start_date.month,
                          start_date.day, 0, 0)
    end_date = datetime(end_date.year, end_date.month,
                        end_date.day, 0, 0)
    n_days = (end_date - start_date).days
    minutes_in_day = 24*60
    n_periods = int((n_days*minutes_in_day)/period)
    n_capture_events = n_periods + 1 # |----|----|, get it?
    n_headlines_generated = n_capture_events*10
    time_delta = timedelta(minutes=period)

    # 2. Sample the headlines, urls, ranks, and timestamps
    headlines = sample_synthetic_headlines(n_headlines_generated)
    urls = sample_synthetic_urls(n_headlines_generated)
    ranks = (1 + (j % 10) for j in range(n_headlines_generated))
    timestamps = (int((start_date + j*time_delta).timestamp())
                                        for j in range(n_capture_events)
                                                            for k in range(10))
    # nb interior iterator changes slowest, exterior iterator  changes fastest

    # 3. Associate the headlines with a rank, URL, and timestamp.
    h_u_r_ts = zip(headlines, urls, ranks, timestamps)
    iter_of_headline_dcts = ({'headline':v[0], 'url':v[1],
                              'rank':v[2], 'timestamp':v[3]} for v in h_u_r_ts)

    # 4. Write the resulting data set to a PostgreSQL relation.
    #for val in iter_of_headline_dcts:
    #    print(val)
    relation_name = 'synthetic_headlines'
    utils.write_to_sql(iter_of_headline_dcts, relation_name)

def sample_synthetic_headlines(n: int):
    src_url = 'http://shakespeare.mit.edu/Poetry/VenusAndAdonis.html'
    src_text = requests.get(src_url).text
    str_to_strip = ['<BR>', '<BLOCKQUOTE>', '</BLOCKQUOTE>']
    for s in str_to_strip: src_text = src_text.replace(s, ' ')
    lines = [strip(s) for s in src_text.split(r'\n')]
    min_line_length = 10
    filtered_lines = [s for s in lines if len(s) > min_line_length]
    print('Sampling synthetic headlines from a set of {}.'.format(
                                                            len(filtered_lines))
    return(random.choices(filtered_lines, k=n))


def sample_synthetic_urls(n: int):
    return ('/news-england-hello-world-{}'.format(k+1) for k in range(n))

start_date = date(2020, 10, 22)
end_date = date(2020, 10, 23)
period = 5 # minutes
write_synthetic_headlines(start_date, end_date, period)
