# snowball
Set of python scripts to implement the controlled snowball sampling to gather collection of the seminal scientific publications on desired subject

Requirements:
To run the package you need 
* python3 
* [pipenv](https://docs.pipenv.org/)
* MS Academic Search API key

## To get the MS Academic API key
1) Open [Microsoft Research APIs Portal](https://msr-apis.portal.azure-api.net)
2) Sign-in with your existing account (or sign-up if you don't have the account)
3) Subscribe to *Academic Search API* that is part of *Project Academic Knowledge service*
You can find the key as *Primary key* in the *Keys* section.


Quick start:
1) get copy ot this repository with

   ```
   $ git clone https://github.com/gendobr/snowball.git
   ```
   and step inside the *snowball* directory
   The content of the directory is 
   ```
   data  - empty directory to place your data  
   docs  - place to additinal documentation
   Pipfile  - list of required packages
   README.md - this file
   scripts - python code
   ```

2) copy the directory ./docs/data into  ./data/YOUR_DATA_DIRECTORY
   ```
   $ cp -R docs/data ./data/example
   ```
   and paste the MS Academic Search API key as value of 
   `subscriptionKey` parameter in the configuration file
   `./data/YOUR_DATA_DIRECTORY/config.ini`

3) install all required python packages with 
   ```
   pipenv install
   ```
   
4) download the required NLTK packages
   ```
   $ pipenv run python scripts/init.py
   ```

5) Find 10 - 20 seed publications in the
   [Microsoft Academic search engine](https://academic.microsoft.com/).

   Each seed publication should be
   * be relevant to your search topic
   * have high citation index (however not extremely high)
   * be up 7-10 years old

   Paste the publication ids in the `./data/YOUR_DATA_DIRECTORY/in-seed.csv` file.
   One id per row

   The publication id is the long number in publication URL.
   For instance, in the URL https://academic.microsoft.com/paper/2899429816/citedby/ 
   publication id is 2899429816

6) run one-after-one the following files (don't forget to change the `../data/GAN/` to `../data/YOUR_DATA_DIRECTORY/` )
inside each file

- 000_download.sh  - may take several hours time to download up to 20000 baseline publications
- 001_tokenizer.sh - perform tokenization step using NLTK tools
- 002_rarewords.sh - detect rare words
- 003_joint_probabilities.sh - estimate token co-occurrence probabilities
- 004_stopwords.sh - detect stopwords
- 005_reduced_joint_probabilities.sh - estimate token co-occurrence probabilities after
- 006_SSNMF.sh  - creates topic model in 1-2 hours
- 007_restricted_snowball.sh   - may take several hours time to download up to 20000 relevant publications
- 008_search_path_count.sh
- 009_extend_items.sh
- 010_extend_items_google_scholar.sh - the script downloads several hundreds publcations from Google Scholar, so you must use proxy to avoid the ban. The proxy address is *proxy* parameter in the configuration file
   `./data/YOUR_DATA_DIRECTORY/config.ini`
- 010_extend_items_google_scholar_resume.sh - sometimes you need to resume the previous command
- 011_download_pdfs.sh - downloads PDF files that are available for free
- 012_export_xlsx.sh - creates the final report according to `./docs/data-requirements.txt`


7) Optionally, you can extended pipeline with ATE step
- 013_ate_pdf2txt.sh
- 014_ate_clear_txt.sh
- 015_ate_generate_datasets.sh
- 015_ate_generate_partial_datasets.sh
- 016_ate_get_terms.sh
- 016_ate_get_terms_partial.sh
- 016_ate_merge_terms_partial.sh
- 017_ate_clear_terms.sh
- 018_ate_saturation.sh              



0) you need NLTK and numpy to run the scripts below.
1) get MS Academic API key ( https://azure.microsoft.com/en-us/services/cognitive-services/academic-knowledge/ )
2) copy config-sample.ini to config.ini and update config.ini
3) set desired MS Academic topics in the file data/in-include-topics.txt
4) set undesired MS Academic topics in the file data/in-exclude-topics.txt
5) paste MS Academic Ids into data/in-seed.csv , one ID per row
6) run sequentially the following files
* 000_download.py
* 001_tokenizer.py
* 002_rarewords.py
* 003_joint_probabilities.py
* 004_stopwords.py
* 005_reduced_joint_probabilities.py
* 007_SSNMF.py
* 008_show_topic_coherence.py
* 009_restricted_snowball.py
* 010_search_path_count.py
