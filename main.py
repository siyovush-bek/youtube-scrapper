from utils import extract_and_save

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Video Data Extractor")
    parser.add_argument("filename", help="Input file name")
    args = parser.parse_args()
    with open(args.filename, newline='') as f:
           for line in f:
               splitted = line.split()
               print(f'Processing query: {splitted[0]}')
               extract_and_save(
                    splitted[0].replace('+', ' '),
                    splitted[1].replace('.csv', '')
                )
               print(f'Done processing url: {splitted[0]}')
               print(f'Saved to {splitted[1]}.csv')
