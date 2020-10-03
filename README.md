# Headline monitor


Configure BBC most read to be logged every 15 minutes (on Linux):  
`crontab -e`  
`14,29,44,59 * * * * /home/jerome/anaconda3/python3 /home/jerome/Documents/headline_monitor/log_bbc_most_read.py`
