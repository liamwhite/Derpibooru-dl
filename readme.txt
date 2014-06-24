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



Explaination of settings:

True
False


[Login]
api_key = Key used to access API (You will need to fill this in.)

[Settings]
reverse = Work backwards
output_folder = path to output to
download_submission_ids_list = Should submission IDs form the input list be downloaded
download_query_list = Should queries from the input list be downloaded
output_long_filenames = Should the derpibooru filenames be used? (UNSUPPORTED! USE AT OWN RISK!)
input_list_path = Path to a text file containing queries, ids, etc
done_list_path = Path to record finished tasks
failed_list_path = Path to record failed tasks
save_to_query_folder = Should each query/tag/etc save to a folder of QUERY_NAME or use one single folder for everything
skip_downloads = Should no downloads be attempted
sequentially_download_everything = Should the range download mode try to save every possible submission?
go_backwards_when_using_sequentially_download_everything = Start at the most recent submission instead of the oldest when trying to download everything.
download_last_week = Should the last 7000 submissions be downloaded (Approx 1 weeks worth)
skip_glob_duplicate_check = You should probably not use this unless you know what you are doing. (Speedhack for use with single output folder)
skip_known_deleted = Should previously encounterd deleted submissions be skipped?
deleted_submissions_list_path = Relative path to put list of known deleted submissions