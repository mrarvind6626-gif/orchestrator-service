"""
ACPC Gujarat FAQ — Direct-answer knowledge base.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW TO ADD A NEW FAQ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Find the right section below (or create a new one).
2. Add a new tuple to _ACPC_FAQS:

    (
        [
            "trigger phrase one",       # all lowercase, exact match
            "another way to ask it",
        ],
        "Your formatted answer here.",  # markdown OK
    ),

3. That's it — ACPC_FAQ_DICT is rebuilt automatically.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW TO ADD A SUGGESTED QUESTION (UI chips)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Append a string to SUGGESTED_QUESTIONS at the bottom of this file.
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# Primary FAQ data — list of (trigger_phrases, answer) tuples.
# All triggers must be lowercase and normalised (stripped, collapsed whitespace).
# ─────────────────────────────────────────────────────────────────────────────

_ACPC_FAQS: list[tuple[list[str], str]] = [

    # ── General / About ACPC ─────────────────────────────────────────────────

    (
        [
            "what is acpc",
            "what is acpc gujarat",
            "tell me about acpc",
            "explain acpc",
            "acpc full form",
            "full form of acpc",
            "what does acpc stand for",
            "what is the full form of acpc",
        ],
        (
            "**ACPC** stands for **Admission Committee for Professional Courses**, Gujarat State.\n\n"
            "It is the official state-level body that manages *centralised admissions* to:\n"
            "- Engineering (BE / B.Tech)\n"
            "- Pharmacy (B.Pharm / D.Pharm)\n"
            "- MBA & MCA\n"
            "- M.Tech & M.Pharm\n"
            "- Diploma courses (through NATA/JEE for architecture)\n\n"
            "All eligible candidates must register on the ACPC portal to participate in the "
            "centralised counselling process for Gujarat government, aided, and self-financed colleges."
        ),
    ),

    (
        [
            "acpc website",
            "acpc official website",
            "acpc portal link",
            "acpc portal",
            "where to register for acpc",
            "acpc registration website",
            "acpc gujarat website",
            "acpc online portal",
        ],
        (
            "The official ACPC Gujarat portal is **acpcgujarat.ac.in**.\n\n"
            "On the portal you can:\n"
            "✅ Register as a new candidate\n"
            "✅ Fill and lock your college-branch choices\n"
            "✅ Check your merit rank\n"
            "✅ View seat allotment results\n"
            "✅ Download your Provisional Admission Letter (PAL)\n"
            "✅ Access the helpdesk and FAQs\n\n"
            "Bookmark the portal and check it regularly during the admission season."
        ),
    ),

    (
        [
            "acpc helpline",
            "acpc helpline number",
            "acpc contact number",
            "acpc phone number",
            "acpc contact",
            "acpc support",
            "how to contact acpc",
            "acpc customer care",
        ],
        (
            "For ACPC Gujarat support:\n\n"
            "📞 **Helpline:** Check the current helpline number on **acpcgujarat.ac.in** "
            "(it is updated every admission cycle).\n"
            "🌐 **Website:** acpcgujarat.ac.in\n"
            "📧 **Helpdesk:** Use the 'Raise Query' / 'Help Desk' section on the ACPC portal.\n\n"
            "💡 *Tip: For faster resolution, raise your query through the official portal "
            "helpdesk rather than calling, as written queries get a trackable ticket number.*"
        ),
    ),

    # ── Eligibility ──────────────────────────────────────────────────────────

    (
        [
            "eligibility for acpc",
            "eligibility for engineering admission",
            "acpc eligibility criteria",
            "who can apply for acpc",
            "what is the eligibility",
            "am i eligible for acpc",
            "eligibility criteria for be",
            "eligibility for b.tech",
            "12th marks required for acpc",
            "minimum percentage for acpc",
        ],
        (
            "**Eligibility criteria for BE / B.Tech through ACPC Gujarat:**\n\n"
            "📚 **Academic:** Passed HSC (12th Science) with **Physics, Chemistry & Mathematics (PCM)**.\n"
            "📊 **Minimum marks:**\n"
            "  - General / Open: **45% aggregate** in PCM\n"
            "  - SC / ST / SEBC / EWS: **40% aggregate** in PCM\n\n"
            "📝 **Entrance exam:** Must have a valid score in **JEE Main** OR **GUJCET**.\n"
            "🏠 **Domicile:** Must be a Gujarat domicile or have studied in Gujarat for the "
            "last two years (check ACPC rules for exact domicile criteria).\n\n"
            "ℹ️ *Eligibility details may change yearly — always verify on the official ACPC portal.*"
        ),
    ),

    (
        [
            "what is gujcet",
            "gujcet exam",
            "gujcet vs jee",
            "can i use gujcet for acpc",
            "gujcet for engineering admission",
            "is gujcet required for acpc",
        ],
        (
            "**GUJCET** (Gujarat Common Entrance Test) is a state-level entrance exam conducted "
            "by **GSEB** (Gujarat Secondary and Higher Secondary Education Board).\n\n"
            "📌 **For ACPC admissions:**\n"
            "- GUJCET score can be used as an *alternative* to JEE Main for merit rank calculation.\n"
            "- Students who haven't appeared for JEE Main can use their GUJCET score.\n"
            "- Both GUJCET and JEE Main scores are accepted; ACPC uses the better one for merit.\n\n"
            "📅 GUJCET is typically held in April–May. Check **gseb.org** for the exam schedule."
        ),
    ),

    # ── Merit Rank ───────────────────────────────────────────────────────────

    (
        [
            "how is merit rank calculated",
            "merit rank calculation",
            "acpc merit rank formula",
            "how merit rank is decided",
            "merit rank calculation formula",
            "how to calculate merit rank",
            "what is merit rank",
            "acpc merit list",
            "how is acpc rank calculated",
        ],
        (
            "**ACPC Merit Rank Calculation (Engineering — BE/B.Tech):**\n\n"
            "| Component | Weightage |\n"
            "|-----------|----------|\n"
            "| Gujcet Percentile | **60%** |\n"
            "| HSC (12th Board) Marks | **40%** |\n\n"
            "📌 **Formula:**\n"
            "`Merit Score = (Gujcet Percentile × 0.60) + (HSC PCM% × 0.40)`\n\n"
            "🔄 **Tie-breaking** (when merit scores are equal):\n"
            "1. Higher HSC PCM percentage\n"
            "2. Higher Gujcet score in Mathematics\n"
            "3. Higher Gujcet score in Physics\n"
            "4. Date of birth (older candidate preferred)\n\n"
            "ℹ️ *Verify the current formula on acpcgujarat.ac.in as it may change yearly.*"
        ),
    ),

    # ── Registration & Process ───────────────────────────────────────────────

    (
        [
            "how to register for acpc",
            "acpc registration process",
            "steps to apply for acpc",
            "how to apply for acpc",
            "acpc admission process",
            "steps for acpc admission",
            "acpc registration steps",
            "how to start acpc application",
        ],
        (
            "**Steps to Register on the ACPC Portal:**\n\n"
            "1️⃣ Visit **acpcgujarat.ac.in**\n"
            "2️⃣ Click **New Registration** and fill in your personal and academic details\n"
            "3️⃣ Enter your HSC (12th) exam details and JEE Main / GUJCET score\n"
            "4️⃣ Upload all required documents (see list below)\n"
            "5️⃣ Pay the **registration fee** online\n"
            "6️⃣ Note your **Application ID** and login credentials\n"
            "7️⃣ Wait for your **merit rank** to be published\n"
            "8️⃣ Proceed to **Choice Filling** once merit ranks are declared\n\n"
            "💡 *Complete registration early — do not wait for the last day.*"
        ),
    ),

    (
        [
            "documents required for acpc",
            "documents needed for acpc",
            "what documents do i need",
            "required documents for acpc",
            "acpc document list",
            "documents for admission",
            "list of documents for acpc",
            "what papers are needed for acpc",
        ],
        (
            "**Documents Required for ACPC Gujarat Admission:**\n\n"
            "📄 **Academic:**\n"
            "- HSC (12th) Marksheet & Passing Certificate\n"
            "- SSC (10th) Marksheet & Passing Certificate\n"
            "- School Leaving Certificate (SLC / Transfer Certificate)\n"
            "- JEE Main Score Card and/or GUJCET Score Card\n\n"
            "🪪 **Identity & Domicile:**\n"
            "- Aadhaar Card\n"
            "- Domicile / Nativity Certificate (Gujarat)\n\n"
            "📋 **Category Certificates** *(if applicable)*:\n"
            "- Caste Certificate (SC / ST / SEBC)\n"
            "- Non-Creamy Layer Certificate (SEBC)\n"
            "- EWS Certificate (for EWS quota)\n"
            "- Income Certificate\n"
            "- PH / Disability Certificate (if applicable)\n\n"
            "📸 **Other:**\n"
            "- Recent passport-size photographs\n"
            "- Provisional Admission Letter (printed from ACPC portal after allotment)\n\n"
            "💡 *Carry originals + 3 sets of self-attested photocopies for document verification.*"
        ),
    ),

    # ── Choice Filling ───────────────────────────────────────────────────────

    (
        [
            "what is choice filling",
            "how to fill choices",
            "choice filling in acpc",
            "how choice filling works",
            "acpc choice filling process",
            "how to add choices",
            "how many choices can i fill",
            "choice filling tips",
        ],
        (
            "**Choice Filling — How It Works:**\n\n"
            "Choice filling is the step where you select and *rank* your preferred "
            "college–branch combinations.\n\n"
            "📝 **How to fill choices:**\n"
            "1. Log in to **acpcgujarat.ac.in** during the choice-filling window\n"
            "2. Search colleges by location, type (Govt / Private), or branch\n"
            "3. Add college-branch pairs to your choice list\n"
            "4. **Drag and rank** them from most preferred (top) to least preferred (bottom)\n"
            "5. Save and lock your choices before the deadline\n\n"
            "✅ **Tips:**\n"
            "- Add ALL colleges you are genuinely willing to attend — there is no penalty\n"
            "- Put your dream college first, safer options lower down\n"
            "- Do NOT lock unless you are satisfied — changes can be made before the deadline\n"
            "- Once locked, choices cannot be changed for that round"
        ),
    ),

    # ── Seat Allotment ───────────────────────────────────────────────────────

    (
        [
            "what is seat allotment",
            "how seat allotment works",
            "acpc seat allotment process",
            "how are seats allotted",
            "seat allotment in acpc",
            "how to check seat allotment",
            "seat allotment result",
            "how to see my allotted seat",
        ],
        (
            "**ACPC Seat Allotment — How It Works:**\n\n"
            "Seats are allotted automatically by the ACPC system based on:\n"
            "- Your **merit rank**\n"
            "- Your **filled choices** (higher-ranked choices are tried first)\n"
            "- **Seat availability** in each category\n\n"
            "📋 **After allotment, you have 3 options:**\n\n"
            "| Option | Meaning |\n"
            "|--------|--------|\n"
            "| **Freeze** | Accept this seat as final; don't participate in further rounds |\n"
            "| **Float / Upgrade** | Accept this seat but try for a better choice in the next round |\n"
            "| **Reject** | Reject the seat and exit the process entirely |\n\n"
            "🔍 **To check your result:** Log in to **acpcgujarat.ac.in** → 'Seat Allotment Result'"
        ),
    ),

    (
        [
            "how many rounds in acpc",
            "number of counselling rounds",
            "acpc rounds",
            "how many rounds of counselling",
            "acpc counselling rounds",
            "rounds in acpc process",
        ],
        (
            "**ACPC Counselling Rounds:**\n\n"
            "ACPC typically conducts **3 to 4 rounds** of seat allotment:\n\n"
            "🔁 **Regular Rounds (Round 1, 2, 3):**\n"
            "- Open to all registered candidates with a merit rank\n"
            "- You can upgrade (float) to a better seat in each successive round\n"
            "- Seats vacated by candidates who exit go back into the pool\n\n"
            "🏁 **Open Round (Mop-Up Round — Final):**\n"
            "- Last round of the process\n"
            "- Open to **any eligible candidate** (even those who didn't register earlier)\n"
            "- No upgrades after this round — allotment is final\n"
            "- Remaining vacant seats are filled here\n\n"
            "ℹ️ *The exact number of rounds is announced by ACPC before each admission cycle.*"
        ),
    ),

    (
        [
            "what is open round",
            "open round acpc",
            "what is mop up round",
            "mop-up round",
            "last round acpc",
            "open round eligibility",
            "can i join open round",
        ],
        (
            "**Open Round (Mop-Up Round):**\n\n"
            "The Open Round is the **final round** of ACPC counselling.\n\n"
            "📌 **Key features:**\n"
            "- Any eligible candidate can participate — including those who did *not* register earlier\n"
            "- Seats available are those remaining after all regular rounds\n"
            "- There is **no upgrade option** in the Open Round — once allotted, you must report or exit\n"
            "- Candidates who previously rejected their seat may also apply\n\n"
            "⚠️ *Candidates who have already frozen a seat in a regular round should NOT participate "
            "in the Open Round unless they intend to cancel their frozen seat.*"
        ),
    ),

    (
        [
            "how to freeze seat",
            "freeze seat in acpc",
            "what is freeze option",
            "freeze vs float",
            "should i freeze or float",
            "acpc freeze option",
        ],
        (
            "**Freeze vs Float (Upgrade):**\n\n"
            "| Action | What it means |\n"
            "|--------|---------------|\n"
            "| **Freeze** | You accept the current seat as your *final* choice. ACPC process ends for you. You must now report to the college. |\n"
            "| **Float** | You accept the current seat temporarily but want to *try for a better one* in the next round. If a better seat is available, you get it; otherwise you keep the current one. |\n\n"
            "💡 **When to Freeze:**\n"
            "- You are satisfied with the allotted college and branch\n"
            "- You don't want to risk losing the seat\n\n"
            "💡 **When to Float:**\n"
            "- You want a higher-ranked choice that hasn't been allotted yet\n"
            "- You are willing to wait for the next round\n\n"
            "⚠️ *If you neither freeze, float, nor reject within the deadline, your seat may be cancelled automatically.*"
        ),
    ),

    (
        [
            "what happens if i don't report",
            "what if i miss reporting date",
            "not reporting to college acpc",
            "missed reporting deadline",
            "seat cancellation acpc",
            "what if i don't go to college after allotment",
        ],
        (
            "⚠️ **If you don't report to your allotted college by the deadline:**\n\n"
            "- Your **seat will be forfeited** (cancelled automatically)\n"
            "- You may lose your admission fee (depending on the stage)\n"
            "- You may only be able to re-enter the process in the **Open Round**, subject to ACPC rules\n\n"
            "📌 **Always:**\n"
            "- Note the reporting deadline in your Provisional Admission Letter (PAL)\n"
            "- Report on time with all original documents\n"
            "- Contact the college or ACPC helpdesk immediately if you face an emergency"
        ),
    ),

    # ── Reservation & Categories ─────────────────────────────────────────────

    (
        [
            "reservation categories in acpc",
            "acpc reservation",
            "quota in acpc",
            "what are the reservation categories",
            "sc st reservation acpc",
            "obc reservation acpc",
            "sebc reservation",
            "ews reservation acpc",
            "reservation percentage acpc",
        ],
        (
            "**Reservation Categories in ACPC Gujarat (Government Colleges):**\n\n"
            "| Category | Reservation |\n"
            "|----------|-------------|\n"
            "| SC (Scheduled Caste) | 7% |\n"
            "| ST (Scheduled Tribe) | 15% |\n"
            "| SEBC (Socially & Educationally Backward Classes) | 27% |\n"
            "| EWS (Economically Weaker Section) | 10% |\n"
            "| PH (Physically Handicapped) | 3% (horizontal reservation) |\n"
            "| Ex-Servicemen | 1% (horizontal reservation) |\n"
            "| General / Open | Remaining seats |\n\n"
            "📋 **Required certificates:**\n"
            "- SC/ST: Caste Certificate from competent authority\n"
            "- SEBC: Caste Certificate + Non-Creamy Layer Certificate\n"
            "- EWS: EWS Certificate + Income Certificate\n\n"
            "ℹ️ *Private self-financed colleges follow a separate seat matrix — check the ACPC portal.*"
        ),
    ),

    # ── Cut-off Ranks ────────────────────────────────────────────────────────

    (
        [
            "what is cut off rank",
            "cut off rank acpc",
            "how to check cut off",
            "previous year cut off",
            "acpc cut off",
            "cut off for engineering",
            "what does cut off mean",
            "last rank admitted",
        ],
        (
            "**Cut-off Rank — What It Means:**\n\n"
            "The cut-off rank is the **last (highest numbered) merit rank** at which a seat was "
            "filled in a particular college–branch combination in a given round.\n\n"
            "📊 **How to use it:**\n"
            "- A **lower cut-off number** = more competitive (fewer seats, more demand)\n"
            "- A **higher cut-off number** = less competitive\n"
            "- If your rank is *better than (lower than)* the cut-off, you have a good chance\n\n"
            "🔍 **Where to find previous year cut-offs:**\n"
            "- ACPC portal → **Previous Year Data** / **Cut-off Archive** section\n"
            "- These are useful for estimating your chances, but actual cut-offs change every year\n\n"
            "💡 *Use previous year data as a reference, not a guarantee.*"
        ),
    ),

    # ── Fees ─────────────────────────────────────────────────────────────────

    (
        [
            "fee structure acpc",
            "acpc fees",
            "engineering college fees gujarat",
            "how much is the fee",
            "government college fees",
            "private college fees acpc",
            "tuition fee for engineering",
            "acpc registration fee",
        ],
        (
            "**Fee Information for ACPC Gujarat Admissions:**\n\n"
            "💳 **ACPC Registration Fee:** A nominal fee is charged during online registration "
            "(amount is updated each year — check the portal).\n\n"
            "🏛️ **Government Engineering College Fees:**\n"
            "- Fees are **regulated by the Gujarat government**\n"
            "- Generally lower than private colleges\n"
            "- Exact fees are published in the ACPC information brochure each year\n\n"
            "🏢 **Private / Self-Financed College Fees:**\n"
            "- Fees are approved by the **Fee Regulatory Committee (FRC)**\n"
            "- Vary by college and branch\n"
            "- Fee details are available on the ACPC portal and individual college websites\n\n"
            "📄 **Where to check:** ACPC portal → *Information Brochure* → Fee Appendix\n\n"
            "⚠️ *Always verify the latest fee structure on acpcgujarat.ac.in before payment.*"
        ),
    ),

    # ── What the Bot Can Help With ───────────────────────────────────────────

    (
        [
            "what can you help me with",
            "what topics can you answer",
            "what questions can you answer",
            "what can this chatbot do",
            "what can you do",
            "help me with acpc",
            "what are you for",
            "what is this chatbot for",
        ],
        (
            "I'm the **ACPC Gujarat Admissions Chatbot** and I can help you with:\n\n"
            "🎓 **Admissions Process** — Registration, choice filling, seat allotment, reporting\n"
            "📊 **Merit Rank** — How it's calculated, tie-breaking rules\n"
            "📋 **Eligibility** — Academic requirements, entrance exams (JEE/GUJCET)\n"
            "🏛️ **Colleges** — Government, aided, and private college information\n"
            "📁 **Documents** — What documents to prepare and bring\n"
            "🔢 **Cut-offs** — How to interpret and use cut-off ranks\n"
            "🪑 **Reservation** — Category-wise quotas and certificate requirements\n"
            "💰 **Fees** — Fee structure and regulatory information\n"
            "🔄 **Rounds** — Regular rounds, Open Round, freeze/float options\n\n"
            "Just ask me your question and I'll do my best to help! 😊"
        ),
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# ACPC_FAQ_DICT — O(1) lookup dict built from _ACPC_FAQS at import time.
# Do NOT edit this directly; edit _ACPC_FAQS above instead.
# ─────────────────────────────────────────────────────────────────────────────

ACPC_FAQ_DICT: dict[str, str] = {
    trigger: answer
    for triggers, answer in _ACPC_FAQS
    for trigger in triggers
}


# ─────────────────────────────────────────────────────────────────────────────
# SUGGESTED_QUESTIONS — displayed as clickable chips in the chat UI.
# To add a new suggestion: append a string to this list.
# ─────────────────────────────────────────────────────────────────────────────

SUGGESTED_QUESTIONS: list[str] = [
    "What is ACPC?",
    "How to register for ACPC?",
    "Eligibility for ACPC?",
    "Documents required for ACPC?",
    "How is merit rank calculated?",
    "What is choice filling?",
    "How many rounds in ACPC?",
    "What is cut off rank?",
    "Reservation categories in ACPC?",
    "How to freeze seat?",
    "What is open round?",
    "What is GUJCET?",
    "ACPC fees?",
    "What can you help me with?",
]


# ─────────────────────────────────────────────────────────────────────────────
# HINDI FAQ DATA  (हिंदी)
#
# HOW TO FILL:
#   • triggers  — lowercase, normalised Hindi (punctuation stripped, no ?)
#   • answer    — replace TODO string with the full Hindi answer
#   • Chip text in SUGGESTED_QUESTIONS_HI must normalise to one of these triggers
#     via _normalize() in fast_path.py  (punctuation → space, lowercase, strip)
# ─────────────────────────────────────────────────────────────────────────────

_ACPC_FAQS_HI: list[tuple[list[str], str]] = [

    (
        ["acpc क्या है", "acpc गुजरात क्या है", "acpc के बारे में बताएं", "acpc का फुल फॉर्म"],
        (
            "**ACPC** का पूरा नाम **Admission Committee for Professional Courses**, गुजरात राज्य है।\n\n"
            "यह वह आधिकारिक राज्य-स्तरीय संस्था है जो इन पाठ्यक्रमों में *केंद्रीकृत प्रवेश* का प्रबंधन करती है:\n"
            "- इंजीनियरिंग (BE / B.Tech)\n"
            "- फार्मेसी (B.Pharm / D.Pharm)\n"
            "- MBA और MCA\n"
            "- M.Tech और M.Pharm\n\n"
            "सभी पात्र उम्मीदवारों को गुजरात के सरकारी, सहायता प्राप्त और स्व-वित्तपोषित कॉलेजों में "
            "केंद्रीकृत काउंसलिंग में भाग लेने के लिए ACPC पोर्टल पर पंजीकरण अनिवार्य है।"
        ),
    ),

    (
        ["acpc में रजिस्ट्रेशन कैसे करें", "acpc में पंजीकरण कैसे करें", "acpc के लिए आवेदन कैसे करें"],
        (
            "**ACPC पोर्टल पर रजिस्ट्रेशन करने के चरण:**\n\n"
            "1️⃣ **acpcgujarat.ac.in** पर जाएं\n"
            "2️⃣ **New Registration** पर क्लिक करें और अपना व्यक्तिगत और शैक्षणिक विवरण भरें\n"
            "3️⃣ अपना HSC (12वीं) परीक्षा विवरण और JEE Main / GUJCET स्कोर दर्ज करें\n"
            "4️⃣ सभी आवश्यक दस्तावेज़ अपलोड करें (नीचे सूची देखें)\n"
            "5️⃣ **रजिस्ट्रेशन शुल्क** का ऑनलाइन भुगतान करें\n"
            "6️⃣ अपनी **Application ID** और लॉगिन क्रेडेंशियल नोट कर लें\n"
            "7️⃣ अपनी **मेरिट रैंक** प्रकाशित होने की प्रतीक्षा करें\n"
            "8️⃣ मेरिट रैंक घोषित होने के बाद **Choice Filling** (कॉलेज चयन) के लिए आगे बढ़ें\n\n"
            "💡 *रजिस्ट्रेशन जल्दी पूरा करें — अंतिम दिन का इंतज़ार न करें।*"
        ),
    ),

    (
        ["acpc के लिए पात्रता", "acpc पात्रता मानदंड", "acpc के लिए कौन आवेदन कर सकता है"],
        (
            "**ACPC गुजरात के माध्यम से BE / B.Tech के लिए पात्रता मानदंड:**\n\n"
            "📚 **शैक्षणिक:** **भौतिक विज्ञान, रसायन विज्ञान और गणित (PCM)** के साथ HSC (12वीं विज्ञान) पास।\n"
            "📊 **न्यूनतम अंक:**\n"
            "  - जनरल / ओपन: PCM में **कुल 45%**\n"
            "  - अनुसूचित जाति / अनुसूचित जनजाति / एसईबीसी / ईडब्ल्यूएस: PCM में **कुल 40%**\n\n"
            "📝 **प्रवेश परीक्षा:** **JEE Main** या **GUJCET** में वैध स्कोर होना चाहिए।\n"
            "🏠 **अधिवास (Domicile):** गुजरात का निवासी होना चाहिए या पिछले दो वर्षों से गुजरात में अध्ययन किया होना चाहिए (सटीक अधिवास मानदंड के लिए ACPC नियम देखें)।\n\n"
            "ℹ️ *पात्रता विवरण हर साल बदल सकते हैं — हमेशा आधिकारिक ACPC पोर्टल पर सत्यापित करें।*"
        ),
    ),

    (
        ["acpc के लिए दस्तावेज", "acpc के लिए जरूरी दस्तावेज", "acpc दस्तावेज सूची"],
        (
            "**ACPC गुजरात प्रवेश के लिए आवश्यक दस्तावेज़:**\n\n"
            "📄 **शैक्षणिक:**\n"
            "- HSC (12वीं) मार्कशीट और पासिंग सर्टिफिकेट\n"
            "- SSC (10वीं) मार्कशीट और पासिंग सर्टिफिकेट\n"
            "- स्कूल लीविंग सर्टिफिकेट (SLC / ट्रांसफर सर्टिफिकेट)\n"
            "- JEE Main स्कोर कार्ड और/या GUJCET स्कोर कार्ड\n\n"
            "🪪 **पहचान और अधिवास:**\n"
            "- आधार कार्ड\n"
            "- अधिवास (Domicile) / निवास प्रमाण पत्र (गुजरात)\n\n"
            "📋 **श्रेणी प्रमाण पत्र** *(यदि लागू हो)*:\n"
            "- जाति प्रमाण पत्र (SC / ST / SEBC)\n"
            "- नॉन-क्रीमी लेयर सर्टिफिकेट (SEBC)\n"
            "- EWS प्रमाण पत्र (EWS कोटे के लिए)\n"
            "- आय प्रमाण पत्र\n"
            "- शारीरिक विकलांगता (PH) प्रमाण पत्र (यदि लागू हो)\n\n"
            "📸 **अन्य:**\n"
            "- हाल के पासपोर्ट आकार के फोटोग्राफ\n"
            "- प्रोविजनल एडमिशन लेटर (आवंटन के बाद ACPC पोर्टल से मुद्रित)\n\n"
            "💡 *दस्तावेज़ सत्यापन के लिए मूल दस्तावेज़ + स्व-सत्यापित फोटोकॉपी के 3 सेट साथ रखें।*"
        ),
    ),

    (
        ["मेरिट रैंक कैसे बनती है", "मेरिट रैंक की गणना", "acpc मेरिट रैंक फॉर्मूला"],
        (
            "**ACPC मेरिट रैंक की गणना (इंजीनियरिंग — BE/B.Tech):**\n\n"
            "| घटक | वेटेज |\n"
            "|-----------|----------|\n"
            "| Gujcet पर्सेंटाइल | **60%** |\n"
            "| HSC (12वीं बोर्ड) के अंक | **40%** |\n\n"
            "📌 **फॉर्मूला:**\n"
            "`मेरिट स्कोर = (Gujcet पर्सेंटाइल × 0.60) + (HSC PCM% × 0.40)`\n\n"
            "🔄 **टाई-ब्रेकिंग** (जब मेरिट स्कोर समान हों):\n"
            "1. HSC PCM प्रतिशत अधिक होना\n"
            "2. गणित में Gujcet स्कोर अधिक होना\n"
            "3. भौतिकी में Gujcet स्कोर अधिक होना\n"
            "4. जन्म तिथि (बड़े उम्मीदवार को प्राथमिकता)\n\n"
            "ℹ️ *acpcgujarat.ac.in पर वर्तमान फॉर्मूले को सत्यापित करें क्योंकि यह हर साल बदल सकता है।*"
        ),
    ),

    (
        ["चॉयस फिलिंग क्या है", "चॉयस फिलिंग कैसे करें", "acpc में कॉलेज कैसे चुनें"],
        (
            "**Choice Filling (कॉलेज चयन) — यह कैसे काम करता है:**\n\n"
            "Choice filling वह चरण है जहां आप अपने पसंदीदा कॉलेज और ब्रांच संयोजन का चयन करते हैं और उन्हें *रैंक* करते हैं।\n\n"
            "📝 **विकल्प (चॉइस) कैसे भरें:**\n"
            "1. चॉइस-फिलिंग विंडो के दौरान **acpcgujarat.ac.in** पर लॉग इन करें\n"
            "2. स्थान, प्रकार (सरकारी/निजी) या ब्रांच के आधार पर कॉलेजों की खोज करें\n"
            "3. अपनी चॉइस सूची में कॉलेज-ब्रांच के जोड़े जोड़ें\n"
            "4. उन्हें सबसे पसंदीदा (शीर्ष पर) से कम पसंदीदा (सबसे नीचे) तक **खींचें और रैंक करें**\n"
            "5. समय सीमा से पहले अपने विकल्पों को सेव करें और लॉक करें\n\n"
            "✅ **सुझाव (Tips):**\n"
            "- उन सभी कॉलेजों को जोड़ें जिनमें आप वास्तव में जाना चाहते हैं — इसका कोई दंड (पेनल्टी) नहीं है\n"
            "- अपने सपनों के कॉलेज को पहले रखें, फिर सुरक्षित विकल्प नीचे रखें\n"
            "- जब तक आप पूरी तरह संतुष्ट न हों, लॉक न करें — समय सीमा से पहले बदलाव किए जा सकते हैं\n"
            "- एक बार लॉक हो जाने पर, उस राउंड के लिए विकल्पों को नहीं बदला जा सकता"
        ),
    ),

    (
        ["acpc में कितने राउंड", "acpc काउंसलिंग राउंड", "काउंसलिंग में कितने राउंड होते हैं"],
        (
            "**ACPC काउंसलिंग राउंड:**\n\n"
            "ACPC आमतौर पर सीट आवंटन के **3 से 4 राउंड** आयोजित करता है:\n\n"
            "🔁 **नियमित राउंड (राउंड 1, 2, 3):**\n"
            "- मेरिट रैंक वाले सभी पंजीकृत उम्मीदवारों के लिए खुला है\n"
            "- आप प्रत्येक आगामी राउंड में बेहतर सीट पर अपग्रेड (फ्लोट) कर सकते हैं\n"
            "- प्रक्रिया से बाहर निकलने वाले उम्मीदवारों द्वारा खाली की गई सीटें फिर से आवंटन के लिए उपलब्ध हो जाती हैं\n\n"
            "🏁 **ओपन राउंड (मॉप-अप राउंड — अंतिम):**\n"
            "- प्रवेश प्रक्रिया का अंतिम राउंड\n"
            "- **किसी भी योग्य उम्मीदवार** के लिए खुला है (यहां तक ​​कि उनके लिए भी जिन्होंने पहले पंजीकरण नहीं कराया था)\n"
            "- इस राउंड के बाद कोई अपग्रेड नहीं होगा — यहां का आवंटन अंतिम है\n"
            "- शेष रिक्त सीटें यहां भरी जाती हैं\n\n"
            "ℹ️ *प्रत्येक प्रवेश चक्र से पहले ACPC द्वारा राउंड की सटीक संख्या की घोषणा की जाती है।*"
        ),
    ),

    (
        ["कट ऑफ रैंक क्या है", "acpc कट ऑफ", "पिछले साल का कट ऑफ"],
        (
            "**कट-ऑफ रैंक — इसका क्या मतलब है:**\n\n"
            "कट-ऑफ रैंक वह **अंतिम (सबसे अच्छी मेरिट रैंक)** है जिस पर किसी विशिष्ट राउंड में किसी विशेष कॉलेज-ब्रांच संयोजन में कोई सीट भरी गई थी।\n\n"
            "📊 **इसका उपयोग कैसे करें:**\n"
            "- **कट-ऑफ संख्या जितनी कम होगी** = उतनी ही अधिक प्रतिस्पर्धा होगी (कम सीटें, अधिक मांग)\n"
            "- **कट-ऑफ संख्या जितनी अधिक होगी** = उतनी ही कम प्रतिस्पर्धा होगी\n"
            "- यदि आपकी रैंक कट-ऑफ संख्या से *बेहतर (कम)* है, तो आपके पास प्रवेश मिलने की अच्छी संभावना है\n\n"
            "🔍 **पिछले वर्ष के कट-ऑफ कहां मिलेंगे:**\n"
            "- ACPC पोर्टल → **Previous Year Data** (पिछले वर्ष का डेटा) / **Cut-off Archive** (कट-ऑफ संग्रह) अनुभाग\n"
            "- पिछले वर्षों के इस डेटा से अपनी संभावनाओं का अनुमान लगाने में मदद मिल सकती है, लेकिन याद रखें कि वास्तविक कट-ऑफ हर साल बदलती है\n\n"
            "💡 *पिछले वर्ष के डेटा का उपयोग एक संदर्भ के रूप में करें, गारंटी या दावे के रूप में नहीं।*"
        ),
    ),

    (
        ["acpc में आरक्षण", "acpc आरक्षण श्रेणियां", "sc st आरक्षण acpc"],
        (
            "**ACPC गुजरात में आरक्षण श्रेणियां (सरकारी कॉलेजों के लिए):**\n\n"
            "| श्रेणी (Category) | प्रतिशत आरक्षण |\n"
            "|----------|-------------|\n"
            "| SC (अनुसूचित जाति) | 7% |\n"
            "| ST (अनुसूचित जनजाति) | 15% |\n"
            "| SEBC (सामाजिक और शैक्षणिक रूप से पिछड़ा वर्ग) | 27% |\n"
            "| EWS (आर्थिक रूप से कमजोर वर्ग) | 10% |\n"
            "| PH (शारीरिक रूप से विकलांग) | 3% (क्षैतिज आरक्षण) |\n"
            "| पूर्व-सैनिक (Ex-Servicemen) | 1% (क्षैतिज आरक्षण) |\n"
            "| जनरल / ओपन | शेष सीटें |\n\n"
            "📋 **आवश्यक प्रमाण पत्र:**\n"
            "- SC/ST: सक्षम प्राधिकारी (Competent Authority) से जाति प्रमाण पत्र\n"
            "- SEBC: जाति प्रमाण पत्र + नॉन-क्रीमी लेयर प्रमाण पत्र\n"
            "- EWS: EWS प्रमाण पत्र + आय प्रमाण पत्र\n\n"
            "ℹ️ *निजी स्व-वित्तपोषित (प्राइवेट / सेल्फ-फाइनेंस्ड) कॉलेज अलग सीट मैट्रिक्स का पालन करते हैं — ACPC पोर्टल पर जांचें।*"
        ),
    ),

    (
        ["सीट फ्रीज कैसे करें", "acpc में सीट फ्रीज", "फ्रीज और फ्लोट में अंतर"],
        (
            "**फ्रीज (Freeze) बनाम फ्लोट (Float / Upgrade):**\n\n"
            "| विकल्प | इसका क्या अर्थ है |\n"
            "|--------|---------------|\n"
            "| **Freeze** | आप वर्तमान आवंटित सीट को अपनी *अंतिम* पसंद के रूप में स्वीकार करते हैं। आपके लिए ACPC प्रक्रिया समाप्त हो जाती है। अब आपको कॉलेज में रिपोर्ट करना होगा। |\n"
            "| **Float** | आप अस्थायी रूप से वर्तमान सीट को स्वीकार करते हैं लेकिन अगले राउंड में *बेहतर सीट प्राप्त करने का प्रयास* करना चाहते हैं। यदि बेहतर सीट मिलती है, तो आपको वह आवंटित हो जाएगी; अन्यथा आपके पास अभी की सीट बनी रहेगी। |\n\n"
            "💡 **फ्रीज (Freeze) कब करें:**\n"
            "- जब आप आवंटित कॉलेज और ब्रांच से पूरी तरह संतुष्ट हैं\n"
            "- आप सीट खोने का जोखिम नहीं लेना चाहते हैं\n\n"
            "💡 **फ्लोट (Float) कब करें:**\n"
            "- जब आपको किसी ऐसे उच्च-रैंक वाले कॉलेज/ब्रांच की उम्मीद है जो अभी तक आवंटित नहीं हुआ है\n"
            "- आप अगले राउंड तक इंतजार करने को तैयार हैं\n\n"
            "⚠️ *यदि आप समय सीमा के भीतर किसी भी विकल्प (Freeze, Float, या Reject) का चयन नहीं करते हैं, तो आपकी सीट स्वचालित रूप से रद्द की जा सकती है।*"
        ),
    ),

    (
        ["ओपन राउंड क्या है", "acpc ओपन राउंड", "मॉप अप राउंड क्या है"],
        (
            "**ओपन राउंड (मॉप-अप राउंड):**\n\n"
            "ओपन राउंड ACPC काउंसलिंग का **अंतिम राउंड** है।\n\n"
            "📌 **मुख्य विशेषताएं:**\n"
            "- कोई भी पात्र उम्मीदवार भाग ले सकता है — जिसमें वे लोग भी शामिल हैं जिन्होंने पहले पंजीकरण *नहीं* किया था\n"
            "- सभी नियमित राउंड के बाद जो सीटें खाली बची होती हैं, वे यहाँ उपलब्ध होती हैं\n"
            "- ओपन राउंड में **अपग्रेड का कोई विकल्प नहीं** होता है — एक बार सीट आवंटित होने के बाद, आपको रिपोर्ट करना होगा या प्रवेश प्रक्रिया से बाहर निकलना होगा\n"
            "- जिन उम्मीदवारों ने पहले अपनी सीट अस्वीकार (reject) कर दी थी, वे भी इसके लिए आवेदन कर सकते हैं\n\n"
            "⚠️ *जिन उम्मीदवारों ने नियमित राउंड में पहले ही अपनी सीट फ्रीज कर दी है, उन्हें ओपन राउंड में भाग नहीं लेना चाहिए, जब तक कि वे अपनी फ्रीज की हुई सीट को रद्द नहीं करना चाहते।*"
        ),
    ),

    (
        ["gujcet क्या है", "gujcet परीक्षा", "gujcet और jee में अंतर"],
        (
            "**GUJCET** (गुजरात कॉमन एंट्रेंस टेस्ट - Gujarat Common Entrance Test) राज्य स्तर की प्रवेश परीक्षा है जो **GSEB** (गुजरात माध्यमिक और उच्चतर माध्यमिक शिक्षा बोर्ड) द्वारा आयोजित की जाती है।\n\n"
            "📌 **ACPC प्रवेश के लिए:**\n"
            "- मेरिट रैंक की गणना के लिए JEE Main के *विकल्प* के रूप में GUJCET स्कोर का उपयोग किया जा सकता है।\n"
            "- जिन छात्रों ने JEE Main परीक्षा नहीं दी है, वे अपने GUJCET स्कोर का उपयोग कर सकते हैं।\n"
            "- GUJCET और JEE Main दोनों के स्कोर स्वीकार किए जाते हैं; ACPC मेरिट के लिए बेहतर स्कोर वाले विकल्प का उपयोग करता है।\n\n"
            "📅 GUJCET का आयोजन आमतौर पर अप्रैल-मई में किया जाता है। परीक्षा के कार्यक्रम के लिए **gseb.org** की जाँच करें।"
        ),
    ),

    (
        ["acpc की फीस", "इंजीनियरिंग कॉलेज फीस गुजरात", "acpc पंजीकरण शुल्क"],
        (
            "**ACPC गुजरात प्रवेश के लिए शुल्क (Fee) की जानकारी:**\n\n"
            "💳 **ACPC रजिस्ट्रेशन शुल्क (Registration Fee):** ऑनलाइन रजिस्ट्रेशन के दौरान एक मामूली शुल्क लिया जाता है (रकम हर साल अपडेट होती है — पोर्टल पर जांचें)।\n\n"
            "🏛️ **सरकारी इंजीनियरिंग कॉलेजों की फीस:**\n"
            "- फीस **गुजरात सरकार द्वारा निर्धारित** की जाती है\n"
            "- आमतौर पर निजी कॉलेजों की तुलना में काफी कम होती है\n"
            "- सटीक फीस हर साल ACPC सूचना विवरणिका (Information Brochure) में प्रकाशित की जाती है\n\n"
            "🏢 **निजी (प्राइवेट) / स्व-वित्तपोषित कॉलेजों की फीस:**\n"
            "- फीस का अप्रूवल (मंजूरी) **शुल्क नियामक समिति — Fee Regulatory Committee (FRC)** द्वारा किया जाता है\n"
            "- यह कॉलेज और ब्रांच के अनुसार भिन्न हो सकती है\n"
            "- फीस का विवरण ACPC पोर्टल और संबंधित कॉलेज की वेबसाइट्स पर उपलब्ध रहता है\n\n"
            "📄 **कहां जांचें:** ACPC पोर्टल → *Information Brochure (ब्रोशर)* → Fee Appendix (शुल्क परिशिष्ट)\n\n"
            "⚠️ *भुगतान करने से पहले हमेशा acpcgujarat.ac.in पर नवीनतम शुल्क संरचना की पुष्टि ज़रूर करें।*"
        ),
    ),

    (
        ["आप किसमें मदद कर सकते हैं", "आप क्या कर सकते हैं", "यह चैटबॉट किस लिए है"],
        (
            "मैं **ACPC गुजरात प्रवेश चैटबॉट (Admissions Chatbot)** हूं और मैं आपकी इसमें मदद कर सकता हूं:\n\n"
            "🎓 **प्रवेश प्रक्रिया** — पंजीकरण (रजिस्ट्रेशन), चॉइस फिलिंग, सीट आवंटन और रिपोर्टिंग\n"
            "📊 **मेरिट रैंक** — इसकी गणना कैसे की जाती है, टाई-ब्रेकिंग नियम\n"
            "📋 **पात्रता मानदंड (Eligibility)** — शैक्षणिक आवश्यकताएँ, प्रवेश परीक्षाएं (JEE/GUJCET)\n"
            "🏛️ **कॉलेज** — सरकारी, अनुदान प्राप्त और निजी कॉलेजों की जानकारी\n"
            "📁 **दस्तावेज़** — कौन से दस्तावेज़ तैयार करने और अपने साथ लाने हैं\n"
            "🔢 **कट-ऑफ (Cut-offs)** — कट-ऑफ रैंक को कैसे समझें और इसका उपयोग कैसे करें\n"
            "🪑 **आरक्षण (Reservation)** — श्रेणी-वार (Category-wise) कोटा और प्रमाण पत्र संबंधी आवश्यकताएं\n"
            "💰 **फीस** — फीस का ढांचा और विनियामक (Regulatory) जानकारी\n"
            "🔄 **राउंड (Rounds)** — नियमित राउंड, ओपन राउंड, फ्रीज/फ्लोट के विकल्प\n\n"
            "बस आप अपना प्रश्न पूछें और मैं आपकी मदद करने की पूरी कोशिश करूंगा! 😊"
        ),
    ),
]

ACPC_FAQ_DICT_HI: dict[str, str] = {
    trigger: answer
    for triggers, answer in _ACPC_FAQS_HI
    for trigger in triggers
}

SUGGESTED_QUESTIONS_HI: list[str] = [
    "ACPC क्या है?",
    "ACPC में रजिस्ट्रेशन कैसे करें?",
    "ACPC के लिए पात्रता?",
    "ACPC के लिए दस्तावेज?",
    "मेरिट रैंक कैसे बनती है?",
    "चॉयस फिलिंग क्या है?",
    "ACPC में कितने राउंड?",
    "कट ऑफ रैंक क्या है?",
    "ACPC में आरक्षण?",
    "सीट फ्रीज कैसे करें?",
    "ओपन राउंड क्या है?",
    "GUJCET क्या है?",
    "ACPC की फीस?",
    "आप किसमें मदद कर सकते हैं?",
]


# ─────────────────────────────────────────────────────────────────────────────
# GUJARATI FAQ DATA  (ગુજરાતી)
#
# HOW TO FILL:
#   • triggers  — lowercase, normalised Gujarati (punctuation stripped, no ?)
#   • answer    — replace TODO string with the full Gujarati answer
#   • Chip text in SUGGESTED_QUESTIONS_GU must normalise to one of these triggers
# ─────────────────────────────────────────────────────────────────────────────

_ACPC_FAQS_GU: list[tuple[list[str], str]] = [

    (
        ["acpc શું છે", "acpc ગુજરાત શું છે", "acpc વિશે જણાવો", "acpc નું પૂરું નામ"],
        (
            "**ACPC** એટલે **Admission Committee for Professional Courses**, ગુજરાત રાજ્ય.\n\n"
            "આ ગુજરાત સરકારની સત્તાવાર રાજ્ય-સ્તરીય સંસ્થા છે, જે નીચેના અભ્યાસક્રમોમાં "
            "*કેન્દ્રીય પ્રવેશ*નું સંચાલન કરે છે:\n"
            "- એન્જિનિયરિંગ (BE / B.Tech)\n"
            "- ફાર્મસી (B.Pharm / D.Pharm)\n"
            "- MBA અને MCA\n"
            "- M.Tech અને M.Pharm\n\n"
            "ગુજરાત સરકારી, અનુદાનિત અને સ્વ-ભ. કૉલેજોમાં કેન્દ્રીય કાઉન્સેલિંગ માટે "
            "તમામ પાત્ર ઉમેદવારોએ ACPC પોર્ટલ પર નોંધણી કરાવવી ફરજિયાત છે."
        ),
    ),

    (
        ["acpc માં નોંધણી", "acpc માં નોંધણી કેવી રીતે કરવી", "acpc માટે અરજી કેવી રીતે"],
        (
            "**ACPC પોર્ટલ પર નોંધણી કરવાના પગલાં:**\n\n"
            "1️⃣ **acpcgujarat.ac.in** ની મુલાકાત લો\n"
            "2️⃣ **New Registration** પર ક્લિક કરો અને તમારી વ્યક્તિગત અને શૈક્ષણિક વિગતો ભરો\n"
            "3️⃣ તમારી HSC (12મું) પરીક્ષાની વિગતો અને JEE Main / GUJCET સ્કોર દાખલ કરો\n"
            "4️⃣ તમામ જરૂરી દસ્તાવેજો અપલોડ કરો (નીચે સૂચિ જુઓ)\n"
            "5️⃣ **નોંધણી ફી** ઓનલાઇન ચૂકવો\n"
            "6️⃣ તમારું **Application ID** અને લોગીન ક્રેડેન્શિયલ્સ નોંધી લો\n"
            "7️⃣ તમારી **મેરિટ રેન્ક** જાહેર થાય તેની રાહ જુઓ\n"
            "8️⃣ મેરિટ રેન્ક જાહેર થયા પછી **Choice Filling** (કોલેજ પસંદગી) માટે આગળ વધો\n\n"
            "💡 *નોંધણી વહેલા પૂર્ણ કરો - છેલ્લા દિવસની રાહ જોશો નહીં.*"
        ),
    ),

    (
        ["acpc માટે પાત્રતા", "acpc પાત્રતા માપદંડ", "acpc માટે કોણ અરજી કરી શકે"],
        (
            "**ACPC ગુજરાત દ્વારા BE / B.Tech માટેની પાત્રતા માપદંડ:**\n\n"
            "📚 **શૈક્ષણિક:** **ભૌતિકશાસ્ત્ર, રસાયણશાસ્ત્ર અને ગણિત (PCM)** સાથે HSC (12મું વિજ્ઞાન) પાસ.\n"
            "📊 **લઘુત્તમ ગુણ:**\n"
            "  - જનરલ / ઓપન: PCM માં **એકંદર 45%**\n"
            "  - SC / ST / SEBC / EWS: PCM માં **એકંદર 40%**\n\n"
            "📝 **પ્રવેશ પરીક્ષા:** **JEE Main** અથવા **GUJCET** માં માન્ય સ્કોર હોવો આવશ્યક છે.\n"
            "🏠 **રહેઠાણ (Domicile):** ગુજરાતનો રહેવાસી હોવો જોઈએ અથવા છેલ્લા બે વર્ષથી ગુજરાતમાં અભ્યાસ કર્યો હોવો જોઈએ (સચોટ ડોમિસાઇલ માપદંડ માટે ACPC નિયમો જુઓ).\n\n"
            "ℹ️ *પાત્રતાની વિગતો દર વર્ષે બદલાઈ શકે છે — હંમેશા અધિકૃત ACPC પોર્ટલ પર ચકાસો.*"
        ),
    ),

    (
        ["acpc માટે દસ્તાવેજ", "acpc માટે જરૂરી દસ્તાવેજો", "acpc દસ્તાવેજ યાદી"],
        (
            "**ACPC ગુજરાત પ્રવેશ માટે જરૂરી દસ્તાવેજો:**\n\n"
            "📄 **શૈક્ષણિક:**\n"
            "- HSC (12મું) માર્કશીટ અને પાસિંગ સર્ટિફિકેટ\n"
            "- SSC (10મું) માર્કશીટ અને પાસિંગ સર્ટિફિકેટ\n"
            "- સ્કૂલ લિવિંગ સર્ટિફિકેટ (SLC / ટ્રાન્સફર સર્ટિફિકેટ)\n"
            "- JEE Main સ્કોર કાર્ડ અને/અથવા GUJCET સ્કોર કાર્ડ\n\n"
            "🪪 **ઓળખ અને રહેઠાણ:**\n"
            "- આધાર કાર્ડ\n"
            "- રહેઠાણ (Domicile) / નિવાસ પ્રમાણપત્ર (ગુજરાત)\n\n"
            "📋 **શ્રેણી પ્રમાણપત્રો** *(જો લાગુ પડતું હોય)*:\n"
            "- જાતિ પ્રમાણપત્ર (SC / ST / SEBC)\n"
            "- નોન-ક્રીમી લેયર સર્ટિફિકેટ (SEBC)\n"
            "- EWS પ્રમાણપત્ર (EWS ક્વોટા માટે)\n"
            "- આવક પ્રમાણપત્ર\n"
            "- શારીરિક વિકલાંગતા (PH) પ્રમાણપત્ર (જો લાગુ પડતું હોય)\n\n"
            "📸 **અન્ય:**\n"
            "- તાજેતરના પાસપોર્ટ સાઇઝના ફોટોગ્રાફ્સ\n"
            "- પ્રોવિઝનલ એડમિશન લેટર (ફાળવણી પછી ACPC પોર્ટલ પરથી પ્રિન્ટ કરેલ)\n\n"
            "💡 *દસ્તાવેજ ચકાસણી માટે અસલ દસ્તાવેજો + સ્વ-પ્રમાણિત ફોટોકોપીના 3 સેટ સાથે રાખો.*"
        ),
    ),

    (
        ["મેરિટ રેન્ક કેવી ગણાય", "મેરિટ રેન્ક ગણતરી", "acpc મેરિટ રેન્ક ફોર્મ્યુલા"],
        (
            "**ACPC મેરિટ રેન્ક ગણતરી (એન્જિનિયરિંગ — BE/B.Tech):**\n\n"
            "| ઘટક | વેઇટેજ (Weightage) |\n"
            "|-----------|----------|\n"
            "| Gujcet પર્સેન્ટાઇલ | **60%** |\n"
            "| HSC (12મું બોર્ડ) ના માર્ક્સ | **40%** |\n\n"
            "📌 **ફોર્મ્યુલા:**\n"
            "`મેરિટ સ્કોર = (Gujcet પર્સેન્ટાઇલ × 0.60) + (HSC PCM% × 0.40)`\n\n"
            "🔄 **ટાઇ-બ્રેકિંગ** (જ્યારે મેરિટ સ્કોર સમાન હોય): \n"
            "1. વધુ HSC PCM ની ટકાવારી\n"
            "2. ગણિતમાં વધુ Gujcet સ્કોર\n"
            "3. ભૌતિકશાસ્ત્રમાં વધુ Gujcet સ્કોર\n"
            "4. જન્મ તારીખ (મોટા ઉમેદવારને પ્રાધાન્ય આપેલ છે)\n\n"
            "ℹ️ *acpcgujarat.ac.in પર વર્તમાન ફોર્મ્યુલા જ ચકાસો કારણ કે તે દર વર્ષે બદલાઈ શકે છે.*"
        ),
    ),

    (
        ["ચોઈસ ફિલિંગ શું છે", "ચોઈસ ફિલિંગ કેવી રીતે", "acpc માં કૉલેજ કેવી રીતે પસંદ"],
        (
            "**ચોઈસ ફિલિંગ (Choice Filling) — તે કેવી રીતે કામ કરે છે:**\n\n"
            "ચોઈસ ફિલિંગ એ તબક્કો છે જ્યાં તમે તમારી પસંદગીના કૉલેજ-બ્રાન્ચ સંયોજનો પસંદ કરો છો અને તેમને *રેન્ક* આપો છો.\n\n"
            "📝 **ચોઈસ કેવી રીતે ભરવી:**\n"
            "1. ચોઈસ-ફિલિંગ વિન્ડો દરમિયાન **acpcgujarat.ac.in** પર લૉગ ઇન કરો\n"
            "2. સ્થાન, પ્રકાર (સરકારી/ખાનગી) અથવા બ્રાન્ચ દ્વારા કૉલેજો શોધો\n"
            "3. તમારી ચોઈસ યાદીમાં કૉલેજ-બ્રાન્ચ ઉમેરો\n"
            "4. તેમને સૌથી વધુ પસંદગીના (ટોચ પર) થી ઓછી પસંદગીના (તળિયે) **ખેંચો અને રેન્ક આપો (ડ્રેગ કરો)**\n"
            "5. છેલ્લી તારીખ પહેલાં તમારી પસંદગીઓ સાચવો અને લોક કરો\n\n"
            "✅ **ટિપ્સ:**\n"
            "- એવી તમામ કૉલેજો ઉમેરો જે આપ ખરેખર જવા માંગો છો — તેનો કોઈ દંડ (પેનલ્ટી) નથી\n"
            "- તમારી મનપસંદ ડ્રીમ કૉલેજ પહેલા રાખો, અને સુરક્ષિત વિકલ્પો નીચે રાખો\n"
            "- જ્યાં સુધી તમે પૂર્ણ સંતુષ્ટ ન હોવ ત્યાં સુધી લૉક કરશો નહીં — છેલ્લી તારીખ પહેલાં ફેરફારો કરી શકાય છે\n"
            "- એકવાર લૉક થઈ ગયા પછી, તે રાઉન્ડ માટે પસંદગીઓ બદલી શકાતી નથી"
        ),
    ),

    (
        ["acpc માં કેટલા રાઉન્ડ", "acpc કાઉન્સેલિંગ રાઉન્ડ", "કાઉન્સેલિંગ માં કેટલા રાઉન્ડ"],
        (
            "**ACPC કાઉન્સેલિંગ રાઉન્ડ:**\n\n"
            "ACPC સામાન્ય રીતે સીટ ફાળવણીના ચાર જેટલા **3 થી 4 રાઉન્ડ** આયોજિત કરે છે:\n\n"
            "🔁 **નિયમિત રાઉન્ડ (રાઉન્ડ 1, 2, 3):**\n"
            "- મેરિટ રેન્ક ધરાવતા તમામ નોંધાયેલા ઉમેદવારો માટે ખુલ્લું છે\n"
            "- તમે દરેક આગામી રાઉન્ડમાં વધુ સારી બેઠક (સીટ) પર અપગ્રેડ (ફ્લોટ) કરી શકો છો\n"
            "- બહાર નીકળતા ઉમેદવારો દ્વારા ખાલી થયેલી બેઠકો પાછી ફાળવણી માટે ઉપલબ્ધ થાય છે\n\n"
            "🏁 **ઓપન રાઉન્ડ (મોપ-અપ રાઉન્ડ — અંતિમ):**\n"
            "- પ્રવેશ પ્રક્રિયાનો છેલ્લો રાઉન્ડ\n"
            "- **કોઈપણ લાયક ઉમેદવાર** માટે ખુલ્લું છે (જેમણે અગાઉ નોંધણી ન કરી હોય તેમના માટે પણ)\n"
            "- આ રાઉન્ડ પછી કોઈ અપગ્રેડની સુવિધા નથી — ફાળવણી અંતિમ ગણાશે\n"
            "- બાકી રહેલી ખાલી બેઠકો આ રાઉન્ડમાં ભરવામાં આવે છે\n\n"
            "ℹ️ *દરેક પ્રવેશ પ્રક્રિયા પહેલા ACPC દ્વારા રાઉન્ડની ચોક્કસ સંખ્યાની જાહેરાત કરવામાં આવે છે.*"
        ),
    ),

    (
        ["કટ ઓફ રેન્ક શું છે", "acpc કટ ઓફ", "ગત વર્ષ કટ ઓફ"],
        (
            "**કટ-ઓફ રેન્ક — તેનો અર્થ શું થાય છે:**\n\n"
            "કટ-ઓફ રેન્ક એ એવી **છેલ્લી (સૌથી વધુ સંખ્યા ધરાવતી) મેરિટ રેન્ક** છે કે જેના પર કોઈ ચોક્કસ રાઉન્ડમાં, કોઈ ચોક્કસ કૉલેજ-બ્રાન્ચ સંયોજનમાં શૈક્ષણિક બેઠક (સીટ) ફાળવણી થયેલી હતી.\n\n"
            "📊 **તેનો ઉપયોગ કેવી રીતે કરવો:**\n"
            "- **નાના કટ-ઓફ નંબર** = વધુ સ્પર્ધા (ઓછી બેઠકો, વધુ માંગ)\n"
            "- **મોટા કટ-ઓફ નંબર** = ઓછી સ્પર્ધા\n"
            "- જો તમારો રેન્ક કટ-ઓફ કરતા *સારો (ઓછો)* હોય, તો તમારા પ્રવેશ માટે સારી તક રહેલી છે\n\n"
            "🔍 **અગાઉના વર્ષના કટ-ઓફ ક્યાં જોવા મળશે:**\n"
            "- ACPC પોર્ટલ → **Previous Year Data** (ગત વર્ષનો ડેટા) / **Cut-off Archive** (કટ-ઓફ આર્કાઇવ) વિભાગમાં\n"
            "- આ આંકડાઓ તમારી તકોનો અંદાજ લગાવવા માટે ઉપયોગી છે, પરંતુ વાસ્તવિક કટ-ઓફ દર વર્ષે બદલાય છે\n\n"
            "💡 *અગાઉના વર્ષના ડેટાનો ઉપયોગ એક માત્ર સંદર્ભ તરીકે કરો, કોઈ બાંયધરી તરીકે નહીં.*"
        ),
    ),

    (
        ["acpc માં અનામત", "acpc અનામત શ્રેણીઓ", "sc st અનામત acpc"],
        (
            "**ACPC ગુજરાતમાં અનામત શ્રેણીઓ (સરકારી કૉલેજો માટે):**\n\n"
            "| શ્રેણી (Category) | અનામત ટકાવારી |\n"
            "|----------|-------------|\n"
            "| SC (અનુસૂચિત જાતિ) | 7% |\n"
            "| ST (અનુસૂચિત જનજાતિ) | 15% |\n"
            "| SEBC (સામાજિક અને શૈક્ષણિક રીતે પછાત વર્ગ) | 27% |\n"
            "| EWS (આર્થિક રીતે નબળો વર્ગ) | 10% |\n"
            "| PH (શારીરિક રીતે વિકલાંગ) | 3% (આડી / આંતરિક અનામત) |\n"
            "| માજી-સૈનિકો (Ex-Servicemen) | 1% (આડી / આંતરિક અનામત) |\n"
            "| જનરલ / ઓપન | બાકી રહેલી બેઠકો |\n\n"
            "📋 **જરૂરી પ્રમાણપત્રો:**\n"
            "- SC/ST: સક્ષમ અધિકારી દ્વારા જારી કરાયેલ જાતિ પ્રમાણપત્ર\n"
            "- SEBC: જાતિ પ્રમાણપત્ર + નોન-ક્રીમી લેયર સર્ટિફિકેટ\n"
            "- EWS: EWS પ્રમાણપત્ર + આવક પ્રમાણપત્ર\n\n"
            "ℹ️ *ખાનગી સ્વ-નિર્ભર (સેલ્ફ-ફાઈનાન્સ્ડ) કૉલેજો અલગ સીટ મેટ્રિક્સનું પાલન કરે છે — ACPC પોર્ટલ પર તપાસો.*"
        ),
    ),

    (
        ["સીટ ફ્રીઝ કેવી રીતે", "acpc માં સીટ ફ્રીઝ", "ફ્રીઝ અને ફ્લોટ ફરક"],
        (
            "**ફ્રીઝ (Freeze) વિરુદ્ધ ફ્લોટ (Float / Upgrade):**\n\n"
            "| વિકલ્પ | તેનો અર્થ શું થાય છે |\n"
            "|--------|---------------|\n"
            "| **Freeze** | તમે હાલમાં ફાળવેલ સીટ (બેઠક) ને તમારી *અંતિમ પસંદગી* તરીકે સ્વીકારો છો. તમારા માટે ACPC પ્રવેશ પ્રક્રિયા પૂર્ણ થાય છે. હવે તમારે કૉલેજમાં રૂબરૂ હાજર થવું પડશે. |\n"
            "| **Float** | તમે અસ્થાયી ધોરણે હાલની સીટ સ્વીકારો છો પરંતુ આગામી રાઉન્ડમાં *વધુ સારી સીટ માટે પ્રયાસ* કરવા માંગો છો. જો વધુ સારી સીટ મળે તો, તે તમને ફાળવવામાં આવશે; અન્યથા તમારી પાસે વર્તમાન સીટ તો રહેશે જ. |\n\n"
            "💡 **ફ્રીઝ (Freeze) ક્યારે કરવું:**\n"
            "- જ્યારે તમે ફાળવવામાં આવેલી કૉલેજ અને બ્રાન્ચથી સંતુષ્ટ હોવ\n"
            "- તમે તમારી સીટ ગુમાવવાનું જોખમ લેવા નથી માંગતા\n\n"
            "💡 **ફ્લોટ (Float) ક્યારે કરવું:**\n"
            "- જ્યારે તમે એવી ઉચ્ચ-રેન્કવાળી પસંદગી મેળવવા માંગતા હોવ જે હજુ સુધી તમને મળી નથી\n"
            "- તમે પછીના રાઉન્ડની રાહ જોવા તૈયાર છો\n\n"
            "⚠️ *જો તમે નિર્ધારિત સમય મર્યાદાની અંદર કોઈ પણ વિકલ્પ (ફ્રીઝ, ફ્લોટ કે રિજેક્ટ) પસંદ નહીં કરો, તો તમારી સીટ આપમેળે રદ થઈ જશે.*"
        ),
    ),

    (
        ["ઓપન રાઉન્ડ શું છે", "acpc ઓપન રાઉન્ડ", "મૉપ અપ રાઉન્ડ શું છે"],
        (
            "**ઓપન રાઉન્ડ (મોપ-અપ રાઉન્ડ):**\n\n"
            "ઓપન રાઉન્ડ એ ACPC કાઉન્સેલિંગનો **અંતિમ રાઉન્ડ** છે.\n\n"
            "📌 **મુખ્ય વિશેષતાઓ:**\n"
            "- કોઈપણ લાયક ઉમેદવાર ભાગ લઈ શકે છે — એવા પણ ઉમેદવારો પણ ભાગ લઇ શકે છે જેઓએ અગાઉ નોંધણી *ન* કરી હોય\n"
            "- તમામ નિયમિત રાઉન્ડ પછી બાકી રહેલી બેઠકો જ આ રાઉન્ડમાં ખાલી ગણાશે\n"
            "- ઓપન રાઉન્ડમાં **અપગ્રેડ માટેનો કોઈ વિકલ્પ નથી** — એકવાર સીટ ફાળવવામાં આવ્યા પછી, તમારે કૉલેજમાં રિપોર્ટ કરવું પડશે અથવા પ્રક્રિયા છોડવી પડશે\n"
            "- જે ઉમેદવારોએ અગાઉ તેમની સીટ નકારી કાઢી હોય (reject કરી હોય), તેઓ પણ આમાં અરજી કરી શકે છે\n\n"
            "⚠️ *જે ઉમેદવારોએ નિયમિત રાઉન્ડમાં પહેલેથી જ સીટ ફ્રીઝ કરી હોય, તેઓએ ઓપન રાઉન્ડમાં ભાગ લેવો જોઈએ નહીં. (સિવાય કે તેઓ તેમની ફ્રીઝ કરેલી સીટ રદ કરવા માંગતા હોય).*"
        ),
    ),

    (
        ["gujcet શું છે", "gujcet પરીક્ષા", "gujcet અને jee ફરક"],
        (
            "**GUJCET** (ગુજરાત કોમન એન્ટ્રન્સ ટેસ્ટ) એ **GSEB** (ગુજરાત માધ્યમિક અને ઉચ્ચતર માધ્યમિક શિક્ષણ બોર્ડ) દ્વારા લેવામાં આવતી રાજ્ય-કક્ષાની પ્રવેશ પરીક્ષા છે.\n\n"
            "📌 **ACPC માં પ્રવેશ માટે:**\n"
            "- મેરિટ રેન્ક ગણતરી માટે GUJCET ના સ્કોરના ઉપયોગ JEE Main ના *વિકલ્પ* તરીકે કરી શકાય છે.\n"
            "- જે વિદ્યાર્થીઓએ JEE Main ની પરીક્ષા નથી આપી, તેઓ તેમના GUJCET ના સ્કોરનો ઉપયોગ કરી શકે છે.\n"
            "- GUJCET અને JEE Main બંનેના સ્કોર માન્ય છે; ACPC મેરિટ માટે તમારા વધુ સારા સ્કોરનો જ ઉપયોગ કરશે.\n\n"
            "📅 GUJCET સામાન્ય રીતે એપ્રિલ-મે મહિનામાં લેવામાં આવે છે. પરીક્ષાના સમયપત્રક માટે **gseb.org** તપાસો."
        ),
    ),

    (
        ["acpc ની ફી", "એન્જિનિયરિંગ કૉલેજ ફી ગુજરાત", "acpc નોંધણી ફી"],
        (
            "**ACPC ગુજરાત પ્રવેશ માટે ફી સંબંધિત માહિતી:**\n\n"
            "💳 **ACPC નોંધણી ફી (Registration Fee):** ઓનલાઇન નોંધણી (રજિસ્ટ્રેશન) દરમિયાન એક નજીવી ફી વસૂલવામાં આવે છે (ફી ની રકમ દર વર્ષે અપડેટ થાય છે - કૃપા કરીને પોર્ટલ પર તપાસો).\n\n"
            "🏛️ **સરકારી એન્જિનિયરિંગ કોલેજોની ફી:**\n"
            "- સરકારી કોલેજોની ફી **ગુજરાત સરકાર દ્વારા નિર્ધારિત (Regulated)** કરવામાં આવે છે\n"
            "- ખાનગી કોલેજોની સરખામણીમાં આ ફી સામાન્ય રીતે ઘણી ઓછી હોય છે\n"
            "- સચોટ ફી દર વર્ષે ACPC ઇન્ફોર્મેશન બ્રોશરમાં પ્રકાશિત કરવામાં આવે છે\n\n"
            "🏢 **ખાનગી (Private) / સ્વનિર્ભર કોલેજોની ફી:**\n"
            "- ફી **ફી રેગ્યુલેટરી કમિટી — Fee Regulatory Committee (FRC)** દ્વારા મંજૂર કરવામાં આવે છે\n"
            "- ફી દરેક કૉલેજ અને બ્રાન્ચ મુજબ અલગ-અલગ હોઈ શકે છે\n"
            "- ફી ની વિગતો ACPC પોર્ટલ અને વ્યક્તિગત કૉલેજની વેબસાઇટ પર ઉપલબ્ધ હોય છે\n\n"
            "📄 **ક્યાં તપાસવું:** ACPC પોર્ટલ → *Information Brochure (માહિતી પુસ્તિકા)* → Fee Appendix (ફી પરિશિષ્ટ)\n\n"
            "⚠️ *ચુકવણી (Payment) કરતા પહેલા હંમેશા acpcgujarat.ac.in પર લેટેસ્ટ ફી સ્ટ્રક્ચર જરૂર ચકાસો.*"
        ),
    ),

    (
        ["તમે શું મદદ કરી શકો", "આ ચેટબૉટ શું કરે", "તમે શેમાં મદદ કરો"],
        (
            "હું **ACPC ગુજરાત એડમિશન ચેટબૉટ (Admissions Chatbot)** છું અને નીચે મુજબની બાબતોમાં હું તમારી મદદ કરી શકું છું:\n\n"
            "🎓 **પ્રવેશ પ્રક્રિયા** — નોંધણી (રજિસ્ટ્રેશન), ચોઈસ ફિલિંગ, સીટ ફાળવણી, રિપોર્ટિંગ\n"
            "📊 **મેરિટ રેન્ક** — મેરિટની ગણતરી કેવી રીતે કરવામાં આવે છે અને ટાઈ-બ્રેકિંગ નિયમો\n"
            "📋 **પાત્રતા (Eligibility)** — શૈક્ષણિક જરૂરિયાતો, પ્રવેશ પરીક્ષાઓ (JEE/GUJCET) ની માહિતી\n"
            "🏛️ **કૉલેજ** — સરકારી, અનુદાનિત (ગ્રાન્ટ-ઈન-એઈડ), અને ખાનગી કૉલેજોની માહિતી\n"
            "📁 **દસ્તાવેજો** — કયા દસ્તાવેજો તૈયાર કરવા અને સાથે લાવવા\n"
            "🔢 **કટ-ઓફ (Cut-offs)** — કટ-ઓફ રેન્ક કેવી રીતે સમજવો અને તેનો ઉપયોગ કેવી રીતે કરવો\n"
            "🪑 **અનામત (Reservation)** — ઑપન, બક્ષીપંચ, અનુસૂચિત જાતિ/જનજાતિ માટેનો ક્વોટા અને પ્રમાણપત્રોની જરૂરિયાતો\n"
            "💰 **ફી (Fees)** — ફી માળખું અને રૅગ્યુલેટરી નિયમોની માહિતી\n"
            "🔄 **રાઉન્ડ (Rounds)** — નિયમિત કાઉન્સેલિંગ રાઉન્ડ, ઓપન રાઉન્ડ, ફ્રીઝ/ફ્લોટ ટિપ્સ\n\n"
            "બસ મને તમારો પ્રશ્ન પૂછો અને હું તમારી મદદ કરવાનો પૂરેપૂરો પ્રયાસ કરીશ! 😊"
        ),
    ),
]

ACPC_FAQ_DICT_GU: dict[str, str] = {
    trigger: answer
    for triggers, answer in _ACPC_FAQS_GU
    for trigger in triggers
}

SUGGESTED_QUESTIONS_GU: list[str] = [
    "ACPC શું છે?",
    "ACPC માં નોંધણી?",
    "ACPC માટે પાત્રતા?",
    "ACPC માટે દસ્તાવેજ?",
    "મેરિટ રેન્ક કેવી ગણાય?",
    "ચોઈસ ફિલિંગ શું છે?",
    "ACPC માં કેટલા રાઉન્ડ?",
    "કટ ઓફ રેન્ક શું છે?",
    "ACPC માં અનામત?",
    "સીટ ફ્રીઝ કેવી રીતે?",
    "ઓપન રાઉન્ડ શું છે?",
    "GUJCET શું છે?",
    "ACPC ની ફી?",
    "તમે શું મદદ કરી શકો?",
]
