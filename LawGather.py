import json

# Function to parse the text file and extract question-answer pairs
def parse_qa(text_file):
    qa_list = []
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        current_q = None
        for line in lines:
            if line.startswith('Q: '):
                if current_q:
                    qa_list.append(current_q)
                current_q = {'text': f"<s>[INST] {line.strip()[3:]} [/INST]"}  # Remove 'Q: '
            elif line.startswith('A: '):
                if current_q:
                    current_q['text'] = current_q['text'] + f"{line.strip()[3:]}</s>"  # Remove 'A: '

        # Append the last Q&A pair
        if current_q:
            qa_list.append(current_q)

    return qa_list

# Function to write the Q&A pairs to a JSON file
def write_to_json(qa_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump({"data": qa_list}, file, ensure_ascii=False, indent=2)
import json
from sklearn.model_selection import train_test_split

# Load your JSON data
def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)['data']
    return data

# Split data into train and test sets
def split_data(data, test_size=0.2):
    train_set, test_set = train_test_split(data, test_size=test_size, random_state=42)
    return train_set, test_set

# Save the split data back to JSON format
def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Main function to process the splitting
def main():
    json_file = 'output.json'  # Path to your JSON file
    data = load_data(json_file)
    train_set, test_set = split_data(data)
    
    # Save the train and test sets to new JSON files
    save_to_json(train_set, 'train_data.json')
    save_to_json(test_set, 'test_data.json')
    
    print("Train and test datasets have been created and saved successfully.")

# Run the script
if __name__ == "__main__":
    qa = parse_qa("data.txt")
    write_to_json(qa, "output.json")
    main()


