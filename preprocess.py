from utils import data_utils

if __name__ == '__main__':
    input_file = 'data/raw_text.csv'
    output_file = 'data/cleaned_text.txt'
    
    cleaner = data_utils.Cleaner()
    cleaner.main(input_file, output_file, rm_url=True, rm_whitespace=True, rm_html=True, rm_emoji=True, rm_tags=True, rm_xhs_emoji=True, rm_at=True)

    input_file = output_file
    output_file = 'data/processed_text.txt'

    lengthprocessor = data_utils.LengthProcessor()
    # lengthprocessor.main(input_file, output_file, metric='rule_based', size=510)
    lengthprocessor.main(input_file, output_file, metric='cutting', size=510, where='head')