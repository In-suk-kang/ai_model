import re
from urllib.parse import urlparse
#외부 모델 사용하기 위한 라이브러리: transformers&torch
from transformers import BertModel, BertTokenizer
import torch
import numpy as np
import pickle

class ai_model_class():
    def __init__(self):
        self.bertmodel = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.feature_funcs = [len, self.character_lengths, self.has_shortening_ser, self.abnormal, self.have_ip]
        #path = ' '# 모델 피클이 있을 주소
        self.return_types = {
        0:('benign', 0.96),
        1:('defacement', 0.96),
        2:('phishing', 0.84),
        3:('malware', 0.94)}

    # Define a function to extract features for each transaction
    def extract_features(self, text):
        # Tokenize the text
        input_ids = self.tokenizer(text, return_tensors="pt", add_special_tokens=True)['input_ids']
        # Get the hidden states for each token
        with torch.no_grad():
            outputs = self.bertmodel(input_ids)
            hidden_states = outputs[2]
        # Concatenate the last 4 hidden states
        token_vecs = []
        for layer in range(-4, 0):
            token_vecs.append(hidden_states[layer][0])
        # Calculate the mean of the last 4 hidden states
        features = []
        for token in token_vecs:
            features.append(torch.mean(token, dim=0))
        # Return the features as a tensor
        return torch.stack(features)

    #shortening service
    def has_shortening_ser(self, url):
        pattern = re.compile(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                            r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                            r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                            r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                            r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                            r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                            r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                            r'tr\.im|link\.zip\.net')
        match = pattern.search(url)
        return int(bool(match))

    def character_lengths(self, url):
        #character lengths
        num_letters = sum(char.isalpha() for char in url)
        num_digits = sum(char.isdigit() for char in url)
        special_chars = "!@#$%^&*()_+-=[]{};:,.<>/?`~|"
        num_special_chars = sum(char in special_chars for char in url)
        return [num_letters, num_digits, num_special_chars]

    #urls where hostname = domain
    def abnormal(self, url):
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if hostname:
            hostname = str(hostname)
            match = re.search(hostname, url)
            if match:
                return 1
        return 0

    #urls with IP
    def have_ip(self, url):
        pattern = r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.' \
                r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|' \
                r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.' \
                r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|' \
                r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)' \
                r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|' \
                r'([0-9]+(?:\.[0-9]+){3}:[0-9]+)|' \
                r'((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)'

        match = re.search(pattern, url)
        if match:
            return 1
        else:
            return 0

    #불필요한 수식어 제거
    def remove_useless(self, url):
        url = re.sub('www.', '', url)
        url = re.sub('http://', '', url)
        url = re.sub('https://', '', url)
        url = re.sub('.html', '', url)
        url = re.sub('.htm', '', url)
        return url

    #primary url 구하기
    def primary(self, url):
        reg = re.compile('^(.*?)\/')
        temp = reg.findall(url)
        primary_url = '0'
        if temp:
            primary_url = temp
        else:
            primary_url = url
        return primary_url

    def preprocessing(self, url):
        url = self.remove_useless(url)
        primary_url = self.primary(url)

        features = []
        for func in self.feature_funcs:
            try:
                features.extend(func(url))
            except:
                features.append(func(url))
        nonbert_features = np.array(features).reshape(1,-1)

        if len(url) > 511:
            bert_features = self.extract_features(primary_url).numpy().reshape(1,-1)
        else:
            bert_features = self.extract_features(url).numpy().reshape(1,-1)
        return np.hstack((bert_features, nonbert_features))

    def predict_results(self, url):
        model_bert = pickle.load(open('model_bert_logreg.pkl', 'rb'))
        return self.return_types[model_bert.predict(self.preprocessing(url))[0]]
