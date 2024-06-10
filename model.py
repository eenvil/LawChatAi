from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
from peft import PeftModel
import torch 


modle_path = "my_model"
model_name = "taide/TAIDE-LX-7B-Chat"

class TAIDE(torch.nn.Module):
    
    def __init__(self):
        super(TAIDE, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
        # self.access_token = "your_access_token_here_for_huggingface"
        self.base_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_4bit=True,#for low memory usaged may cause unexpected error
            device_map ="auto",
            )
        self.model = PeftModel.from_pretrained(self.base_model,modle_path)
        self.model = self.model.merge_and_unload()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        

    def forward(self, input_text):
        input_text = f"<s>[INST] {input_text} [/INST]"
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids
        output = self.model.generate(input_ids, max_length=1024, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(output[0])
        return response

if __name__ == "__main__":
    model = TAIDE()
    print(model("某甲公然陳列色情錄影帶，這種行為的法律後果是什麼？"))
    
