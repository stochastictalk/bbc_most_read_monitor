# BBC Most Read monitor

This application logs and visualizes the most-read articles on bbc.co.uk over time.

Configure BBC Most Read to be logged every 15 minutes (Linux):  
`crontab -e`  
`0,15,30,45 * * * * /home/jerome/anaconda3/python3 /home/jerome/Documents/headline_monitor/log_bbc_most_read.py`
