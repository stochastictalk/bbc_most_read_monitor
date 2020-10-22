# -*- utf-8 -*-

from datetime import date
import utilities as utils

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
    n_days = (start_date - end_date).days
    minutes_in_day = 24*60
    n_periods = int((n_days*minutes_in_day)/period)
    n_capture_events = n_periods + 1 # |----|----|, get it?
    n_headlines_generated = n_capture_events*10

    # 2. Sample the headlines.
    headlines = sample_synthetic_headlines(n_headlines_generated)

    # 3. Associate the headlines with a rank, URL, and timestamp.


    # 4. Write the resulting data set to a PostgreSQL relation.
    relation_name = 'synthetic_headlines'
    utils.write_to_sql(lits_of_headline_dcts)
