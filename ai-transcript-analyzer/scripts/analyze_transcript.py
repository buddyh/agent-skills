#!/usr/bin/env python3
"""
Transcript Analysis Script using OpenAI API

Analyzes transcripts using gpt-5-mini to provide:
- Executive summary
- Key insights
- Topic breakdown with summaries
- Notable quotes and highlights
"""

import argparse
import json
import os
import sys
from pathlib import Path
from openai import OpenAI


def read_transcript(file_path):
    """Read transcript file content."""
    try:
        return Path(file_path).read_text()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_transcript(transcript_text, model="gpt-5-mini", custom_prompt=None):
    """
    Analyze transcript using OpenAI API.

    Args:
        transcript_text: The transcript content to analyze
        model: OpenAI model to use (default: gpt-5-mini)
        custom_prompt: Custom analysis prompt (if None, uses default comprehensive analysis)

    Returns:
        Analysis results as a dictionary
    """
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: export OPENAI_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    print(f"🤖 Analyzing transcript with {model}...")

    # Use custom prompt or default
    if custom_prompt:
        system_prompt = "You are an expert content analyzer. Analyze the provided transcript according to the user's request."
        user_message = f"{custom_prompt}\n\nTranscript:\n\n{transcript_text}"
    else:
        # Default comprehensive analysis prompt
        system_prompt = """You are an expert content analyzer. Analyze the provided transcript and create a comprehensive analysis with the following sections:

1. EXECUTIVE SUMMARY: A concise 2-3 paragraph overview of the entire content

2. KEY INSIGHTS: 5-7 bullet points highlighting the most important takeaways

3. TOPICS DISCUSSED: Break down the major topics covered, with:
   - Topic name
   - Brief summary (2-3 sentences)
   - Key points discussed

4. NOTABLE QUOTES: 3-5 memorable or impactful quotes from the transcript

5. ACTION ITEMS: Any concrete actions, recommendations, or next steps mentioned

6. ADDITIONAL NOTES: Any other relevant observations, context, or interesting details

Format your response in clear markdown with headers and bullet points for readability."""
        user_message = f"Please analyze this transcript:\n\n{transcript_text}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        analysis = response.choices[0].message.content

        # Get usage stats
        usage = response.usage
        print(f"✅ Analysis complete!")
        print(f"   Tokens used: {usage.total_tokens:,} (prompt: {usage.prompt_tokens:,}, completion: {usage.completion_tokens:,})")

        return {
            "analysis": analysis,
            "model": model,
            "tokens_used": usage.total_tokens,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens
        }

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)


def save_analysis(analysis_data, output_path, transcript_path):
    """Save analysis to markdown file."""

    # Create header with metadata
    header = f"""# Transcript Analysis

**Source Transcript:** {transcript_path}
**Analysis Model:** {analysis_data['model']}
**Tokens Used:** {analysis_data['tokens_used']:,}

---

"""

    output_content = header + analysis_data['analysis']

    # Save to file
    output_file = Path(output_path)
    output_file.write_text(output_content)

    print(f"💾 Analysis saved to: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Analyze transcripts using OpenAI gpt-5-mini'
    )
    parser.add_argument(
        'transcript',
        help='Path to transcript file to analyze'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: transcript_name_analysis.md)'
    )
    parser.add_argument(
        '--model', '-m',
        default='gpt-5-mini',
        help='OpenAI model to use (default: gpt-5-mini)'
    )
    parser.add_argument(
        '--print', '-p',
        action='store_true',
        help='Print analysis to stdout instead of saving to file'
    )
    parser.add_argument(
        '--prompt',
        help='Custom analysis prompt (overrides default comprehensive analysis)'
    )

    args = parser.parse_args()

    # Read transcript
    print(f"📄 Reading transcript: {args.transcript}")
    transcript_text = read_transcript(args.transcript)

    # Analyze
    analysis_data = analyze_transcript(transcript_text, model=args.model, custom_prompt=args.prompt)

    # Output results
    if args.print:
        print("\n" + "="*80)
        print(analysis_data['analysis'])
        print("="*80)
    else:
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            # Auto-generate output filename
            transcript_path = Path(args.transcript)
            output_path = transcript_path.parent / f"{transcript_path.stem}_analysis.md"

        save_analysis(analysis_data, output_path, args.transcript)

    return 0


if __name__ == '__main__':
    sys.exit(main())
