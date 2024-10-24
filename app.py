import streamlit as st
from datetime import datetime
import time

# 设置页面标题和图标
st.set_page_config(page_title="Chatroom", page_icon="💬")

# 初始化聊天记录文件
chat_file = "chat_history.txt"

# 从文件中加载聊天记录
def load_chat():
    messages = []
    try:
        with open(chat_file, "r") as file:
            for line in file:
                parts = line.strip().split('|', 2)
                if len(parts) == 3:
                    time, user, content = parts
                    messages.append({'time': time, 'user': user, 'content': content})
    except FileNotFoundError:
        pass
    return messages

# 页面布局

# 输入区域
with st.form(key='chat_form', clear_on_submit=True):
    user_name = st.text_input("Your name", key="name_input", value=st.session_state.get('user_name', 'Anonymous'))
    message = st.text_input("Your message", key="message_input")
    submit_button = st.form_submit_button(label="Send")

# 发送消息
if submit_button and message:
    # 保存用户名到会话状态
    st.session_state['user_name'] = user_name
    # 加载当前聊天记录
    messages = load_chat()
    # 添加新消息
    messages.append({'time': datetime.now().strftime('%H:%M:%S'), 'user': user_name, 'content': message})
    # 只保存最新的 100 条消息
    messages = messages[-100:]
    # 保存消息到聊天记录文件
    with open(chat_file, "w") as file:
        for msg in messages:
            file.write(f"{msg['time']}|{msg['user']}|{msg['content']}\n")
    # 重新渲染页面以显示新的消息
    st.experimental_rerun()

# 自动刷新容器
auto_refresh_container = st.empty()

# 实时显示聊天记录
def auto_refresh():
    while True:
        time.sleep(1)
        messages = load_chat()
        auto_refresh_container.empty()
        with auto_refresh_container.container():
            display_chat(messages)

# 显示已有的聊天记录
def display_chat(messages):
    for message in reversed(messages):
        st.write(f"[{message['time']}] {message['user']}: {message['content']}")

# 启动自动刷新
auto_refresh()
