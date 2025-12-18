#!/usr/bin/env python3
import argparse, sys, os
from rich.console import Console

def parse_arguments():
  parser = argparse.ArgumentParser(
    description="Process a question with an optional model parameter",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
%(prog)s "why is the sky blue?"
%(prog)s --question "why is the sky blue?"
%(prog)s --model "deepseek-ai/DeepSeek-V3.2" --question "..."
%(prog)s --question "..." --model "deepseek-ai/DeepSeek-V3.2"
%(prog)s --question "..." --fast
%(prog)s "..." --model "deepseek-ai/DeepSeek-V3.2"
    """
  )

  # Optional arguments
  parser.add_argument(
    "--question",
    "-q",
    type=str,
    help="The question to process"
  )

  parser.add_argument(
    "--model",
    "-m",
    type=str,
    help="Model to use for processing (default: env['HF_MODEL'])"
  )

  parser.add_argument(
    "--fast",
    "-f",
    action="store_true",
    help="Model to use for processing (default: env['HF_MODEL_FAST'])"
  )

  # Positional argument (will be used if --question is not provided)
  parser.add_argument(
    "positional_question",
    nargs="?",
    type=str,
    help="Question as a positional argument (alternative to --question)"
  )

  args = parser.parse_args()

  # Determine which question to use
  if args.question:
    question = args.question
  elif args.positional_question:
    question = args.positional_question
  else:
    parser.error("No question provided. Use either positional argument or --question flag.")

  if question == "-":
    question = sys.stdin.read().strip()

  return (question, args.model, args.fast)
