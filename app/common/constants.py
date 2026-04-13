"""
Application-wide constants.

Centralizes magic values so they can be tuned from a single location.
"""

from __future__ import annotations

# ── Audio Validation ──
ALLOWED_AUDIO_CONTENT_TYPES: set[str] = {
    "audio/webm",
    "audio/mp3",
    "audio/mpeg",       # standard MIME for MP3
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "audio/m4a",
    "audio/x-m4a",
    "audio/mp4",        # M4A is often sent as audio/mp4
}

ALLOWED_AUDIO_EXTENSIONS: set[str] = {
    ".webm", ".mp3", ".wav", ".ogg", ".m4a",
}

# ── Fast-Path Patterns ──
# Keys are compiled at import time for performance.
GREETING_PATTERNS: list[str] = [
    r"^(hi|hello|hey|howdy|hola|namaste|namaskar)\s*[!?.]*$",
]

GRATITUDE_PATTERNS: list[str] = [
    r"^(thanks|thank\s*you|dhanyavaad|shukriya)\s*[!?.]*$",
]

FAREWELL_PATTERNS: list[str] = [
    r"^(bye|goodbye|good\s*bye|see\s*you|alvida|tata)\s*[!?.]*$",
]

FAST_PATH_RESPONSES: dict[str, str] = {
    "greeting": "Hello! 👋 How can I help you today?",
    "gratitude": "You're welcome! Is there anything else I can help with?",
    "farewell": "Goodbye! Have a great day! 👋",
}

# ── Input Guardrail Patterns (Prompt Injection) ──
PROMPT_INJECTION_PATTERNS: list[str] = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?above\s+instructions",
    r"disregard\s+(all\s+)?previous",
    r"you\s+are\s+now\s+",
    r"act\s+as\s+if\s+you\s+are",
    r"pretend\s+you\s+are",
    r"forget\s+(all\s+)?previous",
    r"new\s+instructions?\s*:",
    r"system\s*prompt\s*:",
    r"override\s+.*instructions",
    r"\[system\]",
    r"\[inst\]",
    r"<\s*system\s*>",
    r"do\s+not\s+follow\s+(your\s+)?instructions",
    r"reveal\s+(your\s+)?(system\s+)?prompt",
    r"what\s+is\s+your\s+system\s+prompt",
]

# ── Small Talk Detection (Tier 0 — O(1) set lookup) ──────────────────────────
# These queries bypass everything and get a canned reply instantly.
# To add a new phrase: append a lowercase string to SMALL_TALK_SET.
SMALL_TALK_SET: set[str] = {
    # Greetings
    "hi", "hello", "hey", "hii", "hiii", "hiiii",
    "hello there", "hey there", "hi there",
    "good morning", "good afternoon", "good evening", "good night",
    "morning", "afternoon", "evening",
    "howdy", "greetings", "salutations",
    "what's up", "whats up", "wassup", "wazzup", "sup",
    "yo", "heya", "hiya", "hola", "namaste", "namaskar",
    # Farewells
    "bye", "goodbye", "good bye", "see you", "see ya",
    "take care", "later", "cya", "ttyl", "talk later",
    "catch you later", "peace out", "peace",
    "bye bye", "bbye", "byee", "alvida", "tata",
    # Gratitude
    "thank you", "thanks", "thankyou", "thank u", "thx", "ty",
    "thanks a lot", "thank you so much", "thanks so much",
    "much appreciated", "appreciate it",
    "thanks for your help", "thank you for helping",
    "dhanyavaad", "shukriya",
    # Politeness
    "please", "sorry", "excuse me", "pardon", "pardon me",
    "my apologies", "apologies", "forgive me",
    # How are you
    "how are you", "how r u", "how r you", "how are u",
    "how's it going", "hows it going",
    "how do you do", "how you doing", "how are you doing",
    "what's going on", "whats going on",
    "how's your day", "hows your day",
    "are you okay", "you okay", "you ok", "r u ok",
    # Bot identity / meta
    "who are you", "what are you", "what is your name",
    "who made you", "who created you", "who built you",
    "what can you do", "what do you do",
    "are you a bot", "are you human", "are you real",
    "are you ai", "are you a robot", "are you a chatbot",
    "tell me about yourself", "introduce yourself",
    # Feelings / small chat
    "i'm fine", "im fine", "i am fine", "doing good", "doing well",
    "i'm good", "im good", "i am good",
    "not bad", "all good", "pretty good",
    "i'm okay", "im okay", "i am okay",
    "nice to meet you", "nice meeting you", "pleased to meet you",
    "same to you", "you too",
    # Filler / acknowledgements
    "ok", "okay", "k", "kk", "cool", "nice", "great", "awesome",
    "wow", "lol", "haha", "hehe", "lmao", "rofl",
    "interesting", "oh", "oh okay", "i see", "got it",
    "hmm", "hmmm", "hmmmm", "umm", "ummm",
    "yes", "no", "yeah", "yep", "nope", "nah", "yea",
    "sure", "of course", "absolutely", "definitely",
    "good", "bad", "fine",
    "tell me a joke", "tell me something funny",
    "what's the weather", "whats the weather", "weather today",
    "what time is it", "what is the time",
    "sing a song", "tell me a story", "tell a story",
}

SMALL_TALK_RESPONSES: list[str] = [
    (
        "Hello! 👋 I'm the ACPC Gujarat Admissions Chatbot. I can help you with "
        "admission processes, college information, merit ranks, and cut-offs. "
        "How can I assist you today?"
    ),
    (
        "Hi there! I'm here to help with ACPC Gujarat admissions queries. "
        "Feel free to ask me about admission procedures, college details, or cut-off ranks!"
    ),
    (
        "Hey! 😊 I'm your ACPC Gujarat assistant. Ask me anything about admissions, "
        "colleges, merit lists, eligibility, or the counselling process!"
    ),
    (
        "Greetings! I specialise in ACPC Gujarat admission information. "
        "What would you like to know?"
    ),
]

# ── Bad Words / Abusive Language (Tier 0 — O(1) set lookup) ──────────────────
# These are blocked immediately before any LLM call.
# To add a new term: append a lowercase string to BAD_WORDS_SET.
BAD_WORDS_SET: set[str] = {
    # Common English profanity & variants
    "fuck", "fck", "fuk", "f*ck", "fu*k", "fuc", "fuq",
    "fucking", "fcking", "fuking", "fking",
    "fucked", "fcked", "fuked",
    "fucker", "fcker", "fukker",
    "motherfucker", "motherfcker", "mfer", "mofo",
    "shit", "sh1t", "sht", "shyt", "bullshit", "bs",
    "shitty", "sh1tty", "shitting",
    "ass", "a$$", "a*s", "arse",
    "asshole", "a$$hole", "a-hole", "arsehole",
    "bitch", "b1tch", "b!tch", "biatch",
    "bitches", "b1tches",
    "bastard", "b@stard", "bstrd",
    "damn", "dammit", "damnit", "goddamn", "goddammit",
    "go to hell", "burn in hell",
    "dick", "d1ck", "d!ck",
    "dickhead", "d1ckhead",
    "cock", "c0ck",
    "pussy", "pu$$y", "pus$y",
    "cunt", "c*nt", "cnt",
    "whore", "wh0re", "wh*re",
    "slut", "sl*t", "s1ut",
    "retard", "r3tard", "retarded",
    "idiot", "idi0t",
    "stupid", "stup1d", "stupd",
    "dumb", "dumbass", "dumba$$",
    "moron", "m0ron",
    "loser", "l0ser",
    "trash", "garbage", "worthless",
    "stfu", "gtfo", "kys",
    # Slurs & hate speech
    "nigger", "n1gger", "n!gger", "nigg3r", "nigga",
    "faggot", "f@ggot", "fag", "f@g",
    "chink", "ch1nk",
    "spic", "sp1c",
    "wetback", "w3tback",
    "kike", "k1ke",
    "gook", "g00k",
    "tranny", "tr@nny",
    "dyke", "d*ke",
    # Threats & violence
    "kill you", "kill yourself",
    "i will kill", "gonna kill",
    "murder", "murd3r",
    "rape", "r@pe",
    "bomb", "b0mb",
    "terrorist", "terr0rist",
    # Hindi/Gujarati abusive (common in ACPC context)
    "madarchod", "mc", "bc", "behenchod",
    "chutiya", "chutia", "ch*tiya",
    "gaand", "gand", "g@nd",
    "bhosdike", "bhosdi", "bhosdiwale",
    "harami", "haramkhor",
    "kamina", "kameena", "kameeni",
    "gadha", "gadhe", "ullu",
    "kutte", "kutta", "kutiya",
    "randi", "r@ndi","condom","gondom","gandmra","gandmara",
    "gandmarn","gandmarni","gandmarnii","gandmarnii",
}

# Pre-extracted multi-word bad phrases for fast substring scan
_BAD_WORD_PHRASES: frozenset[str] = frozenset(
    p for p in BAD_WORDS_SET if " " in p
)

BAD_WORD_RESPONSE: str = (
    "⚠️ I'm unable to process messages containing inappropriate language. "
    "I'm here to help you with ACPC Gujarat admissions queries. "
    "Please rephrase your question respectfully and I'll be happy to assist!"
)

# ── LLM Prompts ──
ROUTER_SYSTEM_PROMPT = """You are an intent classifier for a document retrieval system. 
Analyze the user's query and chat history, then classify the query into exactly ONE of these categories:

- "rag": The user wants to search for information semantically (open-ended questions, concept lookups, general knowledge retrieval).
- "filter": The user wants to look up specific structured data (filtering by department, rank, record ID, specific fields, exact matches).
- "hybrid": The user's query requires BOTH semantic search AND structured filtering (e.g., "Show me Rank 2 requirements for the Sales department" needs both semantic understanding and structured filtering).

Respond with ONLY a JSON object in this exact format:
{"route": "<rag|filter|hybrid>", "reasoning": "<one sentence explaining your decision>"}

Do not include any other text outside this JSON."""

SYNTHESIS_SYSTEM_PROMPT = """You are a helpful and conversational assistant. Your job is to take the 
retrieved data provided to you and synthesize it into a clear, friendly, and accurate response 
for the user.

Rules:
1. Use the retrieved data as your ONLY source of truth. Do NOT hallucinate or make up information.
2. If the retrieved data is empty or irrelevant, say so honestly.
3. Be conversational but concise.
4. When citing sources, reference the document names naturally in your response.
5. Maintain context from the chat history for follow-up questions."""
