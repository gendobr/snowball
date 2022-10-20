# snowball
Set of python scripts to implement the controlled snowball sampling to gather collection of the seminal scientific publications on desired subject. Details of the approach are available in the
[publications](https://scholar.google.com/citations?user=bNlVvTEAAAAJ&hl=ru&oi=sra) and [publications](https://scholar.google.com/citations?hl=ru&user=vaOHuLQAAAAJ&view_op=list_works&sortby=pubdate) 

Requirements:
To run the package you need 
* python3 
* [python-poetry](https://python-poetry.org/)
* optionally: anonymous proxy to query Google Scholar

## Anonymous proxy
You can use one of proxy services listed at 
[https://www.didsoft.com ](https://www.didsoft.com)

## Quick start:
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
   $ cp -R ./docs/data ./data/YOUR_DATA_DIRECTORY
   ```

3) install all required python packages with 
   ```
   $ poetry install
   ```
   
4) download the required NLTK packages
   ```
   $ poetry run python scripts/init.py
   ```

5) Find 10 - 20 seed publications in the
   [openalex.org](https://explore.openalex.org/).

   Each seed publication should be
   * be relevant to your search topic
   * have high citation index (however not extremely high)
   * be 7-10 years old
   Reasoning of the above conditions is discussed in *Lecy, J. D., & Beatty, K. E. (2012). Representative literature reviews using constrained snowball sampling and citation network analysis. Available at SSRN 1992601.*

   Paste the publication ids in the `./data/YOUR_DATA_DIRECTORY/in-seed.csv` file.
   One id per row

   The publication id is the long number in publication URL.
   For instance, in the URL https://academic.microsoft.com/paper/2899429816/citedby/ 
   publication id is 2899429816

6) run one-after-one the following files (don't forget to change the `../data/GAN/` to `../data/YOUR_DATA_DIRECTORY/` )
inside each file

- `000_download.sh`  - may take several hours time to download up to 20000 baseline publications
- `001_tokenizer.sh` - performs tokenization step using NLTK tools
- `002_rarewords.sh` - detects rare words
- `003_joint_probabilities.sh` - estimates token co-occurrence probabilities
- `004_stopwords.sh` - detects stopwords
- `005_reduced_joint_probabilities.sh` - estimates token co-occurrence probabilities after the rare words and stopwords excluded
- `006_SSNMF.sh`  - creates topic model in 1-2 hours
- `007_restricted_snowball.sh`   - may take several hours time to download up to 20000 relevant publications
- `008_search_path_count.sh` - does search path count calculation (see. [Main path analysis](https://en.wikipedia.org/wiki/Main_path_analysis) for explanation)
- `009_extend_items_google_scholar.sh` - the script downloads several hundreds publications from Google Scholar, so you must use proxy to avoid the ban. The proxy address is *proxy* parameter in the configuration file.
   `./data/YOUR_DATA_DIRECTORY/config.ini`
- `009_extend_items_google_scholar_resume.sh` - sometimes you need to resume the previous command
- `010_download_pdfs.sh` - downloads PDF files that are available for free
- `011_export_xlsx.sh` - creates the final report according to `./docs/data-requirements.txt`

Final list of publications is the file `011_exported.xlsx` that is `--outfile` parameter
in the `011_export_xlsx.sh` script.


7) Optionally, you can extended pipeline with ATE step
- `012_ate_pdf2txt.sh` - extract plain text from PDF files
- `013_ate_clear_txt.sh` - clear extracted texts
- `014_ate_generate_datasets.sh` - join extracted texts in the sequence of datasets
- `015_ate_get_terms.sh` - extract terms
- `016_ate_clear_terms.sh` - remove trash terms (list of trash terms is the file `./data/YOUR_DATA_DIRECTORY/ate_stopwords.csv`)
- `017_ate_saturation.sh` - does terminological saturation analysis
