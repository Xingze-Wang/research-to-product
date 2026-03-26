# The Open Source Trap

**How your Day-1 license choice determines your Day-1000 exit options.**

## TL;DR

Most researcher-founders open-source their code under MIT or Apache on Day 1 because "that's what everyone does." Then, 18 months later, they discover their competitor forked their repo, slapped a UI on it, and is selling it to their customers.

**Your license is not a technical decision. It's a business decision.** Treat it like one.

## The Three Paths

### Path 1: Full Open Source (MIT / Apache 2.0)

**What it means:** Anyone can use, modify, sell your code. No restrictions.

**When it makes sense:**
- Your moat is data, not code (e.g., you have proprietary training data)
- Your moat is speed of execution (you're 12 months ahead)
- You're building a developer platform (adoption > revenue right now)
- You're pre-product and need community validation

**When it will kill you:**
- Your code IS the product (model architecture, novel algorithm)
- You have no other moat
- A well-funded competitor can out-engineer you

**Real examples:** PyTorch, Hugging Face Transformers, LangChain. Note: all of these have *other moats* (ecosystem, data, brand).

### Path 2: Copyleft (AGPL / GPL)

**What it means:** Anyone who uses your code must also open-source their code. Cloud companies can't just wrap your code in an API.

**When it makes sense:**
- You want community contributions but don't want AWS to eat your lunch
- You plan to sell commercial licenses (dual licensing)
- Your users are developers who understand GPL

**When it's tricky:**
- Enterprise customers may refuse to touch GPL code (legal departments hate it)
- In China, GPL enforcement is practically impossible
- It can slow adoption in corporate environments

**Real examples:** Linux (GPL), MongoDB (SSPL — they switched *because* AWS was eating their lunch).

### Path 3: Source Available (BSL / SSPL / Elastic License)

**What it means:** Code is visible, but commercial use requires a license. Often converts to full open source after a delay (e.g., 3 years).

**When it makes sense:**
- You want the trust benefits of visible source code
- You need to protect revenue from cloud providers
- You're building infrastructure (databases, ML serving, etc.)

**When it's risky:**
- Community contributions dry up (people don't want to contribute to "not-really-open" projects)
- Some package managers / Linux distros won't distribute BSL software
- VCs may push back (perceived as "less open")

**Real examples:** Elastic, CockroachDB, Sentry, HashiCorp (Terraform).

## Decision Framework

Ask yourself these questions:

1. **Is my code the moat, or is something else the moat?**
   - Code is the moat → BSL or AGPL
   - Data/brand/speed is the moat → MIT/Apache is fine

2. **Who are my first 100 customers?**
   - Developers → MIT/Apache (maximize adoption)
   - Enterprises → BSL is fine (they're used to buying licenses)

3. **Am I in a market where a cloud provider will clone me?**
   - Yes → AGPL or BSL
   - No → MIT/Apache

4. **Do I need community contributions to win?**
   - Critical → MIT/Apache
   - Nice to have → BSL/AGPL

## The China-Specific Angle

A few things that are different in China:

- **GPL enforcement is weak.** Don't rely on GPL to protect you in the Chinese market. If your competitor is in China and doesn't care about GPL, you have no practical recourse.
- **"Open source" is a marketing tool** in China more than a philosophy. Many Chinese tech companies open-source to recruit, not to build community.
- **Government procurement** sometimes requires "domestic open source." This affects your licensing strategy if you're selling to SOEs.

## The Bottom Line

| Situation | Recommended License |
|---|---|
| Pre-product, need validation | MIT / Apache 2.0 |
| Code is the product, VC-backed | BSL (converts to Apache after 3y) |
| Developer tool, need adoption | Apache 2.0 |
| Infrastructure, afraid of AWS | AGPL or SSPL |
| Dual-licensing business model | AGPL + commercial license |

**Don't overthink this on Day 1, but don't ignore it either.** The worst outcome is changing your license later (see: HashiCorp, Elastic — both got massive community backlash).

Pick one. Write it in your README. Move on to building.
