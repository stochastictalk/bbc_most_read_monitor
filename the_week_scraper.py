import requests
import bs4 as bs
from datetime import datetime
from os import mkdir

# Make directory for today's entry
date_string = datetime.today().strftime('%a_%d_%m_%y')
dst_dir = './data/The Week front pages/' + date_string
mkdir(dst_dir)

# Get URLs for images of today's papers from The Week
url = 'https://www.theweek.co.uk/front-pages/101385/todays-front-pages'
r = requests.get(url)
soup = bs.BeautifulSoup(r.text, 'html.parser')
img_tags = soup.find_all('img')
img_filepaths = [tag.attrs['src'] for tag in img_tags]

# Download the images and save them
for j, fp in enumerate(img_filepaths):
	fp = fp.strip()
	if fp[-3:] in 'jpgpegpng':
		r = requests.get(fp)
		dst_fp = dst_dir + '/' + str(j).zfill(3) + fp[-4:]
		dst_file = open(dst_fp, 'wb')
		dst_file.write(r.content)
		dst_file.close()

print('Downloaded and saved all images.')
