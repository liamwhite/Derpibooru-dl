Derpibooru Downloader

Usage:
Run derpibooru_dl.py to create settings files.
Copy and paste your API key from https://derpibooru.org/users/edit to the appropriate line in config\derpibooru_dl_config.cfg
e.g.
api_key = Ap1k3Yh3Re

Put the tags you want to download in config\derpibooru_dl_tag_list.txt, one tag per line
e.g.
Tag1
tag_2
tag+3
T4g 4

Run derpibooru_dl.py again to download the tags you set.
After a tag has been processed, it will be written to the file config\derpibooru_done_list.txt

The API used for the tag mode is depricated, use search mode instead. It should behave the same.