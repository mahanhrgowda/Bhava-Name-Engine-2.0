import pandas as pd
from bhava_vector_tagger import get_bhava_vector, get_dominant_bhava
from utils import format_name

def process_batch_csv(file):
    try:
        df = pd.read_csv(file)
        if 'Name' not in df.columns:
            return None, "CSV must contain a 'Name' column."
        df['Name'] = df['Name'].apply(format_name)
        df['Bhāva Vector'] = df['Name'].apply(get_bhava_vector)
        df['Dominant Bhāva'] = df['Bhāva Vector'].apply(get_dominant_bhava)
        return df, None
    except Exception as e:
        return None, str(e)
