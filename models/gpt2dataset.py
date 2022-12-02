from torch.utils.data import Dataset
import torch

class GPT2Dataset(Dataset):

  def __init__(self, df, tokenizer, gpt2_type="gpt2", max_length=768):

    self.tokenizer = tokenizer
    self.input_ids = []
    self.attn_masks = []

    for index, row in df.iterrows():

      encodings_dict = tokenizer('<|startoftext|>'+ row['input'] + '<|sep|>' + \
                                 row['sequence'] + '<|endoftext|>',
                                 truncation=True, max_length=max_length, 
                                 padding="max_length")

      self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
      self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
    
  def __len__(self):
    return len(self.input_ids)

  def __getitem__(self, idx):
    return self.input_ids[idx], self.attn_masks[idx] 