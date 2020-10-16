# Headline monitor


Configure BBC Most Read to be logged every 15 minutes (Linux):  
`crontab -e`  
`0,15,30,45 * * * * /home/jerome/anaconda3/python3 /home/jerome/Documents/headline_monitor/log_bbc_most_read.py`
