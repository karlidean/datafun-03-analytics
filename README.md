# datafun-03-analytics
44608 - Data Analytics Fundamentals - Week 3 of 7

# Setting Up the Repo for Project Work
1. Created Repo in Github
2. Copied Repo link and went into Powershell using 'cd C:\Repos' followed by 'git clone (project link)'
3. Created '.gitignore' using VS and added contents from example repo
4. Created 'requirements.txt' using VS and added contents from example repo
5. Committed the additions of my '.gitignore' and 'requirements.txt' files to GitHub
6. Pushed all changes
7. Created my '.venv' and activated it
    I am aware that I will have to reactivate this upon re-entry to VS Code
8. Formatting changes with README
9. Pushed all changes

# P3: Python Data Project
1. Added `requests` and `openpyxl` to my `requirements.txt` file

## Fetching the `.csv` File
1. Implemented example script from example repo.
2. Modified the script to use a file that fetched 2019 Division 1 women's volleyball game score data via a link and wrote a `.csv` file that contains the contents from the link. `karlidean_get_csv.py`
   1. This script wrote file `2019_NCAA_Womens_Volleyball.csv` and implemented it into folder `karlidean_data`
3. Add - Commit - Push

## Fetching the `.txt` File
1. Implemented example script from example repo.
2. Modified the script to use a file that fetched Genesis from the Bible via a link and wrote a `.txt` file that contains the contents of that from the link. `karlidean_get_text.py`
   1. This script fetched the CSV and wrote a file `genesis.txt` and implemented it into folder `karlidean_data`
3. Add - Commit - Push
   
## Fetching the `.json` File
1. Implemented example script from example repo.
2. Modified the script to use a file that fetched data on the stars in the night sky via a link and wrote a `.json` file that contains the contents of that from the link. `karlidean_get_json.py`
   1. This script fetched the CSV and wrote a file `stars.json` and implemented it into folder `karlidean_data`
3. Add - Commit - Push

## Fetching the `.xlsx` File
1. Implemented example script from example repo.
2. Modified the script to use a file that fetched data on the technology sales, dates, amounts, and more via a link and wrote a `.xlsx` file that contains the contents of that from the link. `karlidean_get_excel.py`
   1. This script fetched the CSV and wrote a file `ssles.xlsx` and implemented it into folder `karlidean_data`
3. Add - Commit - Push

## Processing the `.xlsx` Fiile
1. Implemented the example processing script from the example processing repo.
2. Modified the script to use the fetched data file `sales.xlsx` and pull the number of how many sales were from the Central Region. In the file, you can find this in column B.
3. This processing script analyzed the `.xlsx` , counted the number of Central Region sales, and wrote a file called `excel_sales_central_count.txt` and put it in a new folder called `karlidean_processed`
4. Add - Commit - Push

## Processing the `.csv` Fiile
1. Implemented the example processing script from the example processing repo.
2. Modified the script to use the fetched data file `2019_NCAA_Womens_Volleyball.csv` and find the percentage of times the home team won during the 2019 NCAA Women's Volleyball Season.
3. This processing script analyzed the `.csv` , analyzed the percentage of times the home team won, and wrote a file called `home_court_advantage.txt` and put it in a folder called `karlidean_processed`
4. Add - Commit - Push

## Processing the `.json` Fiile
1. Implemented the example processing script from the example processing repo.
2. Modified the script to use the fetched data file `stars.json` and understand the different spectral groupings for stars, counting up which stars used what spectral grouping notation.
3. This processing script analyzed the `.json` , counted stars by their spectral grouping, and wrote a file called `stars_by_spectral_group.txt` and put it in a folder called `karlidean_processed`
4. Add - Commit - Push

## Processing the `.txt` Fiile
1. Implemented the example processing script from the example processing repo.
2. Modified the script to use the fetched data file `genesis.txt` and understand how many times "God" was said in the Bible's Genesis 1.
3. This processing script analyzed the `.txt` , counting the number of times Genesis 1 said "God", put it in  `text_God_word_count.txt` and put it in a folder called `karlidean_processed`
4. Add - Commit - Push