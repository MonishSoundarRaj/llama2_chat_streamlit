import streamlit as st
import replicate as rp
import os

st.set_page_config(page_title="Llama 2")

with st.sidebar:
    st.title("Llama 2")
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success("API key already provided!", icon='✔️')
    else:
        replicate_api = st.text_input("Enter Replicate API token/key", type="password")
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your correct credentials!', icon='⚠️')
        else:
            st.success('Your API token/key is successfully set for chat!')

os.environ['REPLICATE_API_TOKEN'] = replicate_api

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat', on_click=clear_chat_history)

def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n" 
    
    output = rp.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                    input = {"prompt": f"{string_dialogue} {prompt_input} Assistant: ", "temperature":0.1, "top_p":0.9, "max_length": 2000, 
                             "repetition_penalty":1})
    
    return output

if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "User", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item

            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    
    st.session_state.messages.append(message)
    
