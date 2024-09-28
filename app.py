
import streamlit as st 
import validators 

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain 

from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

## Streamlit App 

st.title("Summarize Youtube Video & Websites within  Seconds !")

st.subheader("Summarize URL")


# get groq api key & ur field to be summarized 

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", type="password")


# LLM Model using Groq ! 
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

prompt_template = """

provide an easy to understand summary of following content in 300 Words:

Content: {text}


"""

prompt = PromptTemplate(template=prompt_template,input_variables=['text'])

url = st.text_input("URL",label_visibility="collapsed")


if st.button("Summarize the Content from YT & Websites in Seconds"):
    if not groq_api_key or not url.strip():
        st.error("Please provide information.")
    
    elif not validators.url(url):
        st.error("Please Enter Valid URL")

    else:
        try:
            with st.spinner("waiting..."):
                # loading 
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url,add_video_info=True)
                else:
            #         headers = {
            #  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
              
            #     }
                    url = [url]
                    loader = UnstructuredURLLoader(urls=url)
                
                docs = loader.load()

                chain = load_summarize_chain(llm,chain_type="stuff",prompt= prompt)

                output_summary= chain.run(docs)

                st.success(output_summary)

        except Exception as e:
            st.write("Exception ",e)

