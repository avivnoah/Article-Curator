# Article Curator



Implemented a a full-stack machine-learning-powered system that recommends articles based on my personal preferences.

## Demo

Behind the  scenes...🤔
![Demo](demo.gif)
<video width="800" controls>
  <source src="output.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

[!demo]https://github.com/avivnoah/Article-Curator/blob/8344b8504047d7c80c3830b8b3d4b35501a7befc/2025-04-17%2020-19-33.webm

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
