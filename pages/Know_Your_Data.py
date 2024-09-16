import streamlit as st
import pandas as pd
import re
import gpt3 as open_ai_gpt3
import os
from PyPDF2 import PdfReader
import streamlit.components.v1 as components

import pickle
import networkx as nx
from pyvis.network import Network
import base64


GPT_SECRETS = st.secrets["gpt_secret"]
open_ai_gpt3.openai.api_key = GPT_SECRETS
COLLEAGUE_DATA_PATH = '/Users/apple/Documents/Priyesh/Repositories/Explicit-Knowledge-Copilot/Datasets/Leadership Visit Demo/colleague_data.csv'
ASSET_DATA_PATH = '/Users/apple/Documents/Priyesh/Repositories/Explicit-Knowledge-Copilot/Datasets/Leadership Visit Demo/asset_data.csv'
PDF_DIR_PATH = "/Users/apple/Documents/Priyesh/Repositories/Explicit-Knowledge-Chat/data-bank/"

EXP_KNW_URL = 'http://localhost:8501'
CHAT_DOC_URL = 'http://localhost:8502'
KG_PATH = '/Users/apple/Documents/Priyesh/Repositories/Explicit-Knowledge-Copilot/DAG/entire_dag.pkl'
DAG_HTML_PATH = '/Users/apple/Documents/Priyesh/Repositories/Explicit-Knowledge-Copilot/DAG/emp_asset_dag.html' 
VIDEO_FILE_PATH = '/Users/apple/Documents/Priyesh/Repositories/Explicit-Knowledge-Copilot/assets/kyd_banner.mp4'



st.set_page_config(page_icon="assets/images/favicon.png")

st.markdown(f"""
    <style>
    .top-right {{
        position: absolute;
        top: 10px;
        right: 10px;
        display: flex;
        gap: 10px;
    }}
    .button-container button {{
        margin-right: 10px;
    }}
    </style>
    <div class="top-right">
        <div class="button-container">
            <a href="{EXP_KNW_URL}" target="_blank">
                <button class="button"> Explicit Knowledge Copilot </button>
            </a>
            <a href="{CHAT_DOC_URL}" target="_blank">
                <button class="button"> Smart Chat </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('##')

col_main_1, col_main_2, col_main_3 = st.columns([1,4,1])

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'> Know Your Data 📈 </h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; font-size: 20px;'>
        The data driving the Explicit Knowledge Copilot encompasses comprehensive details about your organization's colleagues and assets. This includes employee roles, locations, equipment, asset utilization, performance, and maintenance history. Additionally, the data is enriched with terminologies that can be explored interactively, providing users with the clarity needed to make informed decisions.
    </div>
    """, 
    unsafe_allow_html=True
)
with open(VIDEO_FILE_PATH, 'rb') as video_file:
    video_bytes = video_file.read()
    video_base64 = base64.b64encode(video_bytes).decode('utf-8')
    video_html = f"""
        <video autoplay loop muted style="width:100%; height:auto;">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        """
    st.markdown('##')
    st.components.v1.html(video_html, height=400)

#################################################### METHODS ################################################
@st.cache_data(show_spinner=False)
def rename_dataset_columns(dataframe):
    dataframe.columns = dataframe.columns.str.replace('[#,@,&,$,(,)]', '')
    dataframe.columns = [re.sub(r'%|_%', '_percentage', x) for x in dataframe.columns]
    dataframe.columns = dataframe.columns.str.replace(' ', '_')
    dataframe.columns = [x.lstrip('_') for x in dataframe.columns]
    dataframe.columns = [x.strip() for x in dataframe.columns]
    return dataframe

@st.cache_resource
def load_data(UPLOADED_FILE):
    if UPLOADED_FILE is not None:
        data = pd.read_csv(UPLOADED_FILE)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data = rename_dataset_columns(data)

    data_random_sample = data.sample(frac=0.05)
    rows = data_random_sample.values.tolist()
    header = data_random_sample.columns.tolist()
    sample_data_overview = header + rows[:10]
    return data, sample_data_overview

@st.cache_data(show_spinner=False)
def get_data_overview(header):
    prompt =  f"Format your answer to markdown latex. Use markdown font size 3. " \
              f"Please do not include heading or subheading." \
              f"Given the csv file with headers: {header} " \
              f"You are an actuary, " \
              f"Describe what each column means and what the dataset can be used for?"

    response = open_ai_gpt3.gpt_promt(prompt)
    st.markdown(response['content'])

def display_pdf(file_path):
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        st.subheader(f"Page {page_num + 1}")
        st.text(page.extract_text())

def display_pdfs(directory):
    if os.path.exists(directory):
        # List all PDF files in the directory
        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

        if pdf_files:
            for pdf_file in pdf_files:
                pdf_path = os.path.join(directory, pdf_file)

                # Add a button for each PDF file
                if st.button(f"Open {pdf_file}"):
                    display_pdf(pdf_path)
        else:
            st.warning("No PDF files found in the directory.")
    else:
        st.error("The directory path does not exist. Please check the path and try again.")

def load_graph(KG_PATH):
    with open(KG_PATH, 'rb') as f:
        G = pickle.load(f)
    return G

def get_employee_names(G):
    employee_names = set()
    for node in G.nodes:
        if node.startswith("Employee:"):
            employee_name = node.split("Employee: ")[1].split(" (ID:")[0]
            employee_names.add(employee_name)
    return sorted(employee_names)

def filter_employee_and_asset_graph(G, employee_name):
    filtered_nodes = []
    asset_nodes = []
    for node in G.nodes:
        if employee_name in node:
            filtered_nodes.append(node)
            for neighbor in G.neighbors(node):
                filtered_nodes.append(neighbor)
                if 'Asset:' in neighbor:
                    asset_nodes.append(neighbor)
    for asset in asset_nodes:
        for neighbor in G.neighbors(asset):
            filtered_nodes.append(neighbor)
    subgraph = G.subgraph(filtered_nodes)
    return subgraph






#################################################### DATA EXPLORATION ################################################
colleague_data, colleague_data_overview = load_data(COLLEAGUE_DATA_PATH)
asset_data, asset_data_overview = load_data(ASSET_DATA_PATH)
st.markdown("<h3 style='text-align: left;'> 🔎 Data Exploration </h3>", unsafe_allow_html=True)
st.markdown("The expanders below provide insights into the structure and key components of the datasets that are used in the Explicit Knowledge Copilot. Use the expanders to dive deeper into each dataset.")

# Inspecting raw data
with st.expander("Explore Colleague Data"):
    st.markdown("<h5 style='text-align: center;'> Raw Data </h5>", unsafe_allow_html=True)
    st.markdown('The Colleague Data dataset includes comprehensive details about employees within the organization. \
                Using this dataset a users can understand the distribution of employees across various departments, their roles, and the technology they use.\
                Also, this data enables leadership to make informed decisions on promotions, team restructuring, and identifying skill gaps for targeted training programs.')
    st.write(colleague_data)
    st.markdown('##')
    st.markdown("<h5 style='text-align: center;'> Data Explanation </h5>", unsafe_allow_html=True)
    get_data_overview(colleague_data_overview)


with st.expander("Explore Asset Data"):
    st.markdown("<h5 style='text-align: center;'> Raw Data </h5>", unsafe_allow_html=True)
    st.markdown('The Asset Data dataset captures essential information about the company\'s IT assets. \
                It helps track the performance, maintenance, and lifecycle of assets, ensuring they are effectively utilized and maintained.\
                With this data, the organization can optimize asset management, plan upgrades, and ensure that resources are allocated effectively \
                across departments.')
    st.write(asset_data)
    st.markdown('##')
    st.markdown("<h5 style='text-align: center;'> Data Explanation </h5>", unsafe_allow_html=True)
    get_data_overview(asset_data_overview)

st.markdown('##')
st.markdown("<h3 style='text-align: left;'> 📄 Supporting Documents for Data Insights </h3>", unsafe_allow_html=True)
display_pdfs(PDF_DIR_PATH)
st.markdown('##')


st.markdown("<h3 style='text-align: left;'> 💡 See the Big Picture – Data Relationships Awaits! </h3>", unsafe_allow_html=True)
#################################################### DISPLAY THE DAG ################################################
with st.expander("🔎 Click to Discover How Everything Connects"):
    st.markdown('##')
    st.markdown("<h3 style='text-align: left;'> 💡 An Interactive DAG Graph For Employee and Asset Relationships</h3>", unsafe_allow_html=True)
    with open(DAG_HTML_PATH, 'r') as file:
        html_content = file.read()
    components.html(html_content, height=750, width=750)
    st.markdown('##')




#################################################### EMPLOYEE SEARCH ################################################

with st.expander("🔎 Quick Search: Unravel Employee-Asset Links"):
    G = load_graph(KG_PATH)
    st.markdown("<h3 style='text-align: left;'> 🔎 Employee Search </h3>", unsafe_allow_html=True)

    # Function to get employee names from graph G
    def get_employee_names(G):
        return [node for node in G.nodes if 'Employee:' in node]

    # Function to get asset IDs from graph G
    def get_asset_ids(G):
        return [node for node in G.nodes if 'Asset:' in node]

    # Function to filter graph based on employee and associated asset + nodes
    def filter_employee_and_asset_graph(G, selected_employee):
        nodes_to_keep = set()
        
        # Step 1: Add selected employee node and its neighbors (directly connected nodes)
        for node in G.nodes:
            if selected_employee in node:
                nodes_to_keep.add(node)
                for neighbor in G.neighbors(node):
                    nodes_to_keep.add(neighbor)
                    
                    # Step 2: If the neighbor is an asset node, get its neighbors
                    if 'Asset:' in neighbor:
                        for asset_neighbor in G.neighbors(neighbor):
                            nodes_to_keep.add(asset_neighbor)
        
        return G.subgraph(nodes_to_keep)

    # Function to filter graph based on asset and associated employee + nodes
    # Function to filter graph based on asset and associated employee + nodes
    # Function to filter graph based on asset and associated employee + nodes
    def filter_asset_and_employee_graph(G, selected_asset):
        nodes_to_keep = set()

        # Step 1: Add selected asset node and its neighbors (directly connected nodes)
        if selected_asset in G.nodes:
            nodes_to_keep.add(selected_asset)
            asset_neighbors = list(G.neighbors(selected_asset))

            for neighbor in asset_neighbors:
                nodes_to_keep.add(neighbor)
                
                # Step 2: If the neighbor is an employee node, add it and all of its neighbors
                if 'Employee:' in neighbor:
                    nodes_to_keep.add(neighbor)  # Add the employee node
                    employee_neighbors = list(G.neighbors(neighbor))  # Get neighbors of the employee

                    # Step 3: Add all neighbors of the employee node
                    for emp_neighbor in employee_neighbors:
                        nodes_to_keep.add(emp_neighbor)

        return G.subgraph(nodes_to_keep)



    # Main Streamlit app logic
    # Radio button to choose between search by employee or asset
    search_option = st.radio("Search By:", ("Employee Name", "Asset ID"))

    if search_option == "Employee Name":
        # Dropdown menu to select employee name
        employee_names = get_employee_names(G)
        selected_employee = st.selectbox("Select Employee Name:", employee_names)

        if selected_employee:
            # Filter graph based on selected employee
            subgraph = filter_employee_and_asset_graph(G, selected_employee)
            if subgraph:
                # Visualize the graph using pyvis
                net = Network(notebook=False, height="750px", width="100%", cdn_resources='in_line')
                net.from_nx(subgraph)

                # Customize node colors based on node type
                for edge in subgraph.edges(data=True):
                    src, dst, data = edge
                    net.add_edge(src, dst, title=data['relationship'], label=data['relationship'])

                for node in net.nodes:
                    if 'Employee:' in node['id']:
                        node['color'] = 'blue'  
                    elif 'Asset:' in node['id']:
                        node['color'] = 'gray'  
                    elif 'Incident Count:' in node['id']:
                        node['color'] = 'red'  
                    elif 'Replacement Recommendation:' in node['id']:
                        node['color'] = 'orange'  
                    elif 'Utilization Score:' in node['id']:
                        node['color'] = 'green'  
                    elif 'Work Location' in node['id']:
                        node['color'] = 'purple'

                # Save and display the graph
                path = "employee_asset_filtered_graph.html"
                net.save_graph(path)
                st.write(f"Knowledge graph for {selected_employee}:")
                st.components.v1.html(open(path, 'r', encoding='utf-8').read(), height=750)
            else:
                st.error('No data found for the selected employee.')
        else:
            st.error('Please select an employee.')

    elif search_option == "Asset ID":
        # Dropdown menu to select asset ID
        asset_ids = get_asset_ids(G)
        selected_asset = st.selectbox("Select Asset ID:", asset_ids)

        if selected_asset:
            # Filter graph based on selected asset
            subgraph = filter_asset_and_employee_graph(G, selected_asset)
            if subgraph:
                # Visualize the graph using pyvis
                net = Network(notebook=False, height="750px", width="100%", cdn_resources='in_line')
                net.from_nx(subgraph)

                # Customize node colors based on node type
                for edge in subgraph.edges(data=True):
                    src, dst, data = edge
                    net.add_edge(src, dst, title=data['relationship'], label=data['relationship'])

                for node in net.nodes:
                    if 'Employee:' in node['id']:
                        node['color'] = 'blue'  
                    elif 'Asset:' in node['id']:
                        node['color'] = 'gray'  
                    elif 'Incident Count:' in node['id']:
                        node['color'] = 'red'  
                    elif 'Replacement Recommendation:' in node['id']:
                        node['color'] = 'orange'  
                    elif 'Utilization Score:' in node['id']:
                        node['color'] = 'green'  
                    elif 'Work Location' in node['id']:
                        node['color'] = 'purple'

                # Save and display the graph
                path = "asset_employee_filtered_graph.html"
                net.save_graph(path)
                st.write(f"Knowledge graph for Asset ID {selected_asset}:")
                st.components.v1.html(open(path, 'r', encoding='utf-8').read(), height=750)
            else:
                st.error('No data found for the selected asset.')
        else:
            st.error('Please select an asset.')






















    # employee_names = get_employee_names(G)
    # selected_employee = st.selectbox("Select Employee Name:", employee_names)
    # if selected_employee:
    #     subgraph = filter_employee_and_asset_graph(G, selected_employee)
    #     if subgraph:
    #         net = Network(notebook=False, height="750px", width="100%", cdn_resources='in_line')
    #         net.from_nx(subgraph)
    #         for edge in subgraph.edges(data=True):
    #             src, dst, data = edge
    #             net.add_edge(src, dst, title=data['relationship'], label=data['relationship'])

    #         for node in net.nodes:
    #             if 'Employee:' in node['id']:
    #                 node['color'] = 'blue'  
    #             elif 'Asset:' in node['id']:
    #                 node['color'] = 'gray'  
    #             elif 'Incident Count:' in node['id']:
    #                 node['color'] = 'red'  
    #             elif 'Replacement Recommendation:' in node['id']:
    #                 node['color'] = 'orange'  
    #             elif 'Utilization Score:' in node['id']:
    #                 node['color'] = 'green'  
    #             elif 'Work Location' in node['id']:
    #                 node['color'] = 'purple'

    #         path = "employee_asset_filtered_graph.html"
    #         net.save_graph(path)
    #         st.write(f"Knowledge graph for {selected_employee}:")
    #         st.components.v1.html(open(path, 'r', encoding='utf-8').read(), height=750)
    # else:
    #     st.error('Employee not present')
