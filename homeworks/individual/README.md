# FTEC5660: Agentic AI Reproducibility Project

## Project Summary
This repository contains my reproducibility homework for the FTEC5660 course. I evaluated the robustness of a multi-agent framework by substituting its underlying LLM engine to test how different models handle rigid Agentic Workflow constraints.

## My Modification & Experiments
Following the "Edge Case A" guidelines, my core modification was isolating the underlying LLM as a controlled variable. I tested the framework across three models:
1. **gemini-2.5-flash**: Failed in the early design stage due to JSON parsing format issues.
2. **gemini-2.5-pro**: Failed in the code generation stage. The model output conversational text alongside the code, breaking the framework's regex-based extractor.
3. **gpt-4-turbo (Control Group)**: Succeeded perfectly, generating a fully functional CLI tool.

**Conclusion**: Current agent frameworks suffer from "Model Lock-in" and are overfitted to specific model output styles (like OpenAI's). They break easily when other models exhibit slight conversational variations.

## Installation & Setup
To avoid `pip` dependency backtracking loops during installation, use `uv` with a clean virtual environment:

```bash
# 1. Install uv
pip install uv

# 2. Create a clean Python 3.10 environment
uv venv myenv --python 3.10
source myenv/bin/activate

# 3. Install framework allowing pre-release packages
uv pip install "metagpt>=0.8.0" --upgrade --prerelease=allow