"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  yes i would like to make another booking for tonight                     
How many guests are you confirming for tonight's event?
Your input ->  100 
And how many of those guests will need vegan meals?
Your input ->  50                                                                       
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  100  
Thank you — booking confirmed. 100 guests, 50 requiring vegan meals, £100 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  nothing extra, thanks                                                    
I'm sorry, I'm not trained to help with that.
Okay, I'll be around in case you need further help.
? How would you rate your experience today? 1: 👍 Satisfied (/SetSlots(csat_score=satisf
ied))                                                                                   
Thank you for your feedback! I'm glad I could help.
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  hi, i'd like to make a booking for tonight     
How many guests are you confirming for tonight's event?
Your input ->  170  
and how many of those guests will need vegan meals?
Your input ->  160
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  450                                                         
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £450 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?  
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £400 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "deposit exceeds organiser's authorised limit"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  hi, i'd like to find out when the last train is from london 
to Reading today?                                                          
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
Would you like to continue with handle out of scope?
Your input ->  yes i'd like to continue                                    
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Is there anything else I can help you with?
Your input ->  no thanks                                                   
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Is there anything else I can help you with?
Your input ->                                
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The Rasa CALM agent apologised for not knowing the answer and not having access to a knowledge base. It then asked if there was anything else that it could help me with. It further continued that it could only help me with confirming tonight's booking and for anything else i should contact the organiser's directly

"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
The Rasa CALM agent apologised for not knowing the answer and not having access to a knowledge base. It then asked if there was anything else that it could help me with. It further continued that it could only help me with confirming tonight's booking and for anything else i should contact the organiser's directly

In contrast, the exercise 2 agent when asked about train times confusingly and misleadingly asked the user for more information about train times and the task it needed help with even when it didn't have any tools to fetch train times. It didn't offer any help or escalation or tell us what tasks it was able to do. It could have been more polite
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I uncommented the 4 lines of code. I set the cutoff time to be behind the current time and then started the rasa server and rasa shell. i then re-ran the conversation
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now extracts the numbers from the user speech. Pereviously Regex in Python would have handled that.
Python still handles the validation of the inputs against Rod's rules eg are numbers less than 170, is vegan proportion less than  80% and is the deposit advanced less than £300
No additional latency or cost from external LLMs, no API keys to manage.  Old RASA was fully deterministic and predictable and interpretable which is important in regulated industries. For very constrained, well-defined tasks, old Rasa is less
   moving parts. No prompt engineering, no token limits, no model version changes that
  might subtly alter behaviour.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
Yes the CALM agent can improvise in understanding but not in responding or behaviour.  
Since the LLM has seen billions of examples of human comversation in it's pre-training, it's better able to parse intent and to extract values from messy speech. Langraph doesn't have that constraint of what is in the flows. Its agent decides what to do at every step in a way that can't be exactly predicted in advance and this is a source of risk.
No it can't call a tool that wasn't defined in flows.yml.  I'd say that this is a deliberate feature rather than a limitation for the confirmation use case.
"""
