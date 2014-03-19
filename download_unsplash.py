import os
from multiprocessing.dummy import Pool

import requests

POSTS_ENDPOINT = 'http://api.tumblr.com/v2/blog/unsplash.com/posts'


def download_photo(url):
  dl_res = requests.get(url, allow_redirects=True)
  with open(os.path.join('photos', os.path.basename(dl_res.url)), 'wb') as f:
    f.write(dl_res.content)
    print "Downloaded {}".format(dl_res.url)


def main():
  photo_urls = set()
  offset = 0
  print "Getting photo urls..."
  while True:
    res = requests.get(POSTS_ENDPOINT,
                       params=dict(api_key=os.environ['API_KEY'],
                                   offset=offset)).json()['response']
    if not len(res['posts']):
      break
    for post in res['posts']:
      link_url = post.get('link_url')
      if link_url:
        photo_urls.add(link_url)
    offset += 20
  if not os.path.exists('photos'):
    os.mkdir('photos')
  print "Downloading {} photos...".format(len(photo_urls))
  pool = Pool(10)
  pool.map(download_photo, photo_urls)
  pool.close()
  pool.join()
  print "Done."


if __name__ == '__main__':
  main()

