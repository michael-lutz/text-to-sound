from midi_converter import Converter
from transformers import GPT2LMHeadModel,  GPT2Tokenizer, GPT2Config, GPT2LMHeadModel
from transformers import AdamW, get_linear_schedule_with_warmup
import torch

device = torch.device("cuda")
output_dir = '../model_save/'

model = GPT2LMHeadModel.from_pretrained(output_dir)
tokenizer = GPT2Tokenizer.from_pretrained(output_dir)
model.to(device)

model.eval()

while True:
    prompt = input('Prompt: ')
    gen_prompt = "<|startoftext|> " + prompt

    generated = torch.tensor(tokenizer.encode(gen_prompt)).unsqueeze(0)
    generated = generated.to(device)

    sample_output = model.generate(
                                generated, 
                                do_sample=True,   
                                top_k=50, 
                                max_length = 300,
                                top_p=0.95, 
                                num_return_sequences=1
                                )

    result = tokenizer.decode(sample_output[0], skip_special_tokens=True)


    a = Converter(prompt, result)
    a.write()







prompt = "<|startoftext|> A classical song in the style of Kanye West"

generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
generated = generated.to(device)

print(generated)

sample_outputs = model.generate(
                                generated, 
                                #bos_token_id=random.randint(1,30000),
                                do_sample=True,   
                                top_k=50, 
                                max_length = 300,
                                top_p=0.95, 
                                num_return_sequences=3
                                )

for i, sample_output in enumerate(sample_outputs):
  print("{}: {}\n\n".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))