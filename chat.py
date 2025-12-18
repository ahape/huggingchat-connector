#!/usr/bin/env python3
import os, sys
from pathlib import Path

from rich.markdown import Markdown
from rich.live import Live
from openai import OpenAI, APIError

from arguments import parse_arguments
from console import console
from utilities import log_timing

MODEL_DEFAULT_FAST = "meta-llama/Llama-3.2-1B-Instruct"
MODEL_DEFAULT = "EssentialAI/rnj-1-instruct:together"

_client = None  # Reusable client instance

def get_api_key():
  token = os.getenv("HF_TOKEN")
  if token:
    return token

  token_path = Path(".HF_TOKEN")
  if token_path.exists():
    return token_path.read_text().strip()

  raise SystemExit("ERROR: Need to configure your HF_TOKEN")

def get_client():
  global _client
  if _client is None:
    _client = OpenAI(
      base_url="https://router.huggingface.co/v1",
      api_key=get_api_key(),
    )
  return _client


def get_default_model(fast=False):
  if fast:
    return os.getenv("HF_MODEL_FAST", MODEL_DEFAULT_FAST)
  return os.getenv("HF_MODEL", MODEL_DEFAULT)


def prompt(question, model=None, fast=False, stream=True):
  if not model:
    model = get_default_model(fast)
  if not question:
    raise SystemExit("ERROR: You gotta ask a question")

  console.print("\nProcessing...\n", style="yellow")
  console.print(f"  Question: {question}")
  console.print(f"  Model: {model}\n")

  try:
    if stream:
      answer = stream_answer(question, model)
    else:
      answer = get_answer(question, model)
      console.print(Markdown(answer))
  except APIError as e:
    console.print(f"[red]API Error: {e.message}[/red]")
    return

  console.print("\n")


@log_timing
def get_answer(question, model, system_prompt=None):
  messages = []
  if system_prompt:
    messages.append({"role": "system", "content": system_prompt})
  messages.append({"role": "user", "content": question})

  completion = get_client().chat.completions.create(
    model=model,
    messages=messages,
  )
  return completion.choices[0].message.content


def stream_answer(question, model):
  stream = get_client().chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": question}],
      stream=True,
  )

  full_response = ""
  with Live(console=console, refresh_per_second=10) as live:
    for chunk in stream:
      if chunk.choices and chunk.choices[0].delta.content:
        full_response += chunk.choices[0].delta.content
        live.update(Markdown(full_response))

  return full_response


if __name__ == "__main__":
  question, model, fast = parse_arguments()
  prompt(question, model, fast)
