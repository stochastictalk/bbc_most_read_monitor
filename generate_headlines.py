# -*- utf-8 -*-

from datetime import date

def generate_headlines(start_date: date, end_date: date, period: int):
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
