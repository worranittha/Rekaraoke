from model import sefr_cut
from model.TH2IPA import TH2IPA
from model.IPA2ENG import IPA_matching
from neuspell import BertChecker
import re

# initial variables
th2ipa = TH2IPA()
checker = BertChecker()

def init_model():
    global checker
    sefr_cut.SEFR_CUT.load_model(engine='model')
    checker.from_pretrained()
    return 

def predict(th_sent):
    global checker, th2ipa
    print('input:', th_sent)
    token_list = sefr_cut.tokenize(th_sent, k=80)[0]
    print('tokenize:', token_list)
    ipa_list = th2ipa(token_list)
    print('th2ipa:', ipa_list)
    eng_sent = ' '.join([IPA_matching(i)[0] for i in ipa_list]) 
    print('ipa2eng:', eng_sent)
    correct_sent = checker.correct(eng_sent)
    correct_sent = re.sub(' \' ', '\'', correct_sent)
    print('en_lyric:', correct_sent)
    return correct_sent

# if __name__ == '__main__':
#     init_model()
#     print(predict('ฮันนี่ไอแคนซีเดอะสตา'))

