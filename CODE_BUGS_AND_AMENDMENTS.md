# Code Amendments Log

Changes made to the original course code, with rationale.

---

## [2026-04-11] — Nnamdi

### File: `sovereign_agent/agents/research_agent.py`

**What changed:** Added OpenAI-format tool call detection in the `run_research_agent` message-parsing loop.

**Original behaviour:** The loop only checked for Anthropic/Claude-format tool calls (`type: "tool_use"` blocks inside `m.content`). As a result, `tool_calls_made` was always empty when using the Nebius/Llama endpoint, and the exercise reported "No tool calls were made" even though the model was generating them.

**Root cause:** The Nebius endpoint (OpenAI-compatible) returns tool calls in `m.tool_calls` on the `AIMessage` object, not as structured dicts inside `m.content`. The original parsing code never checked `m.tool_calls`.

**Fix:** Added a check for `hasattr(m, "tool_calls") and m.tool_calls` before the existing content-list check, so both provider formats are handled.

---

## [2026-04-11] — Nnamdi

### File: `sovereign_agent/agents/research_agent.py`

**What changed:** Added a system prompt to `create_react_agent` call (line 89→96).

**Original behaviour:** `create_react_agent(llm, TOOLS)` was called with no system prompt. Llama 3.3 70B on the Nebius endpoint would output multiple tool calls as raw JSON text strings in `m.content` instead of using the structured `tool_calls` interface. LangGraph could not execute these, so the agent loop stopped after one turn with "No tool calls were made."

**Root cause:** Llama 3.3 70B needs explicit instruction to use the tool calling interface rather than dumping JSON. Simple single-tool prompts worked by chance, but complex multi-tool prompts consistently failed.

**Fix:** Added `SYSTEM_PROMPT` instructing the model to use tools one at a time via the tool calling interface. Passed it to `create_react_agent` via the `prompt=` parameter.

---

## Diagnostic Findings — Nebius / Llama 3.3 70B Tool Calling (2026-04-11)

These are the key findings from the debugging session, preserved here so future investigation doesn't start from scratch.

### 1. The Nebius tokenfactory endpoint DOES support structured tool calling
- Confirmed via direct `openai.OpenAI` client call with `tools=` parameter
- `resp.choices[0].message.tool_calls` came back fully populated
- Endpoint: `https://api.tokenfactory.nebius.com/v1/`
- So the endpoint is NOT the problem — it's how the model behaves under different conditions

### 2. LangChain `bind_tools()` works correctly
- `ChatOpenAI(...).bind_tools([check_pub_availability])` with a simple prompt → `tool_calls` populated on the `AIMessage`
- LangChain is converting the tool schemas and passing them to the API correctly

### 3. `create_react_agent` works — but only with simple prompts
- Single tool + short prompt → structured tool calls, full agent loop (tool call → tool result → reasoning → done)
- Four tools + complex multi-step prompt (the Task A brief) → model dumps ALL tool calls as a single JSON text string in `m.content`, no structured `tool_calls` at all
- This is **100% reproducible** — not intermittent

### 4. The failure mode is specific: parallel tool call dumping
- When Llama 3.3 70B "wants" to call multiple tools at once, it falls back to outputting them as a JSON array of strings in the content field
- The content looks like: `["{\"type\": \"function\", \"name\": \"check_pub_availability\", ...}", ...]`
- `m.tool_calls` is `[]` (empty list, not None)
- `m.content` is a `str` (not a list), so it's a serialised JSON array as text
- LangGraph sees no tool calls → terminates the loop after one turn

### 5. The system prompt fix forces sequential tool use
- Telling the model "use tools one at a time" prevents the parallel dump behaviour
- With the system prompt, the model calls tools sequentially: check pub 1 → check pub 2 → catering → weather → flyer
- This produced 6 structured tool calls across the full agent loop

### 6. LangGraph deprecation notice
- `langgraph.prebuilt.create_react_agent` is deprecated in LangGraph v1.1.3
- New import: `from langchain.agents import create_agent`
- Current code still works but will break in LangGraph v2.0
- Not changed now (course code uses the old import) — flag for future weeks

### 7. Package versions at time of testing
- `langgraph`: 1.1.3
- `langchain-openai`: 1.1.12
- Python: 3.12
- Model: `meta-llama/Llama-3.3-70B-Instruct`
