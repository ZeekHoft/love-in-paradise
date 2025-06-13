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

This installs spaCy and English and Tagalog NLP pipelines. Estimated storage size of 1.8 GB, install aswell transformers and torch for the pre-trained library and building deep learning models the size should be around 200mb

```
python -m pip install -r .\requirements.txt
python -m spacy download en_core_web_sm
pip install transformers torch
```

### 4. Running Python file

Run either english or tagalog python files to view corresponding output. Example:

```
python .\english.py
```

## Credits

Tagalog NLP pipeline taken from [calamanCy](https://huggingface.co/ljvmiranda921/tl_calamancy_md).
