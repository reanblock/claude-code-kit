---
name: startup-research
description: "Perform comprehensive research for a startup idea and produce a detailed markdown report. Use this skill whenever the user describes a startup idea, business concept, app idea, SaaS product, or entrepreneurial venture they want to evaluate. Triggers include: phrases like 'startup idea', 'business idea', 'I want to build', 'is this a good idea', 'research this concept', 'validate my idea', 'market research for', 'feasibility study', or any description of a product/service the user is considering building as a business. Also triggers when the user asks about target markets, competitive landscapes, go-to-market strategy, or MVP planning for a new venture. Do NOT use for researching existing public companies, stock analysis, or general business questions unrelated to evaluating a new startup concept."
model: sonnet
effort: low
disallowed-tools: [Agent]
---

# Startup Research Skill

## Purpose

When a user provides a short description of a startup idea, this skill produces a comprehensive research document as a markdown (.md) file. The goal is to give the user a firm, honest understanding of the viability, risks, opportunities, market dynamics, build effort, and post-launch realities of pursuing the idea — so they can make an informed go/no-go decision.

## Workflow

1. Receive the user's startup idea (a short description — even one sentence is enough).
2. Use web search to gather current, real-world data on the market, competitors, trends, and relevant regulations.
3. Synthesize findings into a structured markdown report.
4. Save the report to `/projects/<idea-slug>-startup-research.md` and present it to the user.

## Research Process

When conducting the research, perform the following steps:

### Step 1: Clarify and Expand the Idea
Take the user's short description and infer the core value proposition, the problem being solved, and who it's being solved for. If the idea is ambiguous, make reasonable assumptions and state them explicitly in the report. Do NOT ask the user a bunch of clarifying questions — instead, make smart assumptions and note them so the user can correct anything off-base.

### Step 2: Web Research
Use web search to find:
- Current market size and growth projections for the relevant industry
- Existing competitors (direct and indirect) — names, funding, traction, pricing
- Recent news, trends, and shifts in the space
- Relevant regulations or compliance requirements
- Failure stories and common pitfalls in this space
- Technology stack trends and open-source tools relevant to building the product

### Step 3: Write the Report
Produce the report following the structure defined below.

---

## Report Structure

ALWAYS use this exact structure for the output markdown file:

```markdown
# Startup Research Report: [Idea Name]

> **Idea Summary:** [One-paragraph restatement of the idea in clear terms]
> **Date:** [Current date]
> **Status:** Research Phase

---

## 1. Problem & Value Proposition

Clearly articulate the problem this startup solves. Why does this problem matter? Who feels the pain most acutely? What is the cost of the problem remaining unsolved (in money, time, frustration, risk, etc.)? Frame the value proposition in one sentence: "We help [target user] achieve [outcome] by [mechanism], unlike [current alternatives] which [limitation]."

## 2. Target Market & User Base

### 2.1 Primary User Persona
Define the specific niche user this product serves. Be precise — not "businesses" but "independent physical therapy clinics with 2-10 practitioners" or not "students" but "undergraduate STEM students at universities with 10,000+ enrollment." Include:
- **Who they are**: Role, demographics, professional context
- **Where they are**: Geography, platforms they use, communities they belong to
- **How many there are**: Estimated total addressable users in this niche
- **What they currently do**: How they solve (or fail to solve) the problem today
- **Willingness to pay**: What they currently spend on adjacent solutions

### 2.2 Market Segmentation
Break the broader market into segments. Identify which segment to target first (beachhead market) and why. Show the expansion path from niche to broader market over time.

### 2.3 Total Addressable Market (TAM), Serviceable Addressable Market (SAM), Serviceable Obtainable Market (SOM)
Provide estimates with sources. Be honest about uncertainty — give ranges rather than false precision.

## 3. Competitive Landscape

### 3.1 Direct Competitors
For each direct competitor, include:
- Name, website, founding year
- Funding raised (if known)
- Pricing model and price points
- Key features and differentiators
- Known weaknesses or gaps (from reviews, forums, social media)
- Estimated market share or user base (if available)

### 3.2 Indirect Competitors & Substitutes
What are people using instead, even if it's spreadsheets, pen-and-paper, or ignoring the problem? These are often the real competition for early-stage startups.

### 3.3 Competitive Advantage & Moat
What would make this startup defensible? Consider: network effects, data advantages, switching costs, brand, regulatory barriers, proprietary technology, or speed of execution. Be honest if there is no clear moat — that's important to know.

## 4. Business Model & Revenue

### 4.1 Recommended Revenue Model
Suggest the most appropriate revenue model (SaaS subscription, freemium, marketplace commission, usage-based, licensing, etc.) and explain why it fits this market and user base.

### 4.2 Pricing Strategy
Suggest a pricing range based on competitor analysis, willingness-to-pay signals, and the value delivered. Include thoughts on free tier vs. paid-only, annual vs. monthly, per-seat vs. flat rate.

### 4.3 Unit Economics (Estimated)
Provide rough estimates for:
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- LTV:CAC ratio
- Gross margin expectations
- Payback period

State assumptions clearly.

## 5. Risks & Challenges

### 5.1 Market Risks
- Is the market growing, shrinking, or stagnant?
- Could a major platform (Google, Apple, Microsoft, etc.) build this as a feature?
- Are there regulatory changes on the horizon that could help or hurt?

### 5.2 Execution Risks
- What are the hardest technical challenges?
- Are there talent/hiring risks?
- What are the biggest unknowns?

### 5.3 Financial Risks
- How capital-intensive is this to build and operate?
- What's the burn rate likely to look like?
- How long until break-even at various growth scenarios?

### 5.4 Honest Assessment: Why This Might Fail
List the top 3-5 reasons this startup could fail. Don't sugarcoat. Founders need to hear this.

## 6. Strengths & Opportunities

### 6.1 Why This Might Work
List the top 3-5 reasons this idea has potential. What tailwinds exist? What timing advantages are present?

### 6.2 Unfair Advantages to Cultivate
What advantages could the founder develop over time that would be difficult for competitors to replicate?

## 7. Build Plan & Timeline

### 7.1 MVP Scope
Define the minimum viable product — the smallest thing you can build that delivers the core value proposition and lets you test demand. List the core features (3-7 max) and explicitly call out what is NOT in the MVP.

### 7.2 Recommended Tech Stack
Suggest a modern, pragmatic tech stack appropriate for the product type. Favor speed-to-market and developer productivity over perfection. Consider:
- Frontend framework
- Backend / API
- Database
- Hosting / Infrastructure
- Key third-party services (auth, payments, email, etc.)
- AI/ML components (if applicable)

### 7.3 Development Timeline Estimate (Agentic Engineer)
Provide a realistic timeline assuming the builder is a skilled engineer using AI-assisted / agentic coding tools (e.g., Claude Code, Cursor, Copilot). Break it down by phase:

| Phase | Description | Estimated Duration |
|-------|-------------|-------------------|
| Phase 1: Core MVP | [Core features] | X weeks |
| Phase 2: Polish & Launch-Ready | [Auth, payments, onboarding, basic analytics] | X weeks |
| Phase 3: Feedback & Iteration | [User testing, bug fixes, top feature requests] | X weeks |
| Phase 4: Growth Features | [Features that enable scale — integrations, admin tools, API] | X weeks |
| **Total to Market-Ready Product** | | **X weeks** |

Include a note about the difference between "code complete" and "market ready" — the latter includes testing, documentation, legal compliance, and launch preparation.

### 7.4 Development Timeline Estimate (Traditional Team)
For comparison, provide a rough estimate for a traditional 2-3 person engineering team without heavy AI assistance. This helps the user understand the leverage they get from agentic tools.

## 8. Post-Build: Go-to-Market Strategy

### 8.1 Pre-Launch (Build Demand Before You Ship)
- Landing page and waitlist strategy
- Content marketing / SEO groundwork
- Community engagement (Reddit, forums, Discord, LinkedIn groups relevant to the niche)
- Beta user recruitment — where to find the first 10-50 users

### 8.2 Launch Strategy
- Recommended launch channels (Product Hunt, Hacker News, niche communities, social media)
- Launch day playbook: what to prepare, what to post, how to handle feedback
- PR and press outreach considerations

### 8.3 Marketing & Growth Channels
Rank the following channels by expected effectiveness for this specific startup and user base. For each recommended channel, explain WHY it fits and give a concrete first action:
- Content marketing / SEO
- Social media (specify which platforms and why)
- Paid advertising (Google Ads, Meta, LinkedIn, etc.)
- Partnerships and integrations
- Referral programs
- Cold outreach
- Community-led growth
- Influencer / creator partnerships
- Conference and event presence

### 8.4 Sales Strategy
- Is this product-led growth (self-serve) or sales-led?
- If sales-led: what does the sales motion look like? Inside sales vs. field sales?
- If product-led: what's the conversion funnel from free to paid?
- When should the founder consider hiring the first salesperson?

### 8.5 Customer Engagement & Retention
- Onboarding: How to get users to the "aha moment" quickly
- Engagement loops: What keeps users coming back?
- Feedback collection: How to systematically gather and prioritize user feedback
- Churn prevention: Early warning signs and intervention strategies
- Community building: Should there be a user community? What platform?

### 8.6 Customer Support Strategy
- Support channels appropriate for the stage (email, chat, help docs, community forum)
- Self-serve resources to build early (FAQ, knowledge base, video tutorials)
- When to hire first support person
- Tools to consider (Intercom, Zendesk, plain email, etc.)
- SLA expectations for this market

## 9. Financial Overview

### 9.1 Estimated Startup Costs
Break down costs to get to launch:
- Development costs (if hiring vs. building yourself)
- Infrastructure and tooling
- Legal (incorporation, terms of service, privacy policy)
- Design and branding
- Initial marketing budget

### 9.2 Monthly Operating Costs (Post-Launch)
Estimate monthly burn at different stages:
- Pre-revenue
- Early traction (first 100 paying customers)
- Growth phase (1,000+ customers)

### 9.3 Funding Considerations
- Can this be bootstrapped? Should it be?
- If fundraising: what stage, how much, from whom?
- Alternative funding: grants, competitions, revenue-based financing

## 10. Key Metrics to Track

List the 5-8 most important metrics for this specific startup, organized by stage:

**Pre-Launch:** (e.g., waitlist signups, landing page conversion rate)
**Post-Launch:** (e.g., activation rate, DAU/MAU, NPS, churn rate, MRR)
**Growth Phase:** (e.g., CAC by channel, LTV:CAC, expansion revenue, viral coefficient)

## 11. Recommended Next Steps

Provide a prioritized, actionable list of 5-10 things the user should do in the next 30 days to move forward with validating and building this idea. Be specific and practical — not generic advice like "talk to customers" but "post in [specific subreddit/community] asking [specific question] to validate [specific assumption]."

## 12. Summary Scorecard

| Dimension | Rating (1-10) | Notes |
|-----------|:---:|-------|
| Problem Severity | X | [brief note] |
| Market Size | X | [brief note] |
| Competition Intensity | X | [brief note] |
| Defensibility / Moat | X | [brief note] |
| Ease of Build (MVP) | X | [brief note] |
| Revenue Potential | X | [brief note] |
| Founder-Market Fit* | X | [brief note] |
| Timing | X | [brief note] |
| **Overall Viability** | **X/10** | [one-sentence verdict] |

*Founder-Market Fit is rated based on what can be inferred. Note if more info is needed.

---

*This report was generated as a starting point for evaluation. All estimates should be validated with real customer conversations, deeper financial modeling, and professional legal/financial advice before committing significant resources.*
```

---

## Writing Guidelines

When writing the report, follow these principles:

- **Be honest, not promotional.** This is a decision-making tool, not a pitch deck. If the idea has serious problems, say so clearly. The user's time and money are at stake.
- **Use real data.** Search the web for actual competitor names, market size figures, pricing data, and trends. Don't make up numbers — if data isn't available, say so and provide your best estimate with reasoning.
- **Be specific to the niche.** Generic advice is useless. Every section should be tailored to the specific idea, market, and user base described. If the startup is for veterinary clinics, don't give advice that applies to "small businesses" generically.
- **Quantify when possible.** Use numbers, ranges, timelines, and dollar amounts. "The market is large" is unhelpful. "The US veterinary software market is estimated at $X-Y billion" is useful.
- **Call out assumptions.** Whenever you make an assumption, mark it explicitly so the user knows what to validate.
- **Write for a founder, not an MBA class.** Use plain language. Skip jargon unless it's industry-standard. Be direct and actionable.

## Output

Save the completed report as a markdown file:
- Filename: `<idea-slug>-startup-research.md` (e.g., `ai-nurse-scheduling-startup-research.md`)
- Location: `/mnt/user-data/outputs/`
- Present the file to the user using `present_files`

## Example

**Input:** "An app that helps independent coffee shops optimize their menu pricing based on local competitor prices and ingredient costs"

**Output:** A ~3,000-5,000 word markdown report covering all 12 sections above, with real competitor data (Toast, Square for Restaurants, MarketMan, etc.), market sizing for independent US coffee shops (~38,000 establishments), specific pricing strategy recommendations, a 6-8 week MVP timeline for an agentic engineer, and tailored go-to-market advice focused on coffee shop owner communities and local business associations.