# Setup

Step 1: Set the environment variable `HF_TOKEN` to the access token to use inference stuff

(Unix/macOS)

```sh
echo 'export HF_TOKEN="token_value"' >> ~/.zshrc
# then open a new shell
```

(Windows)

```ps1
setx HF_TOKEN "token_value"
# then open a new shell
```

Step 2: Create the virtual environment

```sh
python3 -m venv .venv
```

Step 3: Activate the virtual environment

(Windows)

```ps1
.venv\Scripts\activate
```

(Unix/macOS)

```sh
.venv/bin/activate
```

Step 4: Install the packages

```sh
pip install -r requirements.txt
```

# Usage

```sh
python3 chat.py --question "What is the capital of South Sudan?" --model "deepseek-ai/DeepSeek-V3.2"
# if --model is omitted, default is deepseek
python3 chat.py --question "What is the capital of South Sudan?"
# other variations
python3 chat.py "What is the capital of South Sudan?"
python3 chat.py "What is the capital of South Sudan?" --model "deepseek-ai/DeepSeek-V3.2"
```
