import streamlit as st
import time
import json
from datetime import datetime

# 初始化数据文件
DATA_FILE = "focus_records.json"

def load_records():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_record(record):
    records = load_records()
    records.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# 页面配置
st.set_page_config(page_title="🎯 专注学习助手", layout="centered")
st.title("🎯 专注学习应用")

# 输入专注内容
task = st.text_input("📌 输入你的专注内容（如：数学复习/英语单词）")

# 设置专注时间（分钟）
duration_min = st.slider("⏱️ 设置专注时间（分钟）", min_value=1, max_value=120, value=25)

# 开始专注按钮
if st.button("🚀 开始专注"):
    if not task:
        st.warning("请先输入专注内容")
    else:
        st.success(f"开始专注任务：**{task}**，时长：{duration_min} 分钟")
        start_time = time.time()
        end_time = start_time + duration_min * 60

        progress_bar = st.progress(0)
        status_text = st.empty()

        while time.time() < end_time:
            remaining = int(end_time - time.time())
            mins, secs = divmod(remaining, 60)
            status_text.markdown(f"⏳ 剩余时间：**{mins:02d}:{secs:02d}**")
            progress_bar.progress((duration_min * 60 - remaining) / (duration_min * 60))
            time.sleep(1)

        st.balloons()
        st.success("🎉 专注结束，干得漂亮！")

        # 保存记录
        save_record({
            "task": task,
            "duration_min": duration_min,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# 展示历史记录
with st.expander("📖 查看历史专注记录"):
    records = load_records()
    if records:
        for r in reversed(records[-10:]):  # 显示最近10条
            st.markdown(f"- 🗓️ `{r['timestamp']}` | ⏱️ {r['duration_min']} 分钟 | ✍️ {r['task']}")
    else:
        st.write("暂无记录")
