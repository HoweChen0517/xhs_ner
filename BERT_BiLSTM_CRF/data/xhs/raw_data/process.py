import os
import re
import json

def split_train_test_dev(input_path, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    train_path = os.path.join(save_path, "train.json")
    test_path = os.path.join(save_path, "test.json")
    dev_path = os.path.join(save_path, "dev.json")
    with open(input_path, 'r') as fp:
        file = json.load(fp)
    train = file[:int(0.8*len(file))]
    test = file[int(0.8*len(file)):int(0.9*len(file))]
    dev = file[int(0.9*len(file)):]
    with open(train_path, 'w') as fp:
        json.dump(train, fp, ensure_ascii=False, indent=4)
    with open(test_path, 'w') as fp:
        json.dump(test, fp, ensure_ascii=False, indent=4)
    with open(dev_path, 'w') as fp:
        json.dump(dev, fp, ensure_ascii=False, indent=4)

def preprocess(input_path, save_path, mode):
    with open(input_path, 'r') as fp:   # check path first
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        data_path = os.path.join(save_path, mode + ".json")
        labels = set()
        result = []
        tmp = {}
        tmp['id'] = 0
        tmp['text'] = ''
        tmp['labels'] = []
        file = json.load(fp)
    
    for dic in file:
        annotations = dic['annotations']
        for annotation in annotations:
            for rslt in annotation['result']:
                for label in rslt['value']['labels']:
                    labels.add(label)

    i = 0
    for dic in file:
        tmp['text'] = dic['data']['text']
        annotations = dic['annotations']
        cnt = 0
        for annotation in annotations:
            for rslt in annotation['result']:
                for l in rslt['value']['labels']:
                    ltmp = []
                    ltmp.append('T{}'.format(cnt))
                    ltmp.append(l)
                    ltmp.append(rslt['value']['start'])
                    ltmp.append(rslt['value']['end'])
                    ltmp.append(rslt['value']['text'])
                    tmp['labels'].append(ltmp)
                    cnt += 1
        tmp['id'] = i
        result.append(tmp)
        tmp = {}
        tmp['id'] = 0
        tmp['text'] = ''
        tmp['labels'] = []
        i += 1

    with open(data_path, 'w') as fp:
        json.dump(result, fp, ensure_ascii=False, indent=4)
    if mode == "train":
        label_path = os.path.join(save_path, "labels.json")
        with open(label_path, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(list(labels), ensure_ascii=False))

if __name__ == '__main__':
    split_train_test_dev('labeled_raw.json', "../raw_data")
    preprocess('train.json', "../mid_data", "train")
    preprocess('test.json', "../mid_data", "test")
    preprocess('dev.json', "../mid_data", "dev")

    labels_path = os.path.join('../mid_data/labels.json')
    with open(labels_path, 'r') as fp:
        labels = json.load(fp)

    tmp_labels = []
    tmp_labels.append('O')
    for label in labels:
        tmp_labels.append('B-' + label)
        tmp_labels.append('I-' + label)
        tmp_labels.append('E-' + label)
        tmp_labels.append('S-' + label)

    label2id = {}
    for k,v in enumerate(tmp_labels):
        label2id[v] = k
    path  = '../mid_data/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "nor_ent2id.json"),'w') as fp:
        fp.write(json.dumps(label2id, ensure_ascii=False))