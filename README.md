# AI Konferansi

Bu Python uygulamasi, fikrini Gemini kullanan iki farkli uzman roluyle sirayla tartisir ve konusma sonunda bir degerlendirme raporu olusturur. Roller farkli gorev tanimlariyla ayni Gemini modelini kullanir; ayri AI servisleri degildir.

## Ilk kurulum (Visual Studio)

1. Google AI Studio'dan yeni bir Gemini API anahtari olustur. Daha once kodda bulunan anahtari iptal et; artik kullanma.
2. Visual Studio'da bu proje klasorunu acip **View > Terminal** menusunden terminali baslat.
3. Asagidaki komutlari sirayla calistir:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

4. Proje klasorundeki `.env` dosyasini bir metin editorunde ac. `GEMINI_API_KEY=` sonrasina yeni anahtarini yazip kaydet. `.env.example` dosyasini degil, `.env` dosyasini duzenle.
5. Terminalde `.\.venv\Scripts\python.exe app.py` komutunu calistir ve istenince analiz edilecek fikrini yaz. Konusma sirasinda sana soz verildiginde gorusunu ekle; konferansi bitirip raporu olusturmak icin tek basina `/exit` yaz.
6. Visual Studio Code'da `.vscode/settings.json`, proje icin `.venv` Python yorumlayicisini secer. Bu ayar Visual Studio IDE icin degil, Visual Studio Code icindir.

## Gizlilik

- API anahtari sifrelenmis degildir: uygulama calisirken `.env` dosyasindan okunur ve bu dosya `.gitignore` ile kaynak kontrolunden dislanir. Anahtari `.env`, ekran goruntusu, hata mesaji veya paylasacagin arsive ekleme.
- Kod yardimi isterken `app.py`, `requirements.txt` ve hata metnini paylasabilirsin; `.env`, `.vs` ve kisisel dosyalarini paylasma.
- API kullanimi Google AI Studio'nun guncel kota ve fiyat kosullarina tabidir; ucretsiz kullanim garantisi yoktur.
- Model adini gerekirse `.env` icindeki `GEMINI_MODEL` degerinden degistirebilirsin.
