![RAG Lex Overview](ss/RAGLEXpic.jpeg)




![Raglex Diagram](ss/Raglexdiagram.jpg)



✈️ AI-Powered Chatbot with Amazon Lex and Bedrock
For Cloud Nine Airlines: Query Travel Policies with AI.

In this project, we leverage Amazon Lex and Amazon Bedrock to create an AI-powered chatbot capable of answering questions about travel policies stored in Amazon S3. The chatbot uses Retrieval-Augmented Generation (RAG) to combine powerful pre-trained models with custom data. Let’s dive in! 🚀

Policies to Query:
Baggage Policy: Weight limits, dimensions, fees, and prohibited items.
Cancellation Policy: Refundable vs. non-refundable tickets, processing times.
Check-in & Boarding: Online check-in, boarding timelines, and requirements.
In-flight Services: Meals, Wi-Fi, entertainment, and special assistance.


Step 1: Setting Up an S3 Bucket for Policy Storage
Login to AWS Console → Search for S3.
Click Create Bucket, name it something unique like cloud-nine-travel-policies. Leave defaults and click Create bucket.

![S3 Bucket](ss/s3-bucket.png) 



Select the bucket → Click Upload → Add the 4 zipped PDF files form the repository entitled "Cloudninepolicies.zip"  (Baggage Policy, Cancellation Policy, etc.) Unzip and upload them.
🎉 These files are now stored and ready for querying! Let’s move to Bedrock to unlock their AI potential.


Step 2: Accessing Amazon Bedrock Models
Search for Amazon Bedrock in the console.
Under Foundation Models, click Base Models.


![Base Model](ss/base-model.png)  



Request access to:
Titan Embeddings G1 - Text (Amazon).
Claude (Anthropic).


![Titan and Claude](ss/titanclaude.png) 



![Claude Model Access](ss/claudemodelaccess.png) 



Approval may take a few minutes. Once granted, you’ll receive an email notification.
Why Bedrock?
S3 can store your data but lacks AI capabilities to summarize, query, or interact intelligently. Bedrock bridges that gap with powerful pretrained models and custom embeddings.


Step 3: Create a Knowledge Base in Amazon Bedrock
Navigate to Bedrock → Knowledge Bases → Create Knowledge Base.


![Knowledge Bases](ss/kbases.png) 



![Create Knowledge Base](ss/createkb.png)  



Configure:
Name: Leave default or customize.
IAM Role: Select Create and use a new service role.


![Knowledge Base Details](ss/kbdetails.png) 



Data Source: Select Amazon S3 → Browse and select your bucket (cloud-nine-travel-policies).



![Browse S3](ss/browses3.png) 




![Knowledge Base Select S3](ss/kbselects3.png) 



Model & Vector Database:
Embeddings Model: Choose Titan Embeddings G1 - Text v1.2.
Vector Database: Select Quick create a new vector store (creates an Amazon OpenSearch Serverless vector store).
Click Create Knowledge Base and wait for setup.


![Vector Database](ss/vectordb.png)



Sync Data: Go to Data Sources, select your Knowledge base, and click Sync.



![Go to Sources](ss/go2sources.png)  



![Sync Data Source](ss/syncdatasource.png)  



🎯 Your Knowledge Base is now live and linked to S3. Time to build the chatbot!


Step 4: Building the Amazon Lex Chatbot
Go to Amazon Lex → Create Bot → Traditional → Blank Bot.
Bot Configuration:
Name: CloudNinePolicyBot.


![Create Bot](ss/createbot.png)  


IAM Role: Create a role with basic Lex permissions.
Description: “An AI assistant for answering Cloud Nine Airlines travel policy questions.”

For "initial response" under "Message" input "Hi! How can I help you today?" 


Leave other settings default.
Step 4.1: Adding Intents

![Hi Test](ss/HI.png) 


1. Welcome Intent:

Name: WelcomeIntent.
Utterances: "Hi", "Hello", "Good morning", etc.
Response: “Hi! How can I help you today?”


![Utterances](ss/u.png)


For "initial response" under "Message" input "Hi! How can I help you today?" 



![Initial Response](ss/initalresponse.png)  



![Inspect Intent](ss/inspect.png)  




Then click the box underneath "Advanced options". Click the arrow under "Set Values" then under "Next step in conversation" select "Wait for users input". Click "Update options".



![Advanced Options](ss/advanceoptions.png)  



Save and build the bot.


![Build Intent](ss/buildintent.png)  



Try asking a question and testing


![Fallback Intent](ss/fallbackintent.png) 


2. Q&A Intent:

Click "Add intent", then "Use built-in intent".


![Add Intent](ss/addintent.png)  



Under "Built-in intent select: AMAZON.QnAIntent (GenAI feature).


![QnA Intent](ss/qnaintent.png)    



Model: Select Anthropic → Claude V2.
Knowledge Base ID: Retrieve from Amazon Bedrock and link it here.
Save and build the bot.

![Knowledge Base ID](ss/kbID.png)  



![Knowledge Base ID and Model](ss/kbIDandmodel.png)  



Step 4.2: Testing the Chatbot
Open the Test Console in Lex.
Within this repository, you will see the cnchatbotqs.pdf. These are questions you can ask the chatbot related to our Cloud Nine airlines travel policies!
Try:
“Hi” → Should trigger the Welcome Intent.
“Can I cancel a refundable ticket on the same day of purchase?” → Queries Bedrock and returns relevant policy details.


![Test Chatbot](ss/testchatbot.png)  



Try unrelated questions to see fallback behavior.


![Fallback Last Pic](ss/fallbacklastpic.png)  




Cleanup & Cost Management
Delete resources to avoid incurring charges:
S3 Bucket, Knowledge Base, Lex Bot.
Go to OpenSearch Serverless → Collections and delete any active collections.

![Delete OpenSearch](ss/deleteopensearch.png) 
