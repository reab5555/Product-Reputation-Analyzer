
<img src="example_images/icon.webp" width="100" alt="alt text">

# Product Reputation Analyzer (PRA)
The purpose of this tool is to perform an in-depth analysis of a product throught social networks opinions, sentiments and atitudes towards a the product, using Large Language Model and Prompt Engineering.

## Description
Social networks contain valuable information about user experiences of using a particular product - such as problems, malfunctions, sentiments, general issues and any other type of criticism. This information is important for businesses that want to understand what internet users or customers on social networks thinks about their current product on the market, so that they can improve it. relevant to business and data analysts, particularly those focused on product management, marketing strategy, and customer relations. The use of KPIs derived from social media analytics is increasingly crucial in understanding and predicting consumer behavior and market trends.

The first step is to extract data from a social network that contain posts or comments mentioning a keyword of a certain product - this can be done through requests from official API services the social networks provide (Twitter, Facebook or Reddit for example). this data is then "fed" into the algorithm as input. it includes the content of the posts or comments, dates, usernames, number of views, number of shares, etc.

Our algorithm is using a Large Language Model (Gemini Pro) that extracts unique KPI measurements from the data in order to provide relevant and important insights for a given product. it also extracts the main criticisms toward the product. by utilizing the Large Language Model, it collects all the criticisms, assemble them, making generalizations, and lists the most frequently mentioned problems or issues the users or customers relation to the product.   

Sentiments and Emotions are extracted using two finetuned variations of BERT language model, which were evaluated with high accuracy of over 95% on the GoEmotions and SST-2 datasets.

At this point, the algorithm only supports the social network Twitter (X).

Here are the algorithm steps:    
1. Extracting data from one of the social networks using the official API service (posts, comments, tweets, usernames, dates, views, likes, shares, etc.).
2. Utilizing AI/LLM with Prompt Engineering for extracting criticisms about the product from posts or comments.
3. Utilizing AI/LLM with Prompt Engineering for extracting sentiments and emotions of user's posts or comments mentioning their experience with the product.
4. Clustering the criticsms into N-number of the most frequent topics (issues, problems, etc.).
5. Assembling a report with the list of the main problems, issues, or criticisms and providing unique KPI metrics.

## Algorithm steps
Loading fetched Dataset -> Cleaning texts -> Extracting all Criticisms and Emotions -> Summarizing the criticisms into main topics and analyzing KPIs

<img src="example_images/Product Analysis.png" width="500" alt="alt text">

## Available KPI list (Twitter/X):
#### Activity:
- Volume:   
  represents the total amount of activity on the social network (views + quotes + replies + retweets + bookmarks + favorites).   
  more mentions can lead to increased brand visibility and consequently, more sales opportunities.      
- Engagement:   
  represents the total amount of user engagement (quotes + replies + retweets).
  higher engagement can foster product spreading and popularity, so more engagment mean more product noticeability.     
- Influence:   
  Represents the level of influence through the amount of the tweets that mention the product together with the number of the users number of followers (Average Followers Count × Tweet Count).
   being influential can help the product becoming a preferred brand, which can boost profit margins. 
#### Sentiments:
- Positive Sentiment:   
  How much the tweets are reflecting a positive attitude toward the product (a probability number 0-1).
  positive sentiment can be amplified to attract new customers and retain existing ones, improving sales. this also can suggest the current magnitude of positivity of the product.   
- Negative Sentiment:   
  How much the tweets are reflecting a negative attitude toward the product (a probability number 0-1).
  Addressing negative feedback promptly can prevent loss of customers and damage to brand reputation.    
#### Emotions:
- Anticipation:   
  How much the tweets represent anticipation toward the product or other features related to this product (a scrore number from 0 to 100).   
  Capitalizing on customer anticipation can drive pre-orders and create buzz, potentially leading to higher initial sales.   
- Curiosity:   
  How much the tweets represent curiosity (a scrore number from 0 to 100).   
  Engaging curious customers can lead to increased information dissemination and higher conversion rates.   
- Surprise:   
  How much the tweets represent reactions of surprise (a scrore number from 0 to 100).   
  Positive surprises can enhance customer experience, leading to free word-of-mouth marketing and potentially more sales.   

<img src="example_images/Product Analysis 2.png" width="500" alt="alt text">

### Notes
In order to get a sentiment probability or an emotion score for each text we need a large language model that will also understand the context and the sentiment that is directed solely towards the product keyword, as this avoid any general impression the text express that is not related to the product itself. Only Large Language Models able to attribute a sentiment to a specific keyword in the text by the right prompt.   
   
Note that we use the Gemini Pro 1.5 model by Google through which we send API requests. however, it is also possible to use different local LLM models such as Llama, Mistral, etc. but we have not yet tried this and have not tested their outputs. also keep in mind that it must use a model with a capability of receiving a maximum tokens number of at least 100,000 in order to receive all the texts at once for summarizing them.  
   
To run, use Main.py - please enter the name of your google cloud project if needed and the number of the desired topics or criticisms to be listed.    

## Demonstration
We would like to demonstrate here some of the results we received from the algorithm. we extracted two datasets containing tweets that mention iPhone 15 Pro Max and the Tesla Model 3. Both are very popular products in the market. We extracted data from different time ranges. The data for the Tesla Model 3 is tweets from 2023, with each month containing the same amount of tweets or samples. For the iPhone 15 Pro Max, we extracted tweets from the period between September 2023 (the product's release date) and December 2023. In total, the two datasets contain about 4000 tweets each.   


