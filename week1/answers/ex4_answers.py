"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER  = "Okay, the user is looking for a venue in Edinburgh that can hold 300 people and has vegan options. I first tried using the search_venues function with min_capacity 300 and requires_vegan true, but there was a validation error. The error said that min_capacity and requires_vegan were required fields. Wait, the user did provide those arguments. Maybe the tool expects the parameters to be nes..."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I changed Albanach status to full in the mcp_venue_server.py file. No other files needed updating. For Query 1, only Haymarket Vault was returned as being suitable and this is correct since Haymarket vaults had been marked as full
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 283   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 100   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
It offers modularity, openness and a single source of truth.  The LangGraph agent and the Rasa agent can both connect to it rather than having their own individual and separate tool definitions.  If one of the venues were to have a change eg become full or there were cancellations there then it would be easy to just update the availability in a few key strokes in one place.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- FILL ME IN
- FILL ME IN
- FILL ME IN
- FILL ME IN
- FILL ME IN
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
FILL ME IN
"""
