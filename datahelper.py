import pandas as pd
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    create_pandas_dataframe_agent,
) #pandas kütüphanesini kullanabilmek için
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os 
from dotenv import load_dotenv

# Çevresel değişkenleri yüklemek için dotenv dosyasını kullan
load_dotenv()

# Çevresel değişkenlerden API anahtarlarını al
my_key_openai = os.getenv("OPENAI_API_KEY")
my_key_anthropic = os.getenv("ANTHROPIC_API_KEY")

# OpenAI GPT-4 modelini seç
llm_gpt = ChatOpenAI(api_key=my_key_openai, model="gpt-4-turbo-preview",temperature = 0)

# Anthropic Claude-3 Opus modelini seç
llm_claude_opus = ChatAnthropic(anthropic_api_key=my_key_anthropic, model_name="claude-3-opus-20240229", temperature=0)

# Anthropic Claude-3 Haiku modelini seç
llm_claude_haiku = ChatAnthropic(anthropic_api_key=my_key_anthropic, model_name="claude-3-haiku-20240307", temperature=0)

# Seçili dil modelini belirle
selected_llm = llm_gpt

# CSV dosyasını özetlemek için fonksiyon
def summarize_csv(data_file):
    # CSV dosyasını pandas DataFrame olarak yükle
    df = pd.read_csv(data_file, low_memory=False) #tüm belleği kullansın diye low memory false

    # Pandas DataFrame ajanı oluştur
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors":"True"},allow_dangerous_code=True)
    #verbose =true yapılan tüm işlemleri takip etmek için yapılır
    #handling_parsing_errors :True diyerek bölme işlemlerinde anlamdırma hataları olduğunda tekrar bu işlemi yap

    # Veri özetini tutacak sözlük
    data_summary = {}

    # İlk 5 satırı özet verisi olarak al
    data_summary["initial_data_sample"] = df.head()

    # Sütun açıklamalarını almak için ajanı kullan
    data_summary["column_descriptions"] = pandas_agent.run("Verideki sütunları içeren bir tablo yap. Tabloda sütunların adları ve yanlarında kısaca içerdikleri bilgiye dair Türkçe bir açıklama yer alsın. Bunu bir tablo olarak ver.")

    # Eksik veri kontrolü
    data_summary["missing_values"] = pandas_agent.run("Bu veri kümesinde eksik veri var mı? Varsa kaç adet var? Yanıtını 'Bu veri kümesinde X adet hücrede eksik veri var' şeklinde ver.")

    # Mükerrer veri kontrolü
    data_summary["duplicate_values"] = pandas_agent.run("Bu veri kümesinde mükerrer veri var mı? Varsa kaç adet var? Yanıtını 'Bu veri kümesinde X adet hücrede mükerrer veri var' şeklinde ver.")

    # Temel metrikleri al
    data_summary["essential_metrics"] = df.describe()

    # Veri özetini döndür
    return data_summary

# DataFrame'i yüklemek için fonksiyon
def get_dataframe(data_file):
    # CSV dosyasını pandas DataFrame olarak yükle
    df = pd.read_csv(data_file, low_memory=False)

    # DataFrame'i döndür
    return df

# Belirli bir değişkenin trend analizini yapmak için fonksiyon
def analyze_trend(data_file, variable_of_interest):
    # CSV dosyasını pandas DataFrame olarak yükle
    df = pd.read_csv(data_file, low_memory=False)

    # Pandas DataFrame ajanı oluştur
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors":"True"}, allow_dangerous_code=True)

    # Değişkenin trend analizini yapmak için ajanı kullan
    trend_response = pandas_agent.run(f"Veri kümesi içindeki şu değişkenin değişim trendini kısaca yorumla: {variable_of_interest} Yorumlamayı reddetme. Verideki satırlar geçmişten günümüze tarih bazlı olduğu için, verideki satırlara bakarak yorumda bulunabilirsin. Yanıtın Türkçe olarak ver.")

    # Trend analizini döndür
    return trend_response

# Kullanıcının sorusunu yanıtlamak için fonksiyon
def ask_question(data_file, question):
    # CSV dosyasını pandas DataFrame olarak yükle
    df = pd.read_csv(data_file, low_memory=False)

    # Pandas DataFrame ajanı oluştur
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors":"True"}, allow_dangerous_code=True)

    # Kullanıcının sorusunu yanıtlamak için ajanı kullan
    AI_Response = pandas_agent.run(f"{question} Bu soruyu Türkçe yanıtla.")

    # Yanıtı döndür
    return AI_Response
