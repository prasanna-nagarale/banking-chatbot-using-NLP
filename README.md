# 🏦 Banking Chatbot using NLP 🤖

A multilingual, voice-enabled AI chatbot designed to provide 24/7 customer support in the banking sector. Built using NLP and machine learning techniques, it answers customer queries related to banking products, services, and policies with accuracy and speed.

---

## 🧠 Introduction

In today’s digital-first world, customers expect instant and personalized banking assistance. Traditional support (call centers or bank visits) often involve delays and limited service hours. This project solves that by building an intelligent chatbot capable of:

- Understanding customer queries in natural language.
- Responding via text or voice.
- Handling multilingual communication.
- Reducing workload on human agents and operational costs.

---

## ❓ Problem Statement

Traditional banking support systems:
- Involve long wait times.
- Are not available 24/7.
- Are expensive and difficult to scale.

This chatbot:
- Answers FAQs about account types, loans, banking rules, etc.
- Supports voice/text input and response.
- Provides multi-language support.
- Reduces overhead and improves customer experience.

---

## 🛠️ Technologies Used

| Feature                     | Library / Tool          |
|-----------------------------|--------------------------|
| 🧹 NLP Preprocessing        | NLTK (tokenization, lemmatization, stopword & punctuation removal) |
| 🔊 Voice Input              | SpeechRecognition       |
| 🗣️ Text-to-Speech          | Pyttsx3                 |
| 🧠 Response Generation      | Scikit-learn (TF-IDF, cosine similarity) |
| 🌐 Multilingual Support     | GoogleTrans             |
| ⚙️ Backend Logic            | Python                  |
| 🖥️ Interface (CLI/Web)      | Python CLI / Flask (optional) |

---

## 🖼️ Interface Screenshot

> Visual of chatbot in action:
![Chatbot Screenshot](https://github.com/user-attachments/assets/5dabeb6e-d47c-4af3-8bc7-d43fb76b0206)

---

## 🔁 Workflow Overview

1. User provides input (text or voice).
2. Input is preprocessed using NLP (lemmatization, tokenization, etc.).
3. System compares input with FAQ corpus using TF-IDF + cosine similarity.
4. Most relevant response is selected.
5. Output is returned via text and optionally spoken aloud (via pyttsx3).
6. User can interact again or exit.

---

## 🌍 Supported Features

- 🔎 Account types, interest rates, loan info, policy queries, etc.
- 🗣️ Voice input and audio output.
- 🌐 Multi-language translation via Google Translator API.
- 🧠 Continuous conversation support.
- 🚫 Error handling for silent input, noise, and unrecognized commands.

---

## 💡 Future Improvements

- Web-based interface using Flask or React.js.
- Integration with real-time databases for dynamic answers.
- Authentication system for account-specific support.
- Logging conversations for training better AI.
