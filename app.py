import streamlit as st
import replicate as rp
import os

st.set_page_config("🦙 Llama 2 chat app")

st.markdown("<h1 style='text-align: center'>CHATPULSE</h1>", unsafe_allow_html=True)
with st.sidebar:
    st.title("🦙 Llama 2 Control Panel")
    with st.form("llama_2_control_panel_form"):
        st.write("Select a model, enter API token, then press 'Submit'.")
        model_selected = st.selectbox("Select a Llama Model", ["llama-2-70b-chat", "llama-2-13b-chat", "llama-2-7b-chat"])
        if 'REPLICATE_API_TOKEN' in st.secrets:
            st.success("API Token is already present '✔️'")
        else:
            replicate_api = st.text_input("Enter you replicate API key/token", type="password")
            st.markdown("<h4><a href='https://gist.github.com/MonishSoundarRaj/76d1d6ef9a806d879ef4357ae5111f00'>How to get replicate API key?</a></h4>", unsafe_allow_html=True)
                
        submit_change = st.form_submit_button("Submit")
        
        if submit_change:
            if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
                st.warning("Please enter the right credentials! '⚠️'")
            else:
                st.success("Your API token/key has been accepted successfully, and your model has been set")

os.environ['REPLICATE_API_TOKEN'] = replicate_api

if model_selected == "llama-2-70b-chat":
   api = "replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf"
elif model_selected == "llama-2-13b-chat":
    api = "a16z-infra/llama-2-13b-chat:9dff94b1bed5af738655d4a7cbcdcde2bd503aa85c94334fe1f42af7f3dd5ee3"
else:
    api = "a16z-infra/llama-2-7b-chat:d24902e3fa9b698cc208b5e63136c4e26e828659a9f09827ca6ec5bb83014381"

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

st.markdown(f"<h5>Model Selected: {model_selected}</h5>", unsafe_allow_html = True)

for item in st.session_state.messages:
    with st.chat_message(item['role']):
        st.write(item['content'])

def clear_chat():
     messages = [{"role": "assistant", "content": "How can I help you today?"}]

st.sidebar.button("Clear Chat", on_click=clear_chat)

def generate_llama_2_messages(prompt, api_for_selected_model):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    
    for dict_item in st.session_state.messages:
        if dict_item['role'] == 'user':
            string_dialogue += 'User: ' + dict_item['content'] + "\n\n"
        else:
            string_dialogue += "assistant" + dict_item['content'] + "\n\n"
    
    output = rp.run(api_for_selected_model, 
                    input = {'prompt': f"{string_dialogue} {prompt} + Assistant: ", "temperature": 0.2, 'max_length': 2000})
    
    return output

if prompt := st.chat_input(disabled= not replicate_api):
    st.session_state.messages.append({"role": "User", "content": prompt})
    with st.chat_message("user"):
       st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            response = generate_llama_2_messages(prompt, api)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                
            placeholder.markdown(full_response)
            
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


    
