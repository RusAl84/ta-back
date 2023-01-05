import json

if __name__ == "__main__":
    filename = "d:/ml/chat/ChatDEEP.json"
    with open("quotes_keywords.json", "r", encoding="UTF8") as file:
        content = file.read()
    quotes_keywords = json.loads(content)