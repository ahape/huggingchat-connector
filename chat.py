#!/usr/bin/env python3
import os, time
import stopwatch
from arguments import parse_arguments
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

stopwatch.start()

(question, model) = parse_arguments()

console = Console()
console.print("\nProcessing the following...\n", style="yellow")
print(f"  Question: {question}")
print(f"  Model: {model}\n")

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
  ],
)

markdown = completion.choices[0].message.content
markdown = Markdown(markdown)

console.print(f"Finished in {stopwatch.stop()}\n", style="yellow")
console.print(markdown)
print()
