# Data Explorer 🤖

`Data Explorer` uygulaması, CSV dosyalarını yükleyip, doğal dil kullanarak bu veriler üzerinde analizler yapabileceğiniz bir Streamlit uygulamasıdır. Bu uygulama, `pandas` kütüphanesi ve `langchain` tabanlı dil modelleri ile entegre çalışarak veri keşfi sürecinizi hızlandırır.

## Özellikler

- **Veri Yükleme:** Kullanıcı, kenar çubuğundan bir CSV dosyasını yükleyebilir.
- **Veri Özeti:** Yüklenen verinin ilk 5 satırını ve temel metrikleri görme imkanı.
- **Eksik ve Mükerrer Veri Tespiti:** Veri kümesinde eksik veya mükerrer veri olup olmadığını tespit eder.
- **Değişken Analizi:** Kullanıcının belirlediği bir değişkenin trend analizi ve grafiği.
- **Doğal Dil Soruları:** Kullanıcı, veri kümesiyle ilgili doğal dilde sorular sorabilir ve yanıt alabilir.

## Kurulum

Bu uygulamayı çalıştırmak için aşağıdaki adımları izleyin:

1. **Gereksinimleri Yükleyin:**

   ```bash
   pip install -r requirements.txt

2. **Çevresel Değişkenleri Ayarlayın:**
.env dosyası oluşturup, aşağıdaki API anahtarlarını ekleyin:


OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key



3. **Uygulamayı Çalıştırın:**
   
```bash
streamlit run app.py


## Kullanım

### 1. Veri Yükleme:

- Uygulama açıldığında, kenar çubuğundan bir CSV dosyası yükleyin.
- Yükleme butonuna basarak veriyi uygulamaya yükleyin.

### 2. Veri Özeti:

- **Veri Özeti** bölümünde, yüklediğiniz veriyle ilgili özet bilgileri inceleyebilirsiniz.
- Bu bölümde, verinin ilk 5 satırını, sütun açıklamalarını, eksik ve mükerrer veri durumunu ve temel metrikleri görebilirsiniz.

### 3. Veriyle Etkileşim:

- Bir değişken adı girerek, bu değişkenin trend analizini yapabilir ve sonuçları bar grafiği olarak görüntüleyebilirsiniz.
- Ayrıca, veri kümesiyle ilgili sorularınızı doğal dilde sorabilir ve yapay zeka destekli yanıtlar alabilirsiniz.



## Dosya Yapısı

- **`app.py`**: Streamlit uygulamasının ana dosyası. Uygulamanın kullanıcı arayüzü ve ana işleyişini içerir.
- **`datahelper.py`**: Veri işleme ve analiz fonksiyonlarının bulunduğu yardımcı dosya. Bu dosya, Pandas DataFrame'leri üzerinde çalışan fonksiyonlar içerir.
- **`requirements.txt`**: Uygulamanın çalışması için gerekli Python kütüphanelerini içeren dosya. Gereksinimlerinizi bu dosya üzerinden yükleyebilirsiniz.
- **`.env`**: API anahtarlarının saklandığı çevresel değişken dosyası. Bu dosya gizli tutulmalıdır ve kod deposunda paylaşılmamalıdır.
