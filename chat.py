#!/usr/bin/env python3
import os, time
# 3rd party
from rich.markdown import Markdown
from openai import OpenAI
# local
from arguments import parse_arguments
from console import console
from utilities import log_timing

model_default_fast = "meta-llama/Llama-3.2-1B-Instruct"
model_default = "alpindale/WizardLM-2-8x22B"

def get_api_key():
  try:
    tok = os.getenv("HF_TOKEN", None) or \
          open(".HF_TOKEN").read().strip()
    return tok
  except:
    raise SystemExit("ERROR: Need to configure your HF_TOKEN")

def get_default_model(fast):
  if fast:
    return os.getenv("HF_MODEL_FAST", model_default_fast)
  return os.getenv("HF_MODEL", model_default)


def prompt(question, model=None, fast=False):
  if not model:
    model = get_default_model(fast)

  if not question:
    raise SystemExit("ERROR: You gotta ask a question")

  console.print("\nProcessing the following...\n", style="yellow")
  console.print(f"  Question: {question}")
  console.print(f"  Model: {model}\n")

  answer = get_answer(question, model)
  markdown = Markdown(answer)

  console.print(markdown)
  console.print("\n")

@log_timing
def get_answer(question, model):
  client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=get_api_key(),
  )

  completion = client.chat.completions.create(
    model=model,
    messages=[
      {
        "role": "user",
        "content": question,
      }
    ]
  )

  return completion.choices[0].message.content

if __name__ == "__main__":
  (question, model, fast) = parse_arguments()

  prompt(question, model, fast)
