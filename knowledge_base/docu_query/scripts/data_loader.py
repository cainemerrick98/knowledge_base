import csv, json
import text_preprocessing


def csv_to_json_data():

    data = []

    with open(r'C:\Users\cmerrick005\OneDrive - pwc\Documents\knowledge_base\knowledge_base\docu_query\test_data\fixture_data.csv',
              'r', encoding='utf-8') as document_csv:
          
          csv_reader = csv.DictReader(document_csv)

          for i, row in enumerate(csv_reader):
               
               # match the preprocessing in the upload api
               row['content'] = text_preprocessing.preprocess_text(row['content'])

               document = {
                    'model':'docu_query.Document',
                    'pk':i+1,
                    'fields':row,
               }

               data.append(document)

          with open(r'C:\Users\cmerrick005\OneDrive - pwc\Documents\knowledge_base\knowledge_base\docu_query\fixtures\test_docs.json',
                    'w') as jsonf:
               
               jsonf.write(json.dumps(data))

    

if __name__ == "__main__":
    csv_to_json_data()
