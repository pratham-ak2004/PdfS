# PdfS - PDF Processing Suite

PdfS is a powerful PDF processing application that allows you to summarize, query, and listen to PDF documents using state-of-the-art natural language processing models.

## Features

- **PDF Summarization**: Generate concise summaries of your PDF documents
- **Question Answering**: Ask questions about your PDF content and get precise answers
- **Text-to-Speech**: Listen to your PDF documents with customizable voice options
- **Page Range Selection**: Process specific pages of your PDF documents

## Installation

1. Download the zip file or Clone the repository

```bash
git clone https://github.com/pratham-ak2004/PdfS.git
cd PdfS
```

2. Install the required dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application

```bash
python main.py
```

2. Open the provided URL in your browser (typically http://127.0.0.1:7860)

3. Upload your PDF document using the document viewer

4. Use the available functions:

### Summarizing a PDF

1. Set the page range (optional)
2. Click the "Summarize" button
3. View the generated summary in the text area

### Asking Questions

1. Type your question in the text area
2. Click "Ask Question"
3. View the answer as a notification and in the text area

### Listening to PDF Content

1. Select your preferred voice from the dropdown menu
2. Click "Read" to generate an audio file
3. Use the audio player to listen to the PDF content

## Configuration Options

- **Start Page/End Page**: Set specific page ranges to process
- **Max Summarization Tokens**: Limit the amount of text processed for summarization
- **Max/Min Length**: Control the length of the generated summary
- **Voice Selection**: Choose from available system voices for text-to-speech

## Models Used

- Summarization: `pszemraj/led-base-book-summary`
- Question Answering: `deepset/roberta-base-squad2`
