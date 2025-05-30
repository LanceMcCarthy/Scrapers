# KB Downloader

| Required | Argument | Type | Description |
|----------|----------|------|-------------|
| ✅ | `--csv_file` | string |Path to the csv file containing a list of KB urls |
| ❌ | `--output_folder_name` | string | (default: download_timestamp) Folder name to save the results in (relative to working directory) |
| ❌ | `--concatenate` | bool | (default: True) Changes behavior to save to single file or separate files  |

## Instructions

The only required argument is the source CSV file, the download folder is automatically created for you and timestamped for each unique run. 

`python kbdownloader.py --csv_file "UrlList.csv"`

> [!IMPORTANT]
> It is recommended to use the default concatenation option if this data is for Copilot Studio use; it has a maximum limit of 500 files and you can only upload 15 at a time. A single file works well as long as the data is clearly separated

## Examples

Running this against 13,788 Sitefinity KB articles resulted in a single txt file with a size of 30 Mb:

`python kbdownloader.py --csv_file "sitefinity-urls.csv"`

![image](https://github.com/user-attachments/assets/20fe23b5-24bf-42a4-9d48-efe1544dbfd6)

Using this data in Copilt has promising results

![image](https://github.com/user-attachments/assets/930d0bd3-4c49-4ae8-b6a5-a21f0ecb190d)


Running with with concatenation disabled, results in 13,788 separate files at ~25kb each.

`python kbdownloader.py --csv_file "sitefinity-urls.csv" --output_folder_name "SitefinityKBs" --concatenate False`

## Support

Contact Lance McCarthy with any questions.

## Prerequisite

This script uses python for the easiest compatibility for quick use. If you do not have Python installed, it is quick and easy; just download and run the appropriate installer from [Pythons's official site](https://www.python.org/downloads/). After it is installed, open your favorite command line tool and follow the instructions below.
