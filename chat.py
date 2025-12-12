#!/usr/bin/env python3
import os, time
# 3rd party
from rich.markdown import Markdown
from openai import OpenAI
# local
from arguments import parse_arguments
from console import console
from utilities import log_timing

def get_default_model(fast=False):
  if fast:
    return os.environ.get("HF_MODEL_FAST", "Sao10K/L3-8B-Lunaris-v1")
  return os.environ.get("HF_MODEL", "alpindale/WizardLM-2-8x22B")


def prompt(question, model=None, fast=False):
  def_model = get_default_model(fast)
  if not model:
    model = def_model
  if model == def_model:
    console.print(
      f"""
  Using default {"fast " if fast else ""}model: {def_model}.
  To override, set env var HF_MODEL{"_FAST" if fast else ""}
  or pass in the --model <model-name> argument if running from the command line
      """,
      style="yellow")

  if not question:
    raise SystemError("Nah. You gotta ask a question")

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
    api_key=os.environ["HF_TOKEN"],
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
