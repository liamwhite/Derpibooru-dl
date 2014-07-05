# Derpibooru Downloader

## Instalation and configuration
### Standalone executable version for Windows
- Download from https://github.com/woodenphone/Derpibooru-dl/releases
- This is an experimental version that only contains the downloader

### Python scripts
- You need to have Python installed first. [You can download it here.
](https://www.python.org/download/)
- Then you need pip installed. [See here for the docs](http://pip.readthedocs.org/en/latest/installing.html).
- Then in your command line, do `pip install mechanize`.

### Configuration for all versions
- We need to run derpibooru_dl to create settings files.
    - On Windows, using the standalone executable version, run `derpibooru_dl.exe`
    - On Windows, run `python derpibooru_dl.py`
    - On Mac and GNU/Linux, run `python derpibooru_dl_nix.py`
- Copy your API key from [https://derpibooru.org/users/edit](https://derpibooru.org/users/edit)
- Past it to the appropriate line in the `derpibooru_dl_config.cfg` inside the `config` folder. (e.g. `api_key = Ap1k3Yh3Re`)
- Put the tags you want to download in `derpibooru_dl_tag_list.txt` always in the `config` file, one tag per line e.g.

````
Tag1
tag_2
tag+3
T4g 4
````
- Run your derpibooru_dl like before again to download your set.
- After a tag has been processed, it will be written to the file `derpibooru_done_list.txt`, again in the `config` folder.

The API used for the tag mode is depricated, use search mode instead. It should behave the same.



### Explaination of settings:
For boolean (yes or no) settings, use these: `True` or `False`

````
[Login]
api_key = **Key used to access API (You will need to fill this in.)**

[Settings]
reverse = **Work backwards**
output_folder = **path to output to**
download_submission_ids_list = **Should submission IDs form the input list be downloaded**
download_query_list = **Should queries from the input list be downloaded**
output_long_filenames = **Should the derpibooru filenames be used? (UNSUPPORTED! USE AT OWN RISK!)**
input_list_path = **Path to a text file containing queries, ids, etc**
done_list_path = **Path to record finished tasks**
failed_list_path = **Path to record failed tasks**
save_to_query_folder = **Should each query/tag/etc save to a folder of QUERY_NAME or use one single folder for everything**
skip_downloads = **Should no downloads be attempted**
sequentially_download_everything = **Should the range download mode try to save every possible submission?**
go_backwards_when_using_sequentially_download_everything = **Start at the most recent submission instead of the oldest when trying to download everything.**
download_last_week = **Should the last 7000 submissions be downloaded (Approx 1 weeks worth)**
skip_glob_duplicate_check = **You should probably not use this unless you know what you are doing. (Speedhack for use with single output folder)**
move_on_fail_verification = **Should files that fail the verification be moved? If false they will only be copied.**
````
