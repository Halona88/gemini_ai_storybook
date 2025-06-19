import streamlit as st
import requests
import base64

st.title("🎨 Gemini 이미지 생성기")

prompt = st.text_input("프롬프트를 입력하세요:", 
    "generate a 3D image of a happy elderly Korean woman with a round face, a pair of glasses and short black wave hair, "
    "wearing a light pastel-colored clothes, sitting outdoors on a low wooden stool. She will be focused on a piece of white watercolor paper "
    "placed on a small easel in front of her, carefully painting delicate pink and red roses with a fine brush. Several small pots of watercolor paints "
    "in various shades of pink, red, and green will be on a nearby weathered wooden table, along with a jar of clear water. The background will show a "
    "slightly blurred garden with lush green foliage and hints of soft sunlight filtering through, suggesting a cool summer breeze. Her face will show "
    "wrinkles of age and a wide, joyful smile, conveying happy laughter."
)

if st.button("이미지 생성"):
    with st.spinner("🖌️ Gemini가 이미지를 그리고 있어요..."):
        try:
            # 실제 FastAPI 서비스 주소로 변경하세요
            API_URL = "https://your-fastapi-service.onrender.com/generate"
            response = requests.post(API_URL, json={"prompt": prompt})
            
            # 디버깅용 응답 로그 출력
            st.write("🔎 응답 상태 코드:", response.status_code)
            st.write("📦 응답 내용:", response.text)

            if response.status_code == 200:
                data = response.json()

                # 1. 이미지 성공 응답 처리
                if "image_base64" in data:
                    img = base64.b64decode(data["image_base64"])

                    st.image(img, caption="✨ 생성된 이미지", use_container_width=True)

                    st.download_button(
                        label="📥 이미지 다운로드",
                        data=img,
                        file_name="generated_img.png",
                        mime="image/png"
                    )

                # 2. 에러 키 응답 처리
                elif "error" in data:
                    st.error(f"❌ 이미지 생성 실패: {data['error']}")

                # 3. 예상치 못한 구조
                else:
                    st.warning("⚠️ 응답은 받았지만 이미지 데이터가 없습니다.")

            else:
                st.error(f"❌ 서버 오류: {response.status_code}")

        except Exception as e:
            st.exception(f"💥 요청 중 예외 발생: {e}")
