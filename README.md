# automate-jobmatching
Automate jobmatching process both for job seekers and hirers

# The reason to work on this project
Even though there're already job matching services that recommends me or let me search jobs exist, still I spend much time selecting the jobs from the jobs listing, and I realized that this process is essentially natural language processing. 

Since I'm currently very interested in knowledge graph, I believe this project would help my understanding that is neccesary for my next project:slightly_smiling_face:

# Blueprint:triangular_ruler:
## 1.1. Scrape Job Description
Scrape job descriptions from job seeking web site based on filtering set by user. I'm going to scrape from [Green](https://www.green-japan.com/).
> **Note**
> I'm going to skip this functionality since preprocessing and cosine similarity computation is main functionalities,
> and I already have some job description to apply the algorithm that I'm going to develop. 

## 1.2. Preprocess Job Descriptions and Company Seek Data into word embeddings
Preprocess the job descriptions and user's profile, and convert them into word embeddings using [GloVe](https://nlp.stanford.edu/projects/glove/), which performs better than Word2Vec for word analogy tasks. It also outperforms related models on similarity tasks and named entity recognition.

## 1.3. Compute Cosine Similarity
For each job description and each company, compute the [cosine similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) between the word embeddings of the job description and the company seek data. This will give you a similarity score for each combination.

## 1.4. Rank the Scores
Rank the similarity scores in descending order to find the best matches between job descriptions and companies. The higher the score, the better the match.

## 1.5. Set a Threshold
Depending on your preferences, you can set a threshold for the similarity score above which you consider the match to be significant.

# Goal for each functionality
|functionality|goal|
|:---|:---|
|1.1. Scrape Job Description|7/30|
|1.2. Preprocess Job Descriptions and Company Seek Data into work embeddings|8/1|
|1.3. Compute Cosine Similarity|8/1|
|1.4. Rank the Scores|8/4|
|1.5. Set a Threshold|8/4|
