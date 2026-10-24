import os
import autogen
from dotenv import load_dotenv

print("🤖 Yapay Zeka Konferans Sistemi Başlatılıyor...\n")

while True:
    startup_fikri = input("Analiz edilmesini istediğiniz fikrinizi girin: ").strip()
    if startup_fikri == "/exit":
        print("Konferans başlatılmadan kapatıldı.")
        raise SystemExit(0)
    if startup_fikri:
        break
    print("Fikir boş olamaz. Lütfen fikrinizi yazın veya çıkmak için /exit girin.\n")

# API anahtari .env dosyasindan okunur; bu dosyayi kimseyle paylasma.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    raise SystemExit(
        "GEMINI_API_KEY bulunamadi. Proje klasorunde .env dosyasi olusturup "
        "GEMINI_API_KEY alanina yeni API anahtarini ekle."
    )

config_list = [
    {
        "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        "api_key": api_key,
        "api_type": "google"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.2,  # Raporların objektif ve tutarlı olması için düşük sıcaklık
}

class ConferenceUserProxyAgent(autogen.UserProxyAgent):
    def get_human_input(self, prompt):
        prompt = prompt.replace("type 'exit'", "type '/exit'")
        reply = super().get_human_input(prompt)
        if reply.strip() == "/exit":
            return "exit"
        if reply.strip() == "exit":
            return f"{reply} "
        return reply

# SEN (Kullanıcı / Girişimci)
# human_input_mode="ALWAYS" sayesinde her turda sana mikrofon uzatılır.
# Masadan kalkmak istediğinde terminale sadece '/exit' yazman yeterlidir.
girisimci = ConferenceUserProxyAgent(
    name="Girisimci_Can",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda message: False,
    code_execution_config=False,
    system_message="Sen projenin sahibisin. Fikrini savun, ajanların sorularını yanıtla. Tartışmayı bitirmek için yalnızca '/exit' yaz."
)

# AJAN 1: Stratejik Finans ve Risk Analisti
finans_analisti = autogen.AssistantAgent(
    name="Finans_ve_Risk_Analisti",
    llm_config=llm_config,
    system_message="""Sen kıdemli bir Finansal Stratejist ve Risk Analistisin. 
    Girişimcinin startup fikrini objektif ve acımasızca eleştir. 
    Gelir modelindeki açıkları bul, regülasyon risklerini (KVKK vb.) hatırlat. 
    Asla sahte iyimserlik yapma, ayakları yere basan finansal mantık ara."""
)

# AJAN 2: Baş Yapay Zeka ve Sistem Mimarı
sistem_mimari = autogen.AssistantAgent(
    name="AI_ve_Sistem_Mimari",
    llm_config=llm_config,
    system_message="""Sen Baş Yapay Zeka Mimarı ve Otomasyon Uzmanısın. 
    Girişimcinin fikrini hayata geçirecek en sade, fonksiyonel ve bütçe dostu yazılım mimarisini planla.
    Gereksiz kütüphanelerden ve karmaşık sistemlerden kaçın. Finans analistinin maliyet eleştirilerine teknik çözümler üret."""
)

# =====================================================================
# 3. AŞAMA: GROUP CHAT (BEYİN FIRTINASI - SEN MASADASIN)
# =====================================================================
groupchat = autogen.GroupChat(
    agents=[girisimci, finans_analisti, sistem_mimari],
    messages=[],
    max_round=12,  # Token optimizasyonu için maksimum konuşma turu
    speaker_selection_method="round_robin"
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

print("🚀 1. AŞAMA: Grup Sohbeti ve Beyin Fırtınası Başlıyor.")
print("💡 Ajanlar konuşurken size söz geldiğinde fikrinizi detaylandırın.")
print("🚪 Masadan kalkıp nihai raporu üretmek istediğinizde tek başına '/exit' yazıp Enter'a basın.\n")

girisimci.initiate_chat(
    manager,
    message=f"Merhaba ekip, yeni startup fikrim şu şekilde: {startup_fikri}. Lütfen objektif olarak tartışmaya başlayın."
)

# =====================================================================
# 4. AŞAMA: SEQUENTIAL REPORTING (Sıralı Bürokrasi - Sen Kalktın)
# =====================================================================
print("\n🏁 1. Aşama Bitti. Girişimci masadan kalktı.")
print("📊 2. AŞAMA: Tartışma Geçmişi Alınıyor ve Nihai Karar Raporu Üretiliyor...\n")

# Grup sohbetindeki tüm konuşma geçmişini metne dönüştürüyoruz
tartisma_loglari = ""
for msg in groupchat.messages:
    sender = msg['name']
    content = msg['content']
    tartisma_loglari += f"[{sender}]: {content}\n\n"

# Raporu derleyecek Üçüncü Ajan: Baş Editör ve Genel Sekreter
bas_editor = autogen.AssistantAgent(
    name="Bas_Editor",
    llm_config=llm_config,
    system_message="""Sen üst düzey bir Baş Editör ve Sistem Raporlayıcısın. 
    Sana verilen grup tartışması loglarını inceler, oradaki tüm kaosu ve fikirleri elersin.
    Tekrara düşmeden, sade, net ve profesyonel bir dille startup yol haritası hazırlarsın.
    Gereksiz jargondan ve maddelemelerden kaçınarak akıcı bir metin üret."""
)

rapor_talebi = f"""
Aşağıdaki grup tartışması loglarını derinlemesine incele. 
Tüm riskleri, teknik mimari önerilerini ve fikirleri birleştirerek, girişimci için eyleme geçmeden önce okuyacağı objektif bir 'Nihai Karar Raporu ve Stratejik Yol Haritası' çıkar.

TARTIŞMA GEÇMİŞİ:
{tartisma_loglari}
"""

# Baş editör raporu hazırlar
nihai_rapor = bas_editor.generate_reply(messages=[{"role": "user", "content": rapor_talebi}])

# Raporu bilgisayara dosya olarak kaydetme
dosya_adi = "startup_nihai_degerlendirme_raporu.txt"
with open(dosya_adi, "w", encoding="utf-8") as f:
    f.write(str(nihai_rapor))

print(f"✅ İşlem Tamamlandı! Objektif analiz raporun '{dosya_adi}' adıyla kaydedildi. Harika bir strateji kurdun.")
