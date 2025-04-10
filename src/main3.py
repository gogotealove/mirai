import random
import time
from dataclasses import dataclass

import dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


# =============================================================
# dataclasses
# @SEEALSO https://python.langchain.com/api_reference/core/messages.html
# =============================================================
@dataclass
class Response:
    content: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


# =============================================================
# variables
# =============================================================
dotenv.load_dotenv()

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_LLM_MODEL = "gpt-4o-mini"
LLM_API_KEY = OPENAI_API_KEY
LLM_MODEL = OPENAI_LLM_MODEL

# LLM model object
llm = None
# LLM response object
llm_res = Response()


# Message for priming AI behavior.
llm_system_message = "あなたは サッカーの専門家です"
llm_system_message = "あなたは女子高生です。決して丁寧語を使わず、絵文字も活用してハイテンションでフレンドリーな感じで回答してください。"
# Message from an AI.
llm_ai_message = "こんにちは"
# Message from a human.
llm_human_message = ""


# =============================================================
# generate LLM model
# temperature (0.0 ~ 1.0)
#   - 0.0: より一貫性のある回答
#   - 0.1: 安定した回答を得るための推奨値
#   - 1.0: よりクリエイティブで多様な回答
# =============================================================
llm = ChatOpenAI(model=OPENAI_LLM_MODEL, temperature=0.1)

# =============================================================
# UI
# =============================================================
st.title("MIRAI")
# st.write(LLM_API_KEY)
chat_input = st.chat_input("メッセージを送信 ")

with st.sidebar:
    st.title("Side Navigation")
    page = st.radio("Choice", ["Home", "A-GPT", "B-Gemini"])


# def create_response(llm, message) -> Response:
def create_response(llm, message):
    print("=" * 30)
    print("OK?")
    # exit()

    llm_human_message = message
    messages = [
        SystemMessage(content=llm_system_message),
        AIMessage(content=llm_ai_message),
        HumanMessage(content=llm_human_message),
    ]
    ret = llm.invoke(messages)
    llm_res.content = ret.content
    llm_res.prompt_tokens = ret.response_metadata["token_usage"]["prompt_tokens"]
    llm_res.completion_tokens = ret.response_metadata["token_usage"][
        "completion_tokens"
    ]
    llm_res.total_tokens = ret.response_metadata["token_usage"]["total_tokens"]

    st.write(ret)

    # st.write(create_response(llm, "こんにちは").content)

    # Streamed response emulator
    # def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.1)


# =============================================================
# メッセージを表示と保存をする関数
# =============================================================
def post_message(message, role, save=True):
    # role に応じてメッセージを表示
    # - role: "user" または "ai"
    with st.chat_message(role):
        st.write(message)

    # save=True の場合、メッセージを session_state に保存
    if save:
        st.session_state["messages"].append({"message": message, "role": role})


# =============================================================
# セッションメッセージキューを準備
# =============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =============================================================
# メッセージキューの中身を表示
# =============================================================
for message in st.session_state["messages"]:
    post_message(
        message["message"],
        message["role"],
        save=False,
    )

# =============================================================
# メイン処理
# =============================================================
if chat_input:
    # 自身のメッセージを表示＆キューイング
    post_message(chat_input, "user", save=True)

    # AIからの回答を得る
    llm_human_message = chat_input
    messages = [
        SystemMessage(content=llm_system_message),
        AIMessage(content=llm_ai_message),
        HumanMessage(content=llm_human_message),
    ]
    ret = llm.invoke(messages)

    llm_res.content = str(ret.content)
    llm_res.prompt_tokens = ret.response_metadata["token_usage"]["prompt_tokens"]
    llm_res.completion_tokens = ret.response_metadata["token_usage"][
        "completion_tokens"
    ]
    llm_res.total_tokens = ret.response_metadata["token_usage"]["total_tokens"]

    # AIからの回答を表示
    post_message(llm_res.content, "ai", save=True)

    # for DEBUG
    with st.sidebar:
        st.write(st.session_state)

# React to user input
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Display assistant response in chat message container
#     # with st.chat_message("assistant"):
#     #     # response = st.write_stream(response_generator())
#     #     # response = st.write_stream(create_response(prompt))
#     #     response = st.write_stream("hello")

#     with st.chat_message("assistant"):
#         response = st.write_stream("てすと")

#     # with st.chat_message("assistant"):
#     #     stream = client.chat.completions.create(
#     #         model=st.session_state["openai_model"],
#     #         messages=[
#     #             {"role": m["role"], "content": m["content"]}
#     #             for m in st.session_state.messages
#     #         ],
#     #         stream=True,
#     #     )
#     #     response = st.write_stream(stream)

#     st.session_state.messages.append({"role": "assistant", "content": response})
