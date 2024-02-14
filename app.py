import streamlit as st
import pandas as pd
from PIL import Image
import ast

flag_data = pd.read_csv("overallanalysis 2.csv")
all_keywords = sorted(set(flag_data['Keyword'].tolist())) 
st.set_page_config(page_title='Flag Data Viewer', layout='wide', initial_sidebar_state='expanded')
logo = Image.open('Logo.jpg')  
st.sidebar.image(logo, use_column_width=False, width=200)

st.markdown(
    """
    <style>
        .header {
            background-color: #78BE20;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 32px; /* Increased font size */
            margin-bottom: 10px;
        }
        .flag-name {
            font-size: 20px;
            font-weight: bold;
            display: inline-block;
            width: 50px; /* Adjust as needed */
        }
        .flag-value {
            font-size: 16px;
        }
        .checkbox-label {
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if 'selected_keyword' not in st.session_state:
    st.session_state.selected_keyword = None
    st.session_state.selected_3_keyword = None

with st.sidebar:
    selected_keyword = st.selectbox("Select Keyword", all_keywords, key="select_keyword")
    
    if selected_keyword != st.session_state.selected_keyword:
        st.session_state.selected_keyword = selected_keyword
        filtered_keywords = sorted(set(flag_data[flag_data['Keyword'] == selected_keyword]['3 keywords'].tolist()))
        st.session_state.selected_3_keyword = None  # Reset selected 3 keyword if keyword changes
    else:
        filtered_keywords = sorted(set(flag_data[flag_data['Keyword'] == selected_keyword]['3 keywords'].tolist()))
    
    selected_3_keyword = st.selectbox("Select 3 Keyword", filtered_keywords, key="select_3_keyword")
    st.session_state.selected_3_keyword = selected_3_keyword  # Store selected 3 keyword in session state

if st.session_state.selected_keyword and st.session_state.selected_3_keyword:
    st.markdown('<div class="header">Profile Templatization for Selected Keyword</div>', unsafe_allow_html=True)

    keyword_data = flag_data[(flag_data['Keyword'] == st.session_state.selected_keyword) & (flag_data['3 keywords'] == st.session_state.selected_3_keyword)]
    if not keyword_data.empty:
        common_flags = keyword_data['Common flags'].iloc[0]
        changing_flags = keyword_data['changing flags'].iloc[0]

        st.write(f"### Common flags")
        st.write("Checked = '1'", " Unchecked = '0'")

        common_flags_dict = ast.literal_eval(common_flags)

        common_flags_dict = dict(sorted(common_flags_dict.items(), key = lambda x: x[1]))

        flag_names = list(common_flags_dict.keys())
        flag_values = list(common_flags_dict.values())

        for i in range(0, len(flag_names), 3):
            cols = st.columns(3)
            for j in range(3):
                index = i + j
                if index < len(flag_names):
                    flag_name = flag_names[index]
                    flag_value = common_flags_dict[flag_name]
                    flag_col1, flag_col2 = cols[j].columns([0.1,1],gap='small')
                    #flag_col1.write(f"{flag_name}:")
                    if flag_value not in (0, 1):
                        flag_value = cols[j].text_input(label='', value=str(flag_value), key=f"{st.session_state.selected_keyword}_{flag_name}_textinput")
                    else:
                        flag_checkbox = flag_col1.checkbox(label='', key=f"{st.session_state.selected_keyword}_{flag_name}_checkbox")
                        flag_value = bool(flag_value)
                    flag_col2.write(f"{flag_name}:")
                    

        st.write(f"### Changing flags")
        changing_flags_list = changing_flags.split(',')
        for i in range(0, len(changing_flags_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(changing_flags_list):
                    flag_col1, flag_col2 = cols[j].columns([0.1,1],gap='small')
                    
                    flag_col1.checkbox(label='', key=f"{st.session_state.selected_keyword}_{changing_flags_list[i + j].strip()}_checkbox")
                    flag_col2.write(f"{changing_flags_list[i + j].strip()}:")

        if st.button('Save Profile'):
            st.write("The profile is saved successfully.")

        st.markdown("____________________________________________________________________________________")
        st.write("*2024 Clean Earth")
    else:
        st.write("No data found for the selected keyword and 3 keywords combination.")
