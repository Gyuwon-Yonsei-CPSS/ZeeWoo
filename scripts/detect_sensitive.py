import spacy
import os

# spaCy NER 모델 로드 (한국어 NER 모델)
nlp = spacy.load("ko_core_news_sm")

# 경로 설정
preprocessed_dir = 'data/preprocessed_texts'
sensitive_data_dir = 'data/sensitive_data_results'

if not os.path.exists(sensitive_data_dir):
    os.makedirs(sensitive_data_dir)

# 민감 정보 탐지 함수
def detect_sensitive_info(text):
    doc = nlp(text)
    sensitive_data = []
    
    # NER로 탐지된 민감 정보 (PERSON: 이름, ORG: 기관명, DATE: 날짜 등)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'DATE', 'CARDINAL']:  
            sensitive_data.append((ent.text, ent.label_))
    
    return sensitive_data

# 전처리된 텍스트에서 민감 정보 탐지
for preprocessed_file in os.listdir(preprocessed_dir):
    with open(os.path.join(preprocessed_dir, preprocessed_file), 'r', encoding='utf-8') as f:
        text = f.read()
        sensitive_info = detect_sensitive_info(text)
        
        # 탐지 결과 저장
        output_file_path = os.path.join(sensitive_data_dir, f"{preprocessed_file}_sensitive.txt")
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            for data in sensitive_info:
                f_out.write(f"{data[0]} ({data[1]})\n")

        print(f"{preprocessed_file}에서 민감 정보 탐지 완료.")
