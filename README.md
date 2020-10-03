# Headline monitor


Configure BBC most read to be logged every 15 minutes (on Linux):  
`crontab -e`  
`0,14,29,44 * * * * python3 ~/Documents/headline_monitor/log_bbc_most_read.py`
