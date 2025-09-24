from openai import OpenAI
import os
import streamlit as st
import requests

# -------------------------
# OpenAI KEY
# -------------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -------------------------
#  Kullanıcı ülkesini IP üzerinden tespit et
# -------------------------
def get_user_country():
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5)
        data = res.json()
        return data.get("country_code"), data.get("country_name")
    except:
        return None, None

# -------------------------
#  Türkiye için evcil hayvan listesi
# -------------------------
TR_EVCIL_HAYVANLAR = {
    "Memeliler": [
        "Kedi", "Köpek", "Hamster", "Guinea Pig", "Tavşan", "Şeker Planörü (Sugar Glider)", "Çinçilla (Chinchilla)"
    ],
    "Kuşlar": [
        "Muhabbet Kuşu", "Kanarya", "Sultan Papağanı"
    ],
    "Sürüngenler": [
        "Leopar Gecko", "Kaplumbağa"
    ],
    "Akvaryum Balıkları": [
        "Tatlı Su Balıkları", "Tuzlu Su Balıkları"
    ]
}

# -------------------------
#  GPT cevabı 
# -------------------------
def chatbot_cevap(mesaj):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen veteriner tavsiyesi veren bir evcil hayvan yardım asistanısın. Hangi dilde yazıldıysa o cevap veriyorsun."},
                {"role": "user", "content": mesaj}
            ],
            temperature=0.6,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# -------------------------
# Günlük bilgiler kısmı 
# -------------------------
def gunluk_bilgi(hayvan_turu):
    try:
        mesaj = f"Lütfen bana {hayvan_turu} hakkında kısa, ilginç ve değişik bir bilgi ver. Maksimum 2 cümle olsun."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen veteriner tavsiyesi veren bir evcil hayvan yardım asistanısın."},
                {"role": "user", "content": mesaj}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# -------------------------
# Streamlit 
# -------------------------
st.set_page_config(page_title="🐾 PetSocial Yapay Zeka Evcil Hayvan Chatbot", page_icon="🐶")
st.title("🐾 Evcil Hayvan Yardım Chatbotu (GPT Destekli)")
st.write("✍ Sorunuzu yazın ve hayvanlar hakkında bilgi alın:")

mesaj = st.text_input("Soru yazın:")

if mesaj:
    with st.spinner("Yanıt hazırlanıyor..."):
        cevap = chatbot_cevap(mesaj)
    st.markdown(f" Cevap: \n {cevap}")

# -------------------------
# Ülkeye göre evcil hayvan listesi
# -------------------------
st.write("---")
st.subheader("Günlük Evcil Hayvan Bilgisi")

country_code, country_name = get_user_country()
if country_code == "TR":
    st.info(f"🌍 Algılanan bölge: {country_name} ({country_code})")
    # Kategorileri açılır menüye dönüştür
    kategori = st.selectbox("Kategori seçin:", list(TR_EVCIL_HAYVANLAR.keys()))
    pets = TR_EVCIL_HAYVANLAR[kategori]
else:
    st.warning("Ülkeniz Türkiye değil veya tespit edilemedi. Basit liste kullanılıyor.")
    pets = ["Kedi", "Köpek", "Kuş", "Balık", "Hamster", "Tavşan"]

hayvan_turu = st.selectbox("Hangi hayvan hakkında bilgi almak istiyorsun?", pets)

if st.button("📖 Günlük Bilgiyi Göster"):
    bilgi = gunluk_bilgi(hayvan_turu)
    st.info(bilgi)



