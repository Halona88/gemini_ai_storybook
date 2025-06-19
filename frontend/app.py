import streamlit as st
import requests
import base64

st.title("🎨 Gemini 이미지 생성기")

prompt = st.text_input("프롬프트를 입력하세요:", "generate a 3D image of a happy elderly Korean woman with a round face, a pair of glasses and short black wave hair, wearing a light pastel-colored clothes, sitting outdoors on a low wooden stool. She will be focused on a piece of white watercolor paper placed on a small easel in front of her, carefully painting delicate pink and red roses with a fine brush. Several small pots of watercolor paints in various shades of pink, red, and green will be on a nearby weathered wooden table, along with a jar of clear water. The background will show a slightly blurred garden with lush green foliage and hints of soft sunlight filtering through, suggesting a cool summer breeze. Her face will show wrinkles of age and a wide, joyful smile, conveying happy laughter ")

if st.button("이미지 생성"):
    with st.spinner("이미지 생성 중..."):
        response = requests.post("http://localhost:8000/generate", json={"prompt": prompt})
        if response.status_code == 200:
            data = response.json()
            if "image_base64" in data:
                img = base64.b64decode(data["image_base64"])

                # 이미지 보여주기기
                st.image(img, caption="✨ 생성된 이미지", use_container_width=True)

                # 다운로드 버튼 추가하기
                st.download_button(
                    label = "📥 이미지 다운로드",
                    data = img,
                    file_name = 'generated_img.png',
                    mime = 'image/png'
                )

            else:
                st.error("이미지를 불러오지 못했습니다.")
