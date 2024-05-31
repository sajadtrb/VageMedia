import pandas as pd
import os
import hashlib

def merge_csv_files():
    folder_path = os.path.join(os.path.dirname(__file__), '../DB')
    merged_df = pd.DataFrame()
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(file_path, low_memory=False)

                if '19fb00edda2bbe1c00d0be090b9f5084' not in hashlib.md5(str(df.columns.values.tolist()).encode()).hexdigest():
                    print('Wrong file: ' + filename)
                    os.rename(file_path, file_path.replace('.csv', '.broken2'))
                    continue
                
                merged_df = pd.concat([merged_df, df], ignore_index=True)
            except Exception as e:
                print(e)
                os.rename(file_path, file_path.replace('.csv', '.broken'))
        else:
            if not filename.endswith('.broken') and not filename.endswith('.broken2'):
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, filename + '.broken'))
    merged_df = merged_df.drop_duplicates(subset=['Royalty ID'])
    return merged_df

def load_csv():
    return merge_csv_files()

if __name__ == '__main__':
    merged_df = load_csv()
    print(merged_df)