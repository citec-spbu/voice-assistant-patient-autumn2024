import torch
import pandas as pd
from transformers import BertTokenizer, BertForTokenClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split

# Данные для обучения
data = pd.read_csv("datetime_dataset.csv")

class DateTimeDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text, label = self.data[idx]
        inputs = self.tokenizer(text, padding="max_length", max_length=self.max_length, truncation=True, return_tensors="pt")
        target = self.tokenizer(label, padding="max_length", max_length=self.max_length, truncation=True, return_tensors="pt")
        return inputs.input_ids[0], inputs.attention_mask[0], target.input_ids[0]
    
# Инициализация токенизатора и модели
tokenizer = BertTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = BertForTokenClassification.from_pretrained("DeepPavlov/rubert-base-cased", num_labels=tokenizer.vocab_size)

# Подготовка данных
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)
train_dataset = DateTimeDataset(train_data, tokenizer)
val_dataset = DateTimeDataset(val_data, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# Настройки для обучения
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Цикл обучения
for epoch in range(3): # по необходимости увеличить количество эпох
    model.train()
    for input_ids, attention_mask, labels, in train_loader:
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    print(f"Эпоха {epoch + 1} закончена, Loss: {loss.item()}")

# Оценка на валидации
model.eval()
with torch.no_grad():
    for input_ids, attention_mask, labels in val_loader:
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        val_loss = outputs.loss
        print(f"Val Loss: {val_loss.item()}")

# Сохранение параметров модели
torch.save(model.state_dict(), "model_weights.pth")

# Сохранение всего объекта модели
torch.save(model, "full_model.pth")