# Article Curator



Implemented a webcrawler using Playwright to scan webpage URLs and extract data, Progressively optimized data acquisition, improving speed and efficiency.

## Demo
Behind the  scenes...🤔

https://github.com/user-attachments/assets/e76e805e-3f12-44fc-8bd5-1f7b21a02fae


## Installation

### Steps:
###### 1. Clone the repository.
###### 2. Navigate to the project directory/Installation_files_run_once
###### 3. Run the Packages_installer.bat file to make sure you have the required python libraries to run the project.
###### 4. Once the file closes itself you can continue.
#### Installation note: to make sure you can use the library_install.bat file, you need to make sure your pip & python Path environment system variables are "correlated". or install them manually, but it's not as fun.

```bash
  pip install concurrent playwright_stealth pytest-playwright multiprocessing time sys
```


### This is still in progress, to implement: 
##### 1. Store the data in a database, sorted by: 'read', 'favorite', etc, with links, to store data with links next to it so i wouldn't need to load all articles every time.
##### 2. finish learning NLP before implementing the last step which utilizes an ML model i'll build to filter out content for me
##### 3. Time lib is needed for edge-case testing, will get rid of it when finished.
#### Note: this code snippet: launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/webkit-1992/playwright.exe", headless=HEADLESS_VALUE) uses an executable path which is local and specific to my computer, you can drop the executable_path and try running gather_website_links without it, it should work, my solution was temporary as my pytest-playwright went weird and I wasn't gonna spend a few days on finding a non very imporant solution to a not very interesting problem I faced.
