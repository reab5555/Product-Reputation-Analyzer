# Product Reputation Profiler (PRP)
The purpose of this tool is to perform an in-depth analysis of the reputation profile of a certain product on social networks using AI or Large Language Model.

## Description
Social networks contain critical information about user experiences of using a particular product - such as problems, malfunctions, sentiments, general issues and any other type of criticism. This information is important for businesses that want to understand what internet users or customers on social networks thinks about their current product on the market, so that they can improve it.
    
First, data is extracted from a social network that contain posts mentioning a keyword of a certain product - this can be done through requests from official API request from the social network (Twitter, Facebook or Reddit for example). The data is then fed to the algorithm as input - it includes the content of the posts or comments, dates, usernames, number of views, number of shares, etc. Using a Large Language Model, it extracts unique KPI indicators from the data in order to provide relevant and important insights for that product. 

Besides those KPI indicators, it also extracts from the posts or comments the product criticisms they contain. By using the K-means clustering method, it collects all the criticisms and lists the most frequently mentioned problems or issues about the product.

At this point, the algorithm only supports Twitter (X) and Reddit.

Here are the algorithm steps:    
1. Extracting data from one of the social networks using the official API requests (posts, comments, tweets, usernames, dates, views, likes, shares, etc.).
2. Utilizing AI/LLM for extracting criticisms about the product from posts or comments.
3. Utilizing AI/LLM for extracting sentiments and emotions of user's posts or comments mentioning their experience with the product.
4. Clustering the criticsms into N-number of the most frequent topics (issues, problems, etc.).
5. Exporting a report and unique KPIs based on the data we extracted.

* Note that we use the GPT model through which we send API requests, but it is also possible to use different local LLM models such as Llama, Mistral, etc. - but we have not yet tried this and have not tested their outputs.   
* To run, use Main.py - please enter the API key if needed, and the number of the desired clusters.   

### KPIs
Twitter:   
- Volume: represents the total amount of activity on the social network (views + quotes + replies + retweets + bookmarks + favorites)
- Engagement: represents the total amount of user engagement (quotes + replies + retweets)
- Influence: Represents the level of influence through the amount of the tweets that mention the product together with the number of the users number of followers (Average Followers Count × Tweet Count)
- Positive Sentiment
- Negative Sentiment
- Anticipation
- Curiosity
- Surprise
    
Reditt:
- Engagement: represents the total amount of user engagement (comments + likes + replies)
- Positive Sentiment
- Negative Sentiment
- Anticipation
- Curiosity
- Surprise

