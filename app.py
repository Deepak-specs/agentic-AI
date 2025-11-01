
import streamlit as st
import pandas as pd
import json
import boto3
import psycopg2
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from PyPDF2 import PdfReader
from utils.auth import check_password
from nlp.preprocess import preprocess_text
from opensearch.mapping import create_index
from opensearchpy import OpenSearch

# --- Authentication ---
if not check_password():
    st.stop()

# --- Inference Parameters ---
INFERENCE_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.9,
    "max_tokens": 1024
}

# --- Load LangChain LLM ---
llm = ChatOpenAI(temperature=INFERENCE_CONFIG["temperature"])

# --- Helper Functions ---
def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file, engine="openpyxl")
    elif file.name.endswith('.json'):
        return pd.read_json(file)
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.name.endswith('.pdf'):
        reader = PdfReader(file)
        return "
".join([page.extract_text() for page in reader.pages])
    else:
        return "Unsupported file format"

def fetch_dynamodb_data(table_name):
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)
    response = table.scan()
    return response['Items']

def fetch_redshift_data(query, conn_params):
    conn = psycopg2.connect(**conn_params)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
        return data
    except Exception as e:
        return f"Error fetching API data: {str(e)}"

def analyze_prompt(prompt, data_text):
    full_input = f"User prompt: {prompt}

Data:
{data_text}

Respond in three sections:
1. Summary/Conclusion
2. Insights based on data
3. Recommendations"
    response = llm([HumanMessage(content=full_input)])
    return response.content

# --- Bedrock Agent Invocation ---
def analyze_with_bedrock_agent(prompt):
    agent = boto3.client("bedrock-agent-runtime")
    response = agent.invoke_agent(
        agentId="your-agent-id",
        agentAliasId="your-alias-id",
        sessionId="session-001",
        inputText=prompt
    )
    return response["completion"]

# --- Bedrock Knowledge Base Invocation ---
def analyze_with_knowledge_base(prompt):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(
        modelId="anthropic.claude-v2",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "prompt": prompt,
            "knowledgeBaseId": "your-knowledge-base-id",
            "max_tokens": 1024
        })
    )
    result = json.loads(response["body"].read())
    return result.get("completion", "No response")

# --- Streamlit UI ---
st.title("Agentic AI for Multi-Source Data Analysis")

uploaded_file = st.file_uploader("Upload a data file", type=["csv", "xlsx", "json", "txt", "pdf"])
prompt = st.text_area("Enter your prompt")

if st.button("Analyze File"):
    if uploaded_file and prompt:
        data_content = read_file(uploaded_file)
        if isinstance(data_content, pd.DataFrame):
            data_text = data_content.to_csv(index=False)
        else:
            data_text = str(data_content)

        clean_text = preprocess_text(data_text)
        result = analyze_prompt(prompt, clean_text)
        st.markdown("### 📄 Response")
        st.markdown(result)

        agent_result = analyze_with_bedrock_agent(prompt)
        st.markdown("### 🤖 Bedrock Agent Response")
        st.markdown(agent_result)

        kb_result = analyze_with_knowledge_base(prompt)
        st.markdown("### 🧠 Knowledge Base Response")
        st.markdown(kb_result)
    else:
        st.warning("Please upload a file and enter a prompt.")

# --- API Data Source ---
with st.expander("🌐 API Data Source"):
    api_url = st.text_input("Enter API Endpoint URL")
    if st.button("Fetch API Data"):
        api_data = fetch_api_data(api_url)
        st.markdown("### 📡 API Response")
        st.write(api_data)

        if prompt:
            api_text = str(api_data)
            clean_api_text = preprocess_text(api_text)
            result = analyze_prompt(prompt, clean_api_text)
            st.markdown("### 🤖 Prompt Response from API Data")
            st.markdown(result)
        else:
            st.warning("Please enter a prompt to analyze the API data.")

# --- OpenSearch Setup ---
with st.expander("🔍 OpenSearch Setup"):
    index_name = st.text_input("Index name")
    if st.button("Create Index"):
        client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}], http_auth=("admin", "admin"), use_ssl=False)
        result = create_index(client, index_name)
        st.write(result)
