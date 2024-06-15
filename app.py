# Ref - chat: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
# Ref - speech: https://platform.openai.com/docs/guides/text-to-speech

from pathlib import Path
from openai import OpenAI
import streamlit as st
from PIL import Image

speech_index = 0
on_change = ""

chu_image_path = "chu.jpg"
chu_image = Image.open(chu_image_path)
dex_image_path = "dex.jpg"
dex_image = Image.open(dex_image_path)
bws_image_path = "byunwoosuk.jpeg"
bws_image = Image.open(bws_image_path)
yuqi_image_path = "yuqi.jpeg"
yuqi_image = Image.open(yuqi_image_path)

chu_txt = open('chu.txt','r').read()
bws_txt = open('byunwoosuk.txt','r').read()
yuqi_txt = open('yuqi.txt','r').read()

yuqi_voice = "nova"
bws_voice = "onyx"

yuqi_title = "송끼끼 ❤️"
bws_title = "우리 우석이 ❤️"

title = yuqi_title
gpt_img = yuqi_image
init_msg = yuqi_txt
voice = yuqi_voice

col_ratio = [1, 6]
img_width = 100

st.markdown("""
    <style>
    img {
        border-radius: 30px;
    }
    div[data-baseweb="select"] > div {
        background-color: #F0F2F6;
    }
    .chat-box {
        max-width: 600px;
        margin: 0 auto;
    }
    .message {
        padding: 10px;
        margin: 20px 0;
        border-radius: 10px;
        display: inline-block;
        max-width: 80%;
        color: black;  /* Change font color to black */
    }
    .message.user {
        background-color: yellow;
        text-color: black;
        text-align: right;
        float: right;
        clear: both;
    }
    .message.bot {
        background-color: white;
        color: black;
        text-align: left;
        float: left;
        clear: both;
    }
    .input-box {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #fff;
        padding: 10px;
        box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def show_user_msg(msg):
    st.markdown(f"<div class='message user'>{msg}</div>", unsafe_allow_html=True)

def show_gpt_msg(msg):
    st.markdown(f"<div class='message bot'>{msg}</div>", unsafe_allow_html=True)

#side bar 선택
def onChangeReset():
    st.session_state.messages = []

    st.session_state.messages.append({"role": "user", "content": init_msg})

    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    )
    st.session_state.messages.append({"role": "assistant", "content": stream.choices[0].message.content})

target = st.sidebar.selectbox(
    "캐릭터 선택",
    ("우기", "변우석"),
    on_change=onChangeReset
)
if target == "우기":
    title = yuqi_title
    gpt_img = yuqi_image
    init_msg = yuqi_txt
    voice = yuqi_voice
else:
    title = bws_title
    gpt_img = bws_image
    init_msg = bws_txt
    voice = bws_voice

col1, col2 = st.columns([5,1])
with col1:
    st.title(title)
with col2:
    st.title("🔍 ☰")


# st.selectbox([
#     "chu",
#     "dex",
#     "bws"
# ])

client = OpenAI(api_key=st.secrets["API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

    st.session_state.messages.append({"role": "user", "content": init_msg})

    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    )
    st.session_state.messages.append({"role": "assistant", "content": stream.choices[0].message.content})

for message in st.session_state.messages[2:]:
    # with st.chat_message(message["role"]):
    #     st.markdown(message["content"])
    if message["role"] == "user":
        # col1, col2 = st.columns(col_ratio)
        # with col1:
        #     st.image(user_img, width = img_width)
        # with col2:
        #     show_user_msg(message["content"])
        show_user_msg(message["content"])
    else:
        col1, col2 = st.columns(col_ratio)
        with col1:
            st.image(gpt_img, width = img_width)
        with col2:
            show_gpt_msg(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # with st.chat_message("user"):
    #     st.markdown(prompt)
    # col1, col2 = st.columns(col_ratio)
    # with col1:
    #     st.image(user_img, width = img_width)
    # with col2:
    #     show_user_msg(prompt)
    show_user_msg(prompt)

    col1, col2 = st.columns(col_ratio)
    with col1:
        st.image(gpt_img, width = img_width)
    with col2:
        # st.markdown(prompt)
    # with st.chat_message("assistant"):
    #     stream = client.chat.completions.create(
    #         model=st.session_state["openai_model"],
    #         messages=[
    #             {"role": m["role"], "content": m["content"]}
    #             for m in st.session_state.messages
    #         ],
    #         stream=True,
    #     )
    #     response = st.write_stream(stream)
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            # stream=True,
        )
        # response = st.write_stream(stream)
        response = stream.choices[0].message.content
        show_gpt_msg(response)
    # st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.messages.append({"role": "assistant", "content": response})

    # TTS
    speech_file_path = Path(str(speech_index) + ".mp3")
    with st.spinner('Converting to the voice...'):
        speech_response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=response
    )
    
    speech_response.stream_to_file(speech_file_path)

    with open(speech_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
    speech_index += 1
