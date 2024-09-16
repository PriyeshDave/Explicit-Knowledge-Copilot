# Explicit Knowledge Copilot - Your Conversational Bridge to Data Insights

Explicit Knowledge Copilot empowers business users to interact with data platforms using natural language, unlocking valuable insights without technical expertise. By enabling tabular data interpretation and visual inferences, Explicit Knowledge Copilot bridges the gap between raw data and actionable knowledge, driving faster decision-making and increased data literacy across your organization.

![Untitled design-2](https://github.com/arunnaray/llm-poc-hub/assets/81012989/2d70f5ca-9cdc-458f-bbb6-9aea3c17e372)

## 1. Home Page:
This web application is built using python, streamlit, python enabled html, Nivo Chart and mui.

<img width="1464" alt="Screenshot 2024-01-21 at 1 20 21 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/a5443d54-ccde-4461-a81c-8fa9adcac62a">


## 2. Data Explanation: 

### 2.1 Data Schema:
<img width="958" alt="Screenshot 2024-01-21 at 1 40 02 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/2d3cc791-28ad-4377-905f-d03153808174">



### 2.2 See Your Raw Data:
<img width="950" alt="Screenshot 2024-01-21 at 1 40 20 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/62ffd002-3c1f-4555-923d-e6b61d29a394">



## 3. Sample Questions Based On Your Data: 
<img width="1464" alt="Screenshot 2024-01-21 at 1 23 38 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/0b1d7fff-e390-41f4-8648-2ea0a9d7461e">

<img width="1464" alt="Screenshot 2024-01-21 at 1 23 58 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/de331af8-75c3-4f51-a6d8-86bab9c40d7e">

<img width="1464" alt="Screenshot 2024-01-21 at 1 24 12 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/a9506c63-5e81-4c68-80d2-38c94e211192">


<img width="1463" alt="Screenshot 2024-01-21 at 1 25 38 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/64d72952-83e6-40a6-bf69-ad50aa0d878e">


<img width="1464" alt="Screenshot 2024-01-21 at 1 26 04 PM" src="https://github.com/arunnaray/llm-poc-hub/assets/81012989/9332d9a6-c89b-43d5-bb8e-16aac0f97a93">



## Explicit Knowledge Copilot Features:
* Natural Language Querying: Ask questions about your data in plain English, like "What are the top performing regions in terms of sales?"
* Tabular Data Interpretation: Get summaries, statistics, and comparisons of your data tables for deeper understanding.
* Visual Inference Generation: Automatically generate relevant charts and graphs based on your queries, enhancing data visualization.
* Interactive Exploration: Drill down into specific data points, filter results, and compare different dimensions with ease.
* Customizable Dashboards: Create personalized dashboards to monitor key metrics and track progress over time.
  
**Current supported chart types:**

-Bar Chart

-Line Plot

-Scatter Plot

-Swarm Plot

-Pie Chart

## How to use the Repository
To start using the repository, first clone the project into your local pc

```
git clone https://github.com/arunnaray/llm-poc-hub.git
```

Next, open the file location in any Python IDE, I highly recommend PyCharm. 
Then, navigate to the folder > .streamlit (as shown in the picture below), create a file called secrets.toml

![add_secrets_toml.png](assets%2Fimages%2Fadd_secrets_toml.png)

Within secrets.toml file add your OpenAI API key into the file (as shown below). This will allow streamlit to pick up the secrets.

```
gpt_secret = "<YOUR-API-KEY>"
```

Once done, install the requirements for the project.

```
pip install -r requirements.txt
```

To run the application. Within the terminal of the IDE do:

```
streamlit run Home.py
```

Access the site using: http://localhost:8501

## Contribution
Please feel free to contribute to the repository.

Fork the application, make edits and perform a pull request. 
