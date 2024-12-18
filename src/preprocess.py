from ..utils import data_utils as utils
import os

if __name__ == '__main__':
    input_file = './data/raw_text.csv'
    output_file = './data/cleaned_text.txt'
    
    cleaner = utils.Cleaner()
    cleaner.main(input_file, output_file, rm_url=True, rm_whitespace=True, rm_html=True, rm_emoji=True, rm_tags=True, rm_xhs_emoji=True, rm_at=True)