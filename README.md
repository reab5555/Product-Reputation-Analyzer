
<img src="examples/icon.png" width="100" alt="alt text">

# Product Reputation Analyzer (PRA)
The purpose of this tool is to perform an in-depth analysis of a product throught social networks opinions, sentiments and atitudes towards a the product, using Large Language Model and Prompt Engineering.

## Description
Social networks contain valuable information about user experiences of using a particular product - such as problems, malfunctions, sentiments, general issues and any other type of criticism. This information is important for businesses that want to understand what internet users or customers on social networks thinks about their current product on the market, so that they can improve it. relevant to business and data analysts, particularly those focused on product management, marketing strategy, and customer relations. The use of KPIs derived from social media analytics is increasingly crucial in understanding and predicting consumer behavior and market trends.

The first step is to extract data from a social network that contain posts or comments mentioning a keyword of a certain product - this can be done through requests from official API services the social networks provide (Twitter, Facebook or Reddit for example). this data is then "fed" into the algorithm as input. it includes the content of the posts or comments, dates, usernames, number of views, number of shares, etc.

Our tool is using a Large Language Model (Gemini Pro) that extracts unique KPI measurements from the data in order to provide relevant and important insights for a given product. it also extracts the main criticisms toward the product. by utilizing the Large Language Model, it collects all the criticisms, assemble them, making generalizations, and lists the most frequently mentioned problems or issues the users or customers relation to the product.   

At this point, the algorithm only supports the social network Twitter (X).

Here are the algorithm steps:    
1. Extracting data from one of the social networks using the official API service (posts, comments, tweets, usernames, dates, views, likes, shares, etc.).
2. Utilizing AI/LLM with Prompt Engineering for extracting criticisms about the product from posts or comments.
3. Utilizing AI/LLM with Prompt Engineering for extracting sentiments and emotions of user's posts or comments mentioning their experience with the product.
4. Clustering the criticsms into N-number of the most frequent topics (issues, problems, etc.).
5. Assembling a report with the list of the main problems, issues, or criticisms and providing unique KPI metrics.

## Algorithm steps
Loading fetched Dataset -> Cleaning texts -> Extracting all Criticisms and Sentiments -> Summarizing the criticisms into main topics and analyzing KPIs

<img src="examples/Product Analysis.png" width="500" alt="alt text">

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

<img src="examples/Product Analysis 2.png" width="500" alt="alt text">

### Notes
In order to get a sentiment probability or an emotion score for each text we need a large language model that will also understand the context and the sentiment that is directed solely towards the product keyword, as this avoid any general impression the text express that is not related to the product itself. Only Large Language Models able to attribute a sentiment to a specific keyword in the text by the right prompt.   
   
Note that we use the Gemini Pro 1.5 model by Google through which we send API requests. however, it is also possible to use different local LLM models such as Llama, Mistral, etc. but we have not yet tried this and have not tested their outputs. also keep in mind that it must use a model with a capability of receiving a maximum tokens number of at least 100,000 in order to receive all the texts at once for summarizing them.  
   
To run, use Main.py - please enter the name of your google cloud project if needed and the number of the desired topics or criticisms to be listed.    

## Demonstration
We would like to demonstrate here some of the results we received from the algorithm. we extracted two datasets containing tweets that mention iPhone 15 Pro Max and the Tesla Model 3. Both are very popular products in the market. We extracted data from different time ranges. The data for the Tesla Model 3 is tweets from 2023, with each month containing the same amount of tweets or samples. For the iPhone 15 Pro Max, we extracted tweets from the period between September 2023 (the product's release date) and December 2023. In total, the two datasets contain about 4000 tweets each.   

### Activity
<img src="examples/Tesla Model 3 - 3.png" width="600" alt="alt text">
<img src="examples/iPhone 15 Pro Max - 1.png" width="600" alt="alt text">
   
Tesla Model 3:   
1. Volume (blue line): The Volume here starts at a lower point of 6,436,448 in month 1, with fluctuations throughout the year, peaking dramatically at 35,495,188 in month 9 (September) before falling to 943,749 by month 12.   
2. Engagement (pink line): Beginning at 6,134, this metric shows variability, with a notable spike to 34,544 in month 9 (September), which correlates with the peak in Volume, followed by a decline to 1,316 by the end of the year.   
3. Influence (yellow line): The Influence starts at 411,549,219 and, like the other metrics, shows fluctuations, with the most significant peak of 1,652,272,286 in month 9 (September). By month 12, it decreases to 114,961,748.   
    
Overall, the data indicates more volatility in the Twitter KPI metrics throughout the year, with a significant peak in all metrics in month 9 (September), which could be associated with a major event or release, followed by a decline.   
     
iPhone 15 Pro Max:    
1. Volume (blue line): Starts at a very high value of 125,443,385 in month 9 (September), indicating a substantial number of tweets. It shows a consistent downward trend over the months, ending at 10,831,111 by month 12 (December).   
2. Engagement (pink line): This line starts at 140,756 and also shows a decline, although not as steep as the Volume. By month 12 (December), the Engagement drops to 26,133.   
3. Influence (yellow line): Beginning with an extremely high value of 4,577,758,611, this metric decreases over time, reaching 404,985,950 by month 12 (December).   
  
The overall trend for the iPhone 15 Pro Max shows a decline across all tracked metrics over these months, suggesting a peak in interest or marketing efforts around month 9 (September) at its initial release month, with a gradual decline thereafter.   
   
### Sentiments
<img src="examples/Tesla Model 3 - 2.png" width="600" alt="alt text">
<img src="examples/iPhone 15 Pro Max - 2.png" width="600" alt="alt text">
   
Tesla Model 3:   
1. Average Negative Sentiment (red line): The average negative sentiment starts at 0.1468, lowers to 0.1298 around month 5, drops significantly to 0.0743 in month 9 (September), and finishes the year at 0.0574. The trend here shows a decrease in negative sentiment over the year, with a sharp drop in month 9 (September).   
2. Average Positive Sentiment (green line): This measure begins at 0.5571, dips to 0.5189 around month 5, peaks at 0.7638 in month 9, and closes the year at 0.5926. The pattern indicates that positive sentiment peaked around month 9 (September), possibly correlating with a significant event or announcement related to the Tesla Model 3.   
   
iPhone 15 Pro Max:    
1. Average Negative Sentiment (red line): This measure starts at 0.41023, shows a slight dip in the middle months, and then rises to its highest point at 0.50772 by month 12 (December).
2. It suggests that negative sentiment around the iPhone 15 Pro Max on Twitter increased over the period.   
3. Average Positive Sentiment (green line): The positive sentiment starts lower at 0.17021, dips to 0.14010 in the middle months, and ends slightly higher at 0.15621 by month 12 (December). This line is relatively flat, indicating that negative sentiment didn't fluctuate much throughout the period.   
   
In summary, the iPhone 15 Pro Max's Twitter sentiment analysis shows an increase in negative sentiment and a slight increase in positive sentiment towards the end of the year. For the Tesla Model 3, there is a marked increase in positive sentiment and a decrease in negative sentiment throughout the year, with a notable change around month 9 (September).   

### Emotions
<img src="examples/Tesla Model 3 - 3.png" width="600" alt="alt text">
<img src="examples/iPhone 15 Pro Max - 3.png" width="600" alt="alt text">
   
Tesla Model 3:   
1. Anticipation (purple line): Starting at 44.38, this measure shows some fluctuation but is generally trending upward, reaching a peak of 67.70 by the end of the year, indicating increasing anticipation for the Tesla Model 3.   
2. Curiosity (light blue line): Curiosity begins at 24.27, dips to 17.02, and then shows an overall upward trend to 29.43 by month 12 (December). This demonstrates a resurgence of curiosity towards the end of the year.   
3. Surprise (orange line): This line starts at 8.265, fluctuates over the months, peaking at 14.893 in month 10 (October), and ends at a lower value of 8.574. The surprise sentiment appears to be variable with a significant peak towards the latter part of the year.   
   
iPhone 15 Pro Max:   
1. Anticipation (purple line): It starts at a high value of 25.453, dips to 16.122 around month 10, and then rises back up to 25.743 by month 12 (December). This pattern may suggest fluctuating expectations or interest regarding the iPhone 15 Pro Max, with a revival of anticipation towards the end of the year.   
2. Curiosity (light blue line): This sentiment begins at a lower value of 8.91 and shows a gradual increase, ending at 19.06 by month 12 (December). This indicates growing curiosity or interest in the product over these months.   
3. Influence (orange line): Beginning with a very high value of 4,577,758,611, there is a steady decline to 404,985,950 by month 12 (December), similar to the previous influence graph for the iPhone 15 Pro Max.   
   
Overall, the sentiment dynamics for both products show that anticipation and curiosity tend to increase towards the end of the year, which could correlate with product release cycles, marketing campaigns, or seasonal events. The Influence metric for the iPhone and the Surprise metric for the Tesla indicate there were periods of heightened reaction, possibly due to specific events or announcements.   
   

### Coin Master: an example from Reddit
Apart from Twitter (X), we also analyzed posts and comments from Reddit related to Coin Master mobile game. We have collected posts and comments that mention the name of the game from January until April 2024. In addition to this, we linked or joined the revenue values of the game with the social network data by the corresponding months.    
   
<img src="examples/Coin_Master_January_-_April_2024.jpg" width="600" alt="alt text">

This dashboard presents a multi-faceted analysis of the Coin Master mobile game based on data aggregated from Reddit over the period January to April 2024. It covers metrics or unique KPIs such as revenue, engagement, sentiments and emotions.   
   
The top portion of the dashboard provides an overview of the mean revenue, which shows a rising trend from January (68.2 million USD) to April (71.2 million USD), apart from a dip in February to 60 million USD.   
   
Engagement, defined as the sum of comments, likes, and replies, experienced a significant drop from January (980) to February (106), followed by a recovery in March (706).   
   
The middle section charts emotions: Anticipation's mean value begins at 10 in January, peaking at 20 in April. Curiosity begin with a mean value of 4 in January, declining to 3 in February, and increasing to 20 by April.   
   
Sentiment analysis depicted at the top right corner indicates that positive sentiment mean values slightly increased from 0.38 in January to 0.50 in April, while negative sentiment remained relatively stable, starting at 0.23 in January and slightly decreasing to 0.13 in April.   

Overall, this analysis suggests that while Coin Master's revenue has generally increased over the observed period, it experienced fluctuations in engagement, anticipation, and curiosity, with an overall increase in positive sentiment on Reddit. 



