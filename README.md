# Product Reputation Profiler (PRP)
The purpose of this tool is to perform an in-depth analysis of the reputation profile of a certain product on social networks using Large Language Model and Prompt Engineering.

## Description
Social networks contain valuable information about user experiences of using a particular product - such as problems, malfunctions, sentiments, general issues and any other type of criticism. This information is important for businesses that want to understand what internet users or customers on social networks thinks about their current product on the market, so that they can improve it.

The first step is to extract data from a social network that contain posts or comments mentioning a keyword of a certain product - this can be done through requests from official API services the social networks provide (Twitter, Facebook or Reddit for example). this data is then "fed" into the algorithm as input. it includes the content of the posts or comments, dates, usernames, number of views, number of shares, etc.

Our tool is using a Large Language Model that extracts unique KPI indicators from the data in order to provide relevant and important insights for a product name. Besides those KPI indicators, it also extracts main criticisms toward the product. by utilizing the Large Language Model, it collects all the criticisms and lists the most frequently mentioned problems or issues the users or customers mention.


At this point, the algorithm only supports the social network Twitter (X).

Here are the algorithm steps:    
1. Extracting data from one of the social networks using the official API service (posts, comments, tweets, usernames, dates, views, likes, shares, etc.).
2. Utilizing AI/LLM with Prompt Engineering for extracting criticisms about the product from posts or comments.
3. Utilizing AI/LLM with Prompt Engineering for extracting sentiments and emotions of user's posts or comments mentioning their experience with the product.
4. Clustering the criticsms into N-number of the most frequent topics (issues, problems, etc.).
5. Assembling a report with the list of the main problems, issues, or criticisms and providing unique KPIs metrics.

### Available KPI list (Twitter/X):
-1 Volume:   
  represents the total amount of activity on the social network (views + quotes + replies + retweets + bookmarks + favorites)
-2 Engagement:   
  represents the total amount of user engagement (quotes + replies + retweets)
-3 Influence:   
  Represents the level of influence through the amount of the tweets that mention the product together with the number of the users number of followers (Average Followers Count × Tweet Count)   
-4 Positive Sentiment
-5 Negative Sentiment
-6 Anticipation
-7 Curiosity
-8 Surprise


Note that we use the GPT model through which we send API requests, but it is also possible to use different local LLM models such as Llama, Mistral, etc. - but we have not yet tried this and have not tested their outputs.   
   
To run, use Main.py - please enter the API key if needed, and the number of the desired clusters.    


