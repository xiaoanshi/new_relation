import models
import nrekit
import sys
from torch import optim
from nrekit.data_loader import JSONFileDataLoader

max_length = 100
train_data_loader = JSONFileDataLoader('./data/tacred_train.json', './data/glove.6B.50d.json', max_length=max_length)
val_data_loader = JSONFileDataLoader('./data/tacred_val.json', './data/glove.6B.50d.json', max_length=max_length, rel2id=train_data_loader.rel2id)

framework = nrekit.framework.SuperviseFramework(train_data_loader, val_data_loader)
sentence_encoder = nrekit.sentence_encoder.CNNSentenceEncoder(train_data_loader.word_vec_mat, max_length)
model = models.cnn_snowball.Snowball(sentence_encoder, base_class=train_data_loader.rel_tot, siamese_model=None, hidden_size=230)
model_name = 'cnn_encoder_on_tacred'
model.NA_label = 13
framework.train_encoder(model, model_name, batch_size=50, train_iter=120000, lr_step_size=60000)
