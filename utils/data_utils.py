# encoding = 'utf-8'

import re
import os
import emoji
import time
import logging
import csv

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_path):
    os.makedirs(log_path)

class Cleaner():
    def __init__(self):
        log_file = os.path.join(log_path, 'Cleaner.log')
        logging.basicConfig(filename=log_file, level=logging.INFO,
            filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%d-%m %H:%M:%S')
        logging.info('---------------------New Cleaner---------------------')
        
    def rmWhitespace(self, text):
        pattern = re.compile(r'\s+')
        return pattern.sub(' ', text).strip()
    
    def rmURL(self, text):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return pattern.sub('', text)

    def rmHTML(self, text):
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', text)
    
    def rmEmoji(self, text):
        return emoji.replace_emoji(text, '')
    
    def rmTags(self, text):
        pattern = re.compile(r'#\S+#')
        return pattern.sub('', text)
    
    def rmXHSemoji(self, text):
        pattern = re.compile(r'\[.*?\]')
        return pattern.sub('', text)
    
    def rmAt(self, text):
        pattern = re.compile(r'@\S+')
        return pattern.sub('', text)
    
    def clean(self, text, rm_url=True, rm_whitespace=True, rm_html=True, rm_emoji=True, rm_tags=True, rm_xhs_emoji=True, rm_at=True):
        if rm_url:
            text = self.rmURL(text)
        if rm_whitespace:
            text = self.rmWhitespace(text)
        if rm_html:
            text = self.rmHTML(text)
        if rm_emoji:
            text = self.rmEmoji(text)
        if rm_tags:
            text = self.rmTags(text)
        if rm_xhs_emoji:
            text = self.rmXHSemoji(text)
        if rm_at:
            text = self.rmAt(text)
        return text
    
    def main(self, input_file, output_file, **kwargs):
        """
        input file: should be a txt or csv file. for txt, each line is a doc to be cleaned; for csv, each row is a doc to be cleaned.
        output file: should be a txt file, each line is a cleaned doc.
        """
        if not os.path.exists(input_file):
            logging.error('File not found')
            raise ValueError('input_file {} does not exist, should be a data file which need to be cleaned.'.format(input_file))
        if os.path.exists(output_file):
            logging.error('File already exists')
            raise ValueError('output_file {} has existed, should be a new file.'.format(output_file))
        
        logging.info('Start cleaning for file: {}'.format(input_file))

        rm_url = kwargs.get('rm_url', True)
        rm_whitespace = kwargs.get('rm_whitespace', True)
        rm_html = kwargs.get('rm_html', True)
        rm_emoji = kwargs.get('rm_emoji', True)
        rm_tags = kwargs.get('rm_tags', True)
        rm_xhs_emoji = kwargs.get('rm_xhs_emoji', True)
        rm_at = kwargs.get('rm_at', True)
        if input_file.endswith('.csv'):
            with open(input_file, 'r') as inf:
                lines = csv.reader(inf)
                with open(output_file, 'w') as outf:
                    if rm_url:
                        logging.info('Remove url for {}'.format(input_file))
                    if rm_whitespace:
                        logging.info('Remove whitespace for {}'.format(input_file))
                    if rm_html:
                        logging.info('Remove html for {}'.format(input_file))
                    if rm_emoji:
                        logging.info('Remove emoji for {}'.format(input_file))
                    if rm_tags:
                        logging.info('Remove tags for {}'.format(input_file))
                    if rm_xhs_emoji:
                        logging.info('Remove xhs emoji for {}'.format(input_file))
                    if rm_at:
                        logging.info('Remove at for {}'.format(input_file))
                    for line in lines:
                        line = line[0]
                        cleaned_line = self.clean(line, rm_url=rm_url, rm_whitespace=rm_whitespace, rm_html=rm_html, rm_emoji=rm_emoji, rm_tags=rm_tags, rm_xhs_emoji=rm_xhs_emoji, rm_at=rm_at)
                        outf.write(cleaned_line + '\n')
            logging.info('Finish cleaning, output at: {}'.format(output_file))
            print('Finish cleaning!')
        elif input_file.endswith('.txt'):
            with open(input_file, 'r') as inf:
                lines = inf.readlines()
                with open(output_file, 'w') as outf:
                    if rm_url:
                        logging.info('Remove url for {}'.format(input_file))
                    if rm_whitespace:
                        logging.info('Remove whitespace for {}'.format(input_file))
                    if rm_html:
                        logging.info('Remove html for {}'.format(input_file))
                    if rm_emoji:
                        logging.info('Remove emoji for {}'.format(input_file))
                    if rm_tags:
                        logging.info('Remove tags for {}'.format(input_file))
                    if rm_xhs_emoji:
                        logging.info('Remove xhs emoji for {}'.format(input_file))
                    if rm_at:
                        logging.info('Remove at for {}'.format(input_file))
                    for line in lines:
                        cleaned_line = self.clean(line, rm_url=rm_url, rm_whitespace=rm_whitespace, rm_html=rm_html, rm_emoji=rm_emoji, rm_tags=rm_tags, rm_xhs_emoji=rm_xhs_emoji, rm_at=rm_at)
                        outf.write(cleaned_line + '\n')
            logging.info('Finish cleaning, output at: {}'.format(output_file))
            print('Finish cleaning!')
            
class LengthProcessor():
    def __init__(self):
        log_file = os.path.join(log_path, 'LengthProcessor.log')
        logging.basicConfig(filename=log_file, level=logging.INFO,
            filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%d-%m %H:%M:%S')
        logging.info('---------------------New LengthProcessor---------------------')

    def cutting(self, doc, size = 510, where='head', portion=None):
        doc = doc.replace('\n', '')
        try:
            if where == 'head':
                return doc[:size]
            elif where == 'tail':
                return doc[-size:]
            elif where == 'head+tail':
                head_size = int(size * portion)
                tail_size = size - head_size
                return doc[:head_size] + doc[-tail_size:]
            return doc
        except:
            raise ValueError('metric should be head, tail or head+tail')
    
    def pooling(self, doc):
        pass

    def rule_based(self, doc, size = 510):
        rule_dict = {   # 可视实际情况添加规则
        'delete_kw': ['举个手', '举手', '宝子们', '评论区', '留言', '留个言',
                      '一起交流讨论','期待','拭目以待','那么','大家','评论','欢迎', '希望',
                      '分享','呢','喜欢','买','你','小伙伴','你','知道','想法','伙伴','吗',
                      '感觉','看看','看','说','好','不','有','的','是','吧','呀','啊','嘛',
                      '怎么']
    }
        sentences = re.split(r'([。？！～])', doc)
        sentences = [sentences[i] + sentences[i + 1] for i in range(0, len(sentences) - 1, 2)]
        filtered_sentences = []
        indicator = 0
        for sentence in sentences:
            for rule in rule_dict['delete_kw']:
                if rule in sentence:
                    indicator += 1
            if indicator < len(sentence) * 0.2:
                filtered_sentences.append(sentence)
            indicator = 0
        if len(filtered_sentences) > size:
            return ''.join(filtered_sentences[:size])
        else:
            return ''.join(filtered_sentences)
        
    def process_doc(self, doc, metric='cutting', **kwargs):
        # check length
        if len(doc) > 512:
            if metric == 'cutting':
                where = kwargs.get('where', 'head')
                portion = kwargs.get('portion', None)
                new_doc = self.cutting(doc, where, portion)
            elif metric == 'pooling':
                new_doc = self.pooling(doc)
            elif metric == 'rule_based':
                new_doc = self.rule_based(doc)
            return new_doc
        else:
            return doc

    def main(self, input_file, output_file, metric, **kwargs):
        if not os.path.exists(input_file):
            logging.error('File not found')
            raise ValueError('input_file {} does not exist, should be a data file which need to be cleaned.'.format(input_file))
        if os.path.exists(output_file):
            logging.error('File already exists')
            raise ValueError('output_file {} has existed, should be a new file.'.format(output_file))
        
        logging.info('Start processing for file: {}'.format(input_file))
        with open(input_file, 'r') as inf:
            lines = inf.readlines()
            with open(output_file, 'w') as outf:
                for line in lines:
                    new_line = self.process_doc(line, metric, **kwargs)
                    if new_line != '':
                        outf.write(new_line + '\n')
        logging.info('Finish processing, output at: {}'.format(output_file))
        print('Finish processing!')
    