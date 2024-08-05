import streamlit as st
import datahelper

# Oturum durumu kontrol ediliyor. Eğer 'dataload' anahtarı oturum durumunda yoksa, False olarak ayarlanıyor.
if "dataload" not in st.session_state:
    st.session_state.dataload = False

# Bu fonksiyon, 'dataload' durumunu True olarak ayarlıyor.
def activate_dataload():
    st.session_state.dataload = True

# Streamlit uygulamasının sayfa ayarları yapılıyor.
st.set_page_config(page_title="Data Explorer 🤖", layout="wide")

# Sayfanın üst kısmında bir banner resmi gösteriliyor.
st.image(image="./img/img/app_banner.jpg", use_column_width=True)

# Sayfanın başlığı ayarlanıyor.
st.title("Data Explorer: Doğal Dilde Veri Keşfi 🤖")
st.divider()  # Görsel bir bölücü ekleniyor.

# Kenar çubuğunda kullanıcıdan CSV dosyası yüklemesini isteyen alt başlık ve bölücü ekleniyor.
st.sidebar.subheader("Veriye Dosyanızı Yükleyin")
st.sidebar.divider()

# Kenar çubuğunda CSV dosyası yükleyici oluşturuluyor.
loaded_file = st.sidebar.file_uploader("Yüklemek istediğiniz CSV dosyasını seçiniz", type="csv")

# Kenar çubuğunda bir yükleme butonu ekleniyor. Tıklanıldığında 'activate_dataload' fonksiyonunu çağırıyor.
load_data_btn = st.sidebar.button(label="Yükle", on_click=activate_dataload, use_container_width=True)

# Sayfada üç kolon oluşturuluyor: veriyi ön işleme, boş kolon ve veriyle etkileşim için.
col_prework, col_dummy, col_interaction = st.columns([4, 1, 7])

# Eğer 'dataload' durumu True ise, yani kullanıcı bir dosya yüklediğinde.
if st.session_state.dataload:
    # Veri özetini oluşturan fonksiyon tanımlanıyor ve cache'leniyor. 
    @st.cache_data #Önbellekleme yapalım, bir kez summarize metodu çalışınca parametresi değişmezse, buradaki işlemlerin tekrar tekrar yapılmasını engelliyor
    def summarize():
        # Dosya başına dönülüyor.
        loaded_file.seek(0)
        # Veri özetini almak için datahelper modülündeki summarize_csv fonksiyonu çağırılıyor.
        data_summary = datahelper.summarize_csv(data_file=loaded_file)
        return data_summary
    
    # Veri özeti fonksiyonu çalıştırılarak sonuç alınıyor.
    data_summary = summarize()

    # İlk kolonda veri özetini gösterme işlemleri yapılıyor.
    with col_prework:
        st.info("VERİ ÖZETİ")  # Bilgi kutusu başlığı
        st.subheader("Verinizden Örnek Bir Kesit:")  # Alt başlık
        st.write(data_summary["initial_data_sample"])  # İlk 5 satırın gösterimi
        st.divider()  # Görsel bölücü
        st.subheader("Veri Kümesinde Yer Alan Değişkenler:")  # Alt başlık
        st.write(data_summary["column_descriptions"])  # Sütun açıklamaları
        st.divider()  # Görsel bölücü
        st.subheader("Eksik/Kayıp Veri Durumu:")  # Alt başlık
        st.write(data_summary["missing_values"])  # Eksik veri bilgisi
        st.divider()  # Görsel bölücü
        st.subheader("Mükerrer Veri Durumu:")  # Alt başlık
        st.write(data_summary["duplicate_values"])  # Mükerrer veri bilgisi
        st.divider()  # Görsel bölücü
        st.subheader("Temel Metrikler")  # Alt başlık
        st.write(data_summary["essential_metrics"])  # Temel istatistiksel metrikler
    
    # Ortadaki kolon boş bırakılıyor.
    with col_dummy:
        st.empty()
    
    # Üçüncü kolonda veri ile etkileşim bölümünü oluşturma işlemleri yapılıyor.
    with col_interaction:
        st.info("VERİYLE ETKİLEŞİM")  # Bilgi kutusu başlığı

        # Kullanıcıdan incelemek istediği değişkeni girmesini isteyen metin girişi.
        variable_of_interest = st.text_input(label="İncelemek İstediğiniz Değişken Hangisi?")
        examine_btn = st.button(label="İncele")  # İnceleme butonu
        st.divider()  # Görsel bölücü

        # Değişkeni inceleyen fonksiyon tanımlanıyor ve cache'leniyor.
        @st.cache_data
        def explore_variable(data_file, variable_of_interest):
            data_file.seek(0)  # Dosya başına dönülüyor.
            dataframe = datahelper.get_dataframe(data_file=data_file)  # DataFrame alınıyor.
            st.bar_chart(data=dataframe, y=[variable_of_interest])  # Belirtilen değişkenin bar grafiği çiziliyor.
            st.divider()  # Görsel bölücü
            data_file.seek(0)  # Dosya başına dönülüyor.
            trend_response = datahelper.analyze_trend(data_file=loaded_file, variable_of_interest=variable_of_interest)  # Trend analizi yapılıyor.
            st.success(trend_response)  # Trend analizi sonucu başarı mesajı olarak gösteriliyor.
            return
        
        # Değişken belirlendiğinde veya inceleme butonuna basıldığında fonksiyon çalıştırılıyor.
        if variable_of_interest or examine_btn:
            explore_variable(data_file=loaded_file, variable_of_interest=variable_of_interest)
        
        # Kullanıcıdan veri kümesi ile ilgili soru sormasını isteyen metin girişi.
        free_question = st.text_input(label="Veri Kümesiyle İlgili Ne Bilmek İstersiniz?")
        ask_btn = st.button(label="Sor")  # Soru sorma butonu
        st.divider()  # Görsel bölücü

        # Soruyu yanıtlayan fonksiyon tanımlanıyor ve cache'leniyor.
        @st.cache_data
        def answer_question(data_file, question):
            data_file.seek(0)  # Dosya başına dönülüyor.
            AI_Response = datahelper.ask_question(data_file=loaded_file, question=free_question)  # Soruyu yanıtlamak için datahelper kullanılıyor.
            st.success(AI_Response)  # Yanıt başarı mesajı olarak gösteriliyor.
            return
        
        # Soru belirlendiğinde veya soru sorma butonuna basıldığında fonksiyon çalıştırılıyor.
        if free_question or ask_btn:
            answer_question(data_file=loaded_file, question=free_question)
