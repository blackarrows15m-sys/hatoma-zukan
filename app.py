import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="鳩間島いきもの・植物図鑑", layout="centered")

st.title("🏝️ 鳩間島 AIいきもの図鑑")
st.caption("島の花や生き物の写真を撮ると、AIが鳩間島目線で解説します。")

# Streamlitの安全な設定管理（Secrets）からAPIキーを自動読込
api_key = st.secrets.get("GEMINI_API_KEY")

uploaded_file = st.camera_input("写真を撮る") or st.file_uploader("または画像を選択", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="撮影した写真", use_container_width=True)

    if not api_key:
        st.error("管理設定でAPIキーが設定されていません。")
    else:
        with st.spinner("鳩間島の図鑑を調べています..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = """
                あなたはやさしい鳩間島の自然ガイドです。
                提供された写真に写っている植物または生き物を特定し、以下のフォーマットでわかりやすく解説してください。

                ### 🌿 なまえ
                - 一般名（和名）
                - 八重山地方・沖縄での呼び名（わかれば）

                ### 🔍 特徴・見分け方
                - どんな特徴があるか（2〜3行で簡潔に）

                ### 🏝️ 鳩間島・八重山での豆知識
                - 島のどんな場所で見られるか
                - 昔からの利用法（民具、薬草、食文化など）や島にまつわる話

                ### ⚠️ 注意点（該当する場合）
                - 毒性、刺胞、トゲなど、触ると危険な点があれば記載（なければ「特になし」）
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, image]
                )

                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"判定中にエラーが発生しました: {e}")