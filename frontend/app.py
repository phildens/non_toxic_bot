import streamlit as st
import requests

st.title("🛡️ Toxic Comment Detector")
st.write("Сервис для проверки комментариев на токсичность.")

text_input = st.text_area("Введите текст комментария:", height=100)

MODEL_API_URL = "http://model_api:8000/predict"

if st.button("Проверить"):
    if text_input.strip():
        try:
            with st.spinner("Анализируем..."):
                response = requests.post(MODEL_API_URL, json={"text": text_input})

            if response.status_code == 200:
                data = response.json()
                prob = data['toxic_probability']

                st.metric(label="Вероятность токсичности", value=f"{prob:.2%}")

                if prob > 0.8:
                    st.error("⚠️ Это ТОКСИЧНЫЙ комментарий!")
                elif prob > 0.4:
                    st.warning("🤔 Комментарий сомнительный.")
                else:
                    st.success("✅ Комментарий нормальный.")
            else:
                st.error("Ошибка API модели.")
        except Exception as e:
            st.error(f"Не удалось подключиться к сервису модели: {e}")
    else:
        st.warning("Введите текст!")