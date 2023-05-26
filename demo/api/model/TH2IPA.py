import os
dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)

import numpy as np
import json
from keras_preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import load_model
import re

path = {'idx2IPA': '../dict/idx2IPA.json', 
        'TH_char2idx': '../dict/TH_char2idx.json', 
        'model': './self_attn'}

class TH2IPA(object):
    def __init__(self, model_path=path['model']):
        self.model = load_model(model_path)
        with open(path['idx2IPA'], encoding="utf8") as f:
            self.idx2IPA = json.loads(f.read())
        with open(path['TH_char2idx'], encoding="utf8") as f:
            self.TH_char2idx = json.loads(f.read())
        # with open(path['IPA2idx'], encoding="utf8") as f:
        #     self.IPA2idx = json.loads(f.read())
        # with open(path['TH_idx2char'], encoding="utf8") as f:
        #     self.TH_idx2char = json.loads(f.read())


    # def convertModelInput2Char(self, input_x):
    #     input_name = [''.join(list(map(lambda x: self.TH_idx2char[str(x)] if x!=0 else "", idx_sequence))) for idx_sequence in np.argmax(input_x, axis = -1)]
    #     return input_name
    
    def convertChar2ModelInput(self, char_list, maxlen_x, n_vocab, pad='post'):
        x = [list(map(lambda x: self.TH_char2idx[x] if x in self.TH_char2idx.keys() else 1 , word)) for word in char_list]
        x_pad = pad_sequences(x, maxlen_x, padding=pad)
        x_categorical = to_categorical(x_pad, n_vocab)
        return x_categorical
    

    def convertPred2IPA(self, y_pred):
        output = []
        '''convert the array returned from model to list of IPA.'''
        prediction = np.swapaxes(y_pred, 0, 1)
        prediction = np.argmax(prediction, axis = -1)
        for idx in range(len(prediction)):
            output.append("".join([self.idx2IPA[str(i)] for i in prediction[idx] if i!=0]))
        return output

    # def convertIPA2ModelOutput(self, IPA, maxlen_y, n_vocab, pad='post'):
    #     y = [list(map(lambda x: self.IPA2idx[x] if x in self.IPA2idx.keys() else 1 , phone)) for phone in IPA]
    #     y_pad = pad_sequences(y, maxlen_y, padding='post')
    #     y_categorical = to_categorical(y_pad, n_vocab)
    #     return y_categorical
    
    def predictFromPronunciation(self, pron, display=False, n_decode=128):
        x_test = self.convertChar2ModelInput(pron, self.model.input_shape[0][1], self.model.input_shape[0][2])
        s0 = np.zeros((len(pron), n_decode)) 
        c0 = np.zeros((len(pron), n_decode))
        y_pred = self.model.predict([x_test , s0, c0])
        if display:
            IPA = self.convertPred2IPA(y_pred)
            for i in range(len(IPA)):
                print("{} : {}" .format(pron[i], IPA[i]))

        return y_pred
    
    def __call__(self, list_pron):
        y_pred = self.predictFromPronunciation(list_pron)
        y_pred_ipa = self.convertPred2IPA(y_pred)
        y_pred_ipa = [re.sub('[\/]', '', i) for i in y_pred_ipa]
        return y_pred_ipa
