# Product Reputation Profiler (PRP)
The purpose of this tool is to perform an in-depth analysis of the reputation profile of a certain product on social networks.

## Description
The tool analyzes and extracts a number of key indicators (KPIs) that measure the activity in social networks related to a product.    
Social networks contain critical information of user experiences of a particular product, such as problems, malfunctions, sentiments, general issues and any other type of criticism. This information is important for businesses that want to understand what internet users of it thinks about their product, and want to improve the existing product that is on the market.    
    
First, data is extracted from a social network that contain posts mentioning a keyword of a certain product - this can be done through requests from official API request from the social network (Twitter, Facebook or Reddit for example). The data is then fed to the algorithm as input - it includes the content of the posts or comments, dates, usernames, number of views, number of shares, etc. After that, the algorithm extracts unique KPI indicators from the data in order to provide relevant and important insights for that product.    
    
Besides those KPI indicators, it also extracts from the posts or comments the product criticisms they contain. By using the K-means clustering method, it collects all the criticisms and lists the most frequently mentioned problems or issues about the product.

Here are the algorithm steps:
1. Extracting data from one of the social networks from APIs (posts, comments, tweets, usernames, dates, views, likes, shares, etc.)
