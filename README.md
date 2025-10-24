## Usage Instructions

Run the following commands in terminal.

### 1. Create virtual environment inside project root directory

Not required but recommended. Skip to step 3 to install directly on computer.

```
python -m venv .venv
```

### 2. Activate virtual environment

```
.\.venv\Scripts\activate
```

### 3. Install requirements

This installs all requirements needed to run the project.

```
python -m pip install -r .\requirements.txt
python -m spacy download en_core_web_sm
pip install transformers torch
```

### 4. Install CoreNLP

Installs the Stanford CoreNLP Server. Ensure you already have Java installed in your system.

```
python -c "import stanza;stanza.install_corenlp()"
```

### 5. Running Python file

Run the algorithm in Python to see if it works with no error.

```
python .\love_in_paradise\server\main.py
```

### 5. Running the server

Once the algorithm is verified working properly as intended, make the server available on localhost by running the Flask server.

```
python .\love_in_paradise\server\server.py
```

### 6. Use via website GUI

Access the server using web user interface. Run with npm and open the displayed link in a web browser. (Usually at http://localhost:3000)

```
cd .\love_in_paradise\
npm run dev
```

## Credits

- [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) by Stanford NLP Group
- Tagalog NLP pipeline taken from [calamanCy](https://huggingface.co/ljvmiranda921/tl_calamancy_md).
