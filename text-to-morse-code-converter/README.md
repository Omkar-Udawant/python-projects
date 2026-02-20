# 🔤 Text to Morse Code Converter

A command-line Python application that converts plain text into Morse code using a standard Morse code chart.

This project was built as part of **Day 81 – 100 Days of Code (Python Bootcamp)**.

---

## 📌 Project Description

The program takes user input and converts each valid character (A–Z, 0–9) into its corresponding Morse code representation.

- Letters are separated by spaces
- Words are separated using `/`
- Unsupported characters are ignored

---

## 🚀 Features

- ✅ Converts alphabets (A–Z)
- ✅ Converts numbers (0–9)
- ✅ Word separation using `/`
- ✅ Continuous user input loop
- ✅ External Morse code chart file (easy to extend)
- ✅ Clean modular function structure
- ✅ Error handling for missing chart file

---

## 📂 Project Structure

```
text-to-morse-code-converter/
│
├── main.py
├── morse_code_chart.txt
└── README.md
```

---

## ▶️ How to Run

1. Make sure Python 3 is installed.
2. Navigate to the project folder.
3. Run:

```bash
python main.py
```

---

## 🧠 Example

**Input:**
```
hello 123
```

**Output:**
```
.... . .-.. .-.. --- / .---- ..--- ...--
```

---

## 🛠️ Technologies Used

- Python 3
- File Handling
- Dictionary Comprehension
- String Manipulation
- Loops & Conditional Logic

---

## 🎯 Learning Outcomes

- Practiced working with external files
- Strengthened understanding of dictionaries
- Improved function structuring
- Built a complete command-line application
- Applied clean code principles

---

## 🚀 Possible Future Improvements

- Add reverse conversion (Morse → Text)
- Add punctuation support
- Add GUI version using Tkinter
- Create a web version using Flask
- Add unit tests

