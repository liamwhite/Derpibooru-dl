# Derpibooru Downloader

## Instalation and configuration
There are two ways to run Derpibooru_dl, from a windows executable or directly from the script itself.

### Standalone executable version for Windows
- Suggested for anyone without programming experience.
- This only contains the downloader itself.
- Download the latest version (In green at the top) from https://github.com/woodenphone/Derpibooru-dl/releases
- Extract the contents of the .zip into a folder.
- Read the configuration section for the next steps.

### Python scripts
- This is only suggested for those with experience in using python.
- You need to have Python version **2.6 or 2.7** installed first. [You can download it here.
](https://www.python.org/download/)
- Then you need pip installed. [See here for the docs](http://pip.readthedocs.org/en/latest/installing.html).
- Then in your command line, do `pip install mechanize derpybooru`.
- Read the configuration section for the next steps.

### Configuration and running for all versions
- We need to run derpibooru_dl to create settings files.
    - On Windows, using the standalone executable version, run `derpibooru_dl.exe`.
    - On Windows, macOS and GNU/Linux, run `python derpibooru_dl.py` in a command line terminal.
- Without a valid API key you will not be able to download anything not visible in the default guest view.
- Copy your API key from [https://derpibooru.org/users/edit](https://derpibooru.org/users/edit)
- Past it to the appropriate line in the `derpibooru_dl_config.cfg` inside the `config` folder. (e.g. `api_key = Ap1k3Yh3Re`)
- Put the queries you want to download in `derpibooru_dl_tag_list.txt` in the `config` folder, with one query per line.
- Full derpibooru search syntax MAY be available. Syntax guide is available at [https://derpibooru.org/search/syntax](https://derpibooru.org/search/syntax)
- If your query works on the site but not in this script, please send a private message to my account "misspelledletter" on derpibooru.
- Example of query list.
````
Tag1
tag_2
tag+3
T4g 4
tag-five || tag-six
````
- Run derpibooru_dl again to download your set.
- After a tag has been processed, it will be written to the file `derpibooru_done_list.txt`, in the `config` folder.
- Derpibooru-dl will close itself after it has finished.

### Explaination of settings:
For boolean (yes or no) settings, use these: `True` or `False` (case sensitive!)

````ini
[Login]
api_key = **Key used to access API (You will need to fill this in.)**

[Download]
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
save_comments = **Should image comments be requested and saved, uses more resources on both client and server.**

[General]
show_menu **Should a text based menu be shown instead of automatically running the batch mode?**
hold_window_open = **Should the window be kept open after all tasks are done, to allow the user to confirm the program worked**
````

### Example of typical settings
- This configuration should be fine for most users
- Make sure to use your own API key, the one here is just an example
````ini
[Login]
api_key = Replace_this_with_your_API_key

[Download]
reverse = False
output_folder = download
download_submission_ids_list = True
download_query_list = True
output_long_filenames = False
input_list_path = config\derpibooru_dl_tag_list.txt
done_list_path = config\derpibooru_done_list.txt
failed_list_path = config\derpibooru_failed_list.txt
save_to_query_folder = True
skip_downloads = False
sequentially_download_everything = False
go_backwards_when_using_sequentially_download_everything = False
download_last_week = False
skip_glob_duplicate_check = False
skip_known_deleted = True
deleted_submissions_list_path = config\deleted_submissions.txt
move_on_fail_verification = False
save_comments = False

[General]
show_menu = True
hold_window_open = True
````

### Tips and Fixes
- When editing settings or input lists, you may find that your text editor does not display items on different lines properly.
    - This is probably due to the text editor you are using, try using a different editor, such as notepad++
    - Known incompatible editors:
    ````
    Microsoft Notepad (Ships with Windows)
    ````
    - Known compatible editors:
    ````
    Notepad++ [http://www.notepad-plus-plus.org/](http://www.notepad-plus-plus.org/)
    ````
- ~~I've written a guide with screenshots for the windows .exe releases. [Guide link](http://evil-vortex.com/Guide_2014-10-28.pdf)~~
