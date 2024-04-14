import streamlit as st
import csv, requests, json
from datetime import date
from audiorecorder import audiorecorder
from fuzzywuzzy import process
import plotly.graph_objects as go

url = st.secrets["url"]
stocks = json.load(open("stocks.json"))

st.session_state["ticker"] = None
st.session_state["news"] = None
st.session_state["summary"] = None
st.session_state["model"] = "@hf/thebloke/zephyr-7b-beta-awq"
st.session_state["date"] = "2024-04-12"


with st.sidebar:
    with st.form("Settings ⚙️"):
        model = st.selectbox(
            "Select a Model 🤖",
            [
                "@hf/thebloke/zephyr-7b-beta-awq",
                "@cf/qwen/qwen1.5-0.5b-chat",
                "@hf/nexusflow/starling-lm-7b-beta",
                "@hf/thebloke/llamaguard-7b-awq",
                "@hf/thebloke/neural-chat-7b-v3-1-awq",
                "@cf/meta/llama-2-7b-chat-fp16",
                "@cf/mistral/mistral-7b-instruct-v0.1",
                "@cf/tinyllama/tinyllama-1.1b-chat-v1.0",
                "@hf/mistral/mistral-7b-instruct-v0.2",
                "@hf/thebloke/codellama-7b-instruct-awq",
                "@hf/mistralai/mistral-7b-instruct-v0.2",
                "@cf/thebloke/discolm-german-7b-v1-awq",
                "@cf/meta/llama-2-7b-chat-int8",
                "@hf/thebloke/mistral-7b-instruct-v0.1-awq",
                "@hf/thebloke/openchat_3.5-awq",
                "@cf/qwen/qwen1.5-7b-chat-awq",
                "@hf/thebloke/llama-2-13b-chat-awq",
                "@hf/thebloke/openhermes-2.5-mistral-7b-awq",
                "@cf/tiiuae/falcon-7b-instruct",
                "@hf/nousresearch/hermes-2-pro-mistral-7b",
                "@cf/qwen/qwen1.5-1.8b-chat",
                "@cf/microsoft/phi-2",
                "@hf/google/gemma-7b-it",
                "@cf/qwen/qwen1.5-14b-chat-awq",
                "@cf/openchat/openchat-3.5-0106",
                "@cf/google/gemma-2b-it-lora",
                "@cf/google/gemma-7b-it-lora",
            ],
            placeholder="Select a Model",
        )
        date = st.date_input(
            "Select Date 📅", value=date(2024, 4, 12), format="YYYY-MM-DD"
        )
        submit = st.form_submit_button("Submit ✅")
        if submit:
            st.session_state["model"] = model
            st.session_state["date"] = date


# st.set_page_config(layout="wide")
st.title("Stonks App 📈📉")
# with st.spinner('Wait for it...'):
# time.sleep(5)


@st.cache_data
def show_chart(ticker, date):
    res = requests.get(f"{url}chart_data", params={"ticker": ticker, "date": date})
    if res.status_code == 200:
        stock_data = res.json()
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=stock_data["x"],
                    open=stock_data["open"],
                    high=stock_data["high"],
                    low=stock_data["low"],
                    close=stock_data["close"],
                )
            ]
        )
        # fig.update_layout(xaxis_rangeslider_visible=False)

        st.markdown("## Chart")
        st.plotly_chart(fig)
    else:
        st.write("Error in fetching chart")


@st.cache_data
def fetch_news():
    res = requests.get(f"{url}news")
    if res.status_code == 200:
        return res.json()
    else:
        return [
            {
                "article_url": fake.url(),
                "description": fake.paragraph(),
                "image_url": fake.image(),
                "title": fake.name(),
                "keywords": fake.words(5),
            }
            for _ in range(3)
        ]


col1, col2 = st.columns([3, 1])

with col1:
    option = st.selectbox(
        "Select a stock", stocks.keys(), index=None, placeholder="search for stock"
    )
    if option:
        st.session_state["ticker"] = stocks[option]
    if st.session_state["ticker"]:
        st.write(f"You selected: {st.session_state['ticker']}")
with col2:
    st.write("")
    st.write("")
    audio = audiorecorder("🎙️", "🚫")
    if len(audio) > 0:
        text = ""
        res = requests.get(f"{url}whisper", data=audio.export().read())
        if res.status_code == 200:
            text = res.json()["text"]
        else:
            st.write(f"Error: {res.status_code}")
        if text:
            option = process.extractOne(text, stocks.keys())
            if option:
                st.session_state["ticker"] = stocks[option[0]]
                st.write(f"You selected: {st.session_state['ticker']}")


if st.session_state["ticker"]:
    st.title("Summary")
    with st.container():
        with st.spinner(text="Wait for Summary ... 🔤🔠"):
            res = requests.get(
                f"{url}stocks/{st.session_state['ticker']}",
                params={
                    "date": st.session_state["date"],
                    "model": st.session_state["model"],
                },
            )
            if res.status_code == 200:
                st.session_state["summary"] = res.text
            else:
                st.write(f"Error fetching summary: {res.status_code}")

            st.markdown(st.session_state["summary"])

        lang = st.selectbox(
            "language",
            ["english", "french", "spanish", "hindi", "russian", "chinese"],
            placeholder="Translate to ",
        )
        if lang != "english":
            with st.spinner("Fetching Translation ..."):
                res = requests.get(
                    f"{url}translate",
                    params={"text": st.session_state["summary"], "lang": lang},
                )
                if res.status_code == 200:
                    st.write(f"Translated in {lang}")
                    st.write(res.text)
                else:
                    st.write("Error fetching translation")

        summarize = st.toggle("Summarize More!")

        if summarize:
            with st.spinner("Fetching Summary .."):
                res = requests.get(
                    f"{url}summarize", params={"text": st.session_state["summary"]}
                )
                if res.status_code == 200:
                    st.write(res.text)
                else:
                    st.write("Error fetching summary")

        with st.spinner("Loading chart ... 📊"):
            show_chart(st.session_state["ticker"], st.session_state["date"])

    st.title("News")
    with st.container():
        with st.spinner(text="Wait for news ... 📰🗞️"):
            st.session_state["news"] = fetch_news()

        tabs = st.tabs(
            ["News " + str(i) for i in range(1, len(st.session_state["news"]) + 1)]
        )
        for i, x in enumerate(st.session_state["news"]):
            tabs[i].image(x["image_url"])
            tabs[i].write("### " + x["title"])
            tabs[i].write(x["description"])
            if "keywords" in x:
                tabs[i].write("Keywords = :red[" + str(x["keywords"]) + "]")
            tabs[i].link_button(":blue[Visit Now ↗️]", x["article_url"])

        sentiment = st.toggle("Get Sentiment ➕ ➖")
        if sentiment:
            with st.spinner("Loading Snetiments ..."):
                res = requests.get(
                    f"{url}sentiment",
                    params={"text": x["title"] + "\n" + x["description"]},
                )
                if res.status_code == 200:
                    data = res.json()
                    st.progress(data["POSITIVE"], text="POSITIE")
                    st.progress(data["NEGATIVE"], text="NEGATIVE")
                else:
                    st.write("Failed to fetch Sentiment response.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = requests.get(
            f"{url}chat",
            params={
                "ticker": st.session_state["ticker"],
                "text": prompt,
                "date": st.session_state["date"],
                "model": st.session_state["model"],
            },
        )
        st.chat_message("assistant").markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response})
