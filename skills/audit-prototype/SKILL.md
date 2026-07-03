---
name: audit-prototype
description: Build a mocked interactive prototype UI from smart contracts to help security researchers understand a protocol. Analyzes contracts, extracts interfaces/admin functions/state, and builds a lightweight frontend with SQLite persistence, real-time price feeds, simulated trading, admin levers, and annotated visualizations. Uses agent teams for parallel builds. Does NOT connect to any blockchain, wallet, or local node. Use when users request "audit prototype", "prototype the contracts", "build a mock UI", "mock frontend", "contract explorer", "protocol prototype", or want to visually explore a smart contract system.
argument-hint: [contracts-path-or-glob] [output-dir]
---

# Audit Prototype Builder

You are a senior blockchain security researcher. Your task is to analyze smart contracts in a project and build a fully mocked, interactive prototype frontend that helps auditors understand the protocol — its mechanics, admin controls, token flows, and economic dynamics.

**This prototype does NOT connect to any blockchain, local node, wallet (MetaMask), or RPC endpoint.** All contract interactions are mocked. Persistence uses SQLite. Real-time market data (prices) is sourced from public APIs. Everything else (traders, swaps, liquidations) is simulated.

## Arguments

- **Contracts path**: `$ARGUMENTS[0]` — Path or glob to the smart contract files (e.g., `src/*.sol`, `contracts/`)
- **Output directory**: `$ARGUMENTS[1]` — Where to generate the prototype (default: `./audit-prototype`)

## Purpose

Security researchers use this prototype to:
- Visually understand how the protocol works before reading code line-by-line
- Toggle admin levers (fees, rates, thresholds, pausing) and see the effects immediately
- Observe simulated market activity (trades, swaps, liquidations, deposits/withdrawals)
- Explore state transitions, access control, and privileged roles
- Annotate and take notes on protocol mechanics during an audit
- Identify attack surfaces by manipulating parameters in a safe mock environment

---

## Phase 1: Contract Analysis

Read and deeply analyze all in-scope smart contracts. Extract the following:

### 1.1 Contract Inventory

For each contract, identify:
- **Name and purpose** (what it does in the protocol)
- **Inheritance hierarchy** (parent contracts, interfaces, libraries)
- **Deployment dependencies** (what contracts it references or calls)

### 1.2 State Variables

Extract all storage variables:
- Name, type, visibility, initial value (if set)
- Which variables are configurable (set via setter functions)
- Which variables affect protocol economics (fees, rates, thresholds, caps)
- Mappings and their key/value types (these become queryable tables in the UI)

### 1.3 Admin / Privileged Functions

This is critical for the prototype. Extract every function gated by access control:
- `onlyOwner`, `onlyAdmin`, `onlyRole(...)`, `onlyGovernance`, custom modifiers
- Timelock-protected functions
- Pausable controls (`pause()`, `unpause()`)
- Parameter setters (`setFee()`, `setRate()`, `setThreshold()`, `updateOracle()`)
- Emergency functions (`emergencyWithdraw()`, `killSwitch()`)

For each, record:
- Function signature and parameters
- What state it modifies
- Current access control (who can call it)
- Impact on the protocol (what changes when this is called)

### 1.4 User-Facing Functions

Extract all public/external functions callable by regular users:
- Deposit, withdraw, swap, stake, unstake, borrow, repay, claim, etc.
- Their parameters, return values, and events emitted
- Any preconditions or validation checks

### 1.5 Events

Extract all events — these drive the activity feed and visualizations:
- Event name, parameters (indexed and non-indexed)
- Which functions emit them
- What they represent in the protocol lifecycle

### 1.6 Economic Model

Identify the protocol's economic mechanics:
- Fee structures (flat fees, percentage fees, tiered fees)
- Interest rate models (linear, compound, utilization-based)
- Reward/emission schedules
- Liquidation mechanics and thresholds
- Bonding curves, AMM formulas, or pricing functions
- Token minting/burning mechanics

### 1.7 Oracle / External Data Dependencies

Identify what external data the protocol consumes:
- Price feeds (Chainlink, Pyth, TWAP, custom oracles)
- Which tokens need price data
- How prices flow through the system (which calculations use them)

---

## Phase 2: Prototype Architecture Design

Based on the contract analysis, design the prototype architecture.

### 2.1 Technology Stack

Use the lightest-weight, most portable stack possible:

**Frontend**: React + Vite + TailwindCSS + shadcn/ui
- Fast to build, easy to run (`npm run dev`)
- shadcn/ui for polished components without heavy dependencies
- Recharts or lightweight charting for visualizations

**Backend**: Node.js + Express (or Fastify) + SQLite (via better-sqlite3)
- Single-file database, zero config
- REST API mimicking contract calls
- SSE (Server-Sent Events) for real-time simulation streams

**Simulation Engine**: Node.js background process
- Generates simulated market activity (trades, swaps, liquidations)
- Feeds real-time price data from public APIs (CoinGecko, etc.)
- Runs configurable scenarios

### 2.2 Database Schema Design

Design SQLite tables that mirror the contract state:

- **protocol_state**: Key-value store for all configurable parameters (fees, rates, thresholds)
- **accounts**: Simulated user accounts with balances per token
- **positions**: Open positions (borrows, stakes, LP positions, etc.)
- **transactions**: History of all simulated actions with timestamps
- **events_log**: Mirror of contract events for the activity feed
- **price_feeds**: Cached price data with timestamps
- **admin_actions**: Audit trail of all admin lever changes

### 2.3 Mock Contract Layer

Create a service layer that mimics smart contract behavior:
- Each contract becomes a service class/module
- Functions validate inputs, update SQLite state, and emit events
- Access control is enforced (admin vs. user functions)
- Economic calculations use the same formulas from the contracts
- State changes are atomic (SQLite transactions)

### 2.4 Real-Time Data Strategy

**Real data sources** (use public APIs, no API keys required where possible):
- Token prices: CoinGecko public API (`/api/v3/simple/price`)
- Gas prices: Public Ethereum gas trackers
- Market data: Any freely available crypto market endpoints

**Simulated data** (generated by the simulation engine):
- Trader activity: Random trades within realistic bounds
- Liquidity events: Deposits, withdrawals following patterns
- Liquidation events: Triggered when simulated prices cross thresholds
- Time progression: Accelerated time for interest accrual, vesting, etc.

### 2.5 UI Layout Design

Design the prototype UI with these sections:

**Header / Navigation**:
- Protocol name and description (extracted from contracts/README)
- Role switcher: Admin | User | Observer
- Simulation controls: Play/Pause, Speed (1x, 5x, 10x, 50x), Reset

**Dashboard (Main View)**:
- Protocol overview: TVL, total users, total transactions
- Live price feeds with mini-charts
- Recent activity feed (events stream)
- Key protocol metrics (utilization rate, health factor, etc.)

**Admin Panel** (visible when Admin role selected):
- Grouped by contract: all admin functions as interactive forms
- Each lever shows: current value, input to change, description of impact
- Toggle switches for boolean settings (paused, enabled, etc.)
- Sliders for numeric parameters (fees 0-100%, rates, thresholds)
- History of admin actions with timestamps
- Visual indicators showing what part of the protocol each setting affects

**User Interaction Panel**:
- Forms for each user-facing function (deposit, swap, borrow, etc.)
- Simulated wallet with token balances
- Position viewer (open positions, their health, PnL)
- Transaction history for the selected account

**Visualizations Panel**:
- Protocol flow diagram (how tokens/value move through contracts)
- Fee flow visualization (where fees are collected and distributed)
- State machine diagram (protocol states and transitions)
- Real-time charts: prices, TVL over time, utilization, rates
- Animated token flow when actions are performed

**Contract Explorer Panel**:
- Annotated contract list with descriptions
- Function reference with parameters and access control
- State variable browser with current values
- Event log with filtering and search

**Annotations & Notes**:
- Ability to add sticky notes/annotations to any section
- Highlight suspicious or interesting patterns
- Export notes as markdown for audit reports

---

## Phase 3: Agent Team Build

Use agent teams to build the prototype in parallel. This is the core execution phase.

### 3.1 Determine Team Structure

Based on the contract analysis, spawn this team:

**Agent 1 — Database & Mock Contract Layer** (backend-core):
- Owns: `<output-dir>/server/db/`, `<output-dir>/server/services/`, `<output-dir>/server/models/`
- Builds: SQLite schema, mock contract services, state management
- Does NOT touch: frontend/, simulation/

**Agent 2 — API & Simulation Engine** (backend-api):
- Owns: `<output-dir>/server/routes/`, `<output-dir>/server/simulation/`, `<output-dir>/server/index.js`
- Builds: REST API endpoints, SSE streams, simulation engine, real-time data fetching
- Does NOT touch: frontend/, db/, services/

**Agent 3 — Frontend UI & Visualizations** (frontend):
- Owns: `<output-dir>/frontend/`
- Builds: React components, admin panel, visualizations, annotations
- Does NOT touch: server/

### 3.2 Define Contracts Before Spawning

**Database → API contract:**
- Service function signatures (e.g., `getProtocolState(): Record<string, any>`)
- Data model shapes (TypeScript interfaces for all entities)
- Return types for queries (paginated lists, single items)

**API → Frontend contract:**
- Exact REST endpoint URLs, methods, request/response JSON shapes
- SSE event stream URL and event types with JSON payloads
- Admin endpoints vs user endpoints (authentication mock via role header)
- Error response shapes and status codes

**Simulation → API contract:**
- How simulation events are stored (via service layer)
- How simulation state is queried (via API endpoints)
- SSE event types for real-time simulation updates

### 3.3 Cross-Cutting Concerns

Assign explicitly before spawning:

| Concern | Owner | Details |
|---------|-------|---------|
| URL conventions | backend-api | All endpoints: `/api/v1/<resource>`, no trailing slash |
| Error shapes | backend-api | `{ error: string, code: string, details?: any }` |
| Role-based access | backend-core | Mock auth via `X-Role` header: `admin`, `user`, `observer` |
| Real-time updates | backend-api | SSE at `/api/v1/events/stream`, event types prefixed with entity |
| Price data caching | backend-api | Cache prices for 30s, refresh in background |
| Responsive layout | frontend | Mobile-friendly but desktop-primary |
| Annotation storage | backend-core | Store in SQLite `annotations` table, CRUD via API |

### 3.4 Spawn All Agents in Parallel

Enter **Delegate Mode** (Shift+Tab) before spawning agents. You are the coordinator — do NOT implement code yourself.

Use the spawn prompt structure from `build-with-team`:
- Include ownership boundaries
- Include the full contracts (API shapes, data models)
- Include cross-cutting concern assignments
- Include validation checklists

### 3.5 Agent Validation Checklists

**Agent 1 (backend-core) validates:**
1. SQLite database creates without errors
2. All mock contract services can be instantiated
3. CRUD operations work for all entities
4. Admin functions enforce role checks
5. Economic calculations match contract formulas

**Agent 2 (backend-api) validates:**
1. Server starts without errors on a configurable port
2. All API endpoints respond with correct shapes
3. SSE stream connects and sends events
4. Simulation engine starts and generates activity
5. Real-time price fetching works (with graceful fallback)

**Agent 3 (frontend) validates:**
1. `npm run build` succeeds with no errors
2. Dev server starts
3. All pages render without console errors
4. Admin panel shows all extracted admin functions
5. Visualizations render with mock data
6. Role switching works (Admin/User/Observer)

---

## Phase 4: Protocol-Specific Customizations

After the base prototype is built, customize it based on the protocol type detected during contract analysis.

### DEX / AMM Protocol
- Swap simulator with slippage visualization
- Liquidity pool depth chart
- Impermanent loss calculator
- Real-time price feeds for trading pairs
- Order book visualization (if applicable)
- Animated token flow on swap execution

### Lending / Borrowing Protocol
- Health factor gauge with liquidation threshold markers
- Interest rate curve visualization (utilization vs rate)
- Collateral ratio dashboard
- Liquidation simulator (drag price to see when liquidation triggers)
- Supply/borrow APY comparison charts

### Staking / Yield Protocol
- APY calculator with compounding visualization
- Reward distribution timeline
- Vesting schedule visualization
- Stake/unstake flow with cooldown periods
- TVL growth over time chart

### Governance Protocol
- Proposal lifecycle visualization
- Voting power distribution
- Timelock countdown timers
- Quorum progress bars
- Proposal impact previews

### Vault / Aggregator Protocol
- Strategy allocation pie chart
- Yield comparison across strategies
- Deposit/withdrawal flow visualization
- Performance over time vs benchmark
- Risk exposure breakdown

### Bridge / Cross-Chain Protocol
- Cross-chain message flow diagram
- Transfer status tracker
- Chain-specific balance views
- Message relay visualization
- Fee comparison across routes

---

## Phase 5: Final Assembly & Polish

### 5.1 Startup Script

Create a single startup script at `<output-dir>/start.sh`:

```bash
#!/bin/bash
# Audit Prototype - <Protocol Name>
# Start both backend and frontend

echo "Starting Audit Prototype..."

# Install dependencies if needed
(cd server && npm install --silent) &
(cd frontend && npm install --silent) &
wait

# Start backend (includes simulation engine)
(cd server && node index.js) &
BACKEND_PID=$!

# Wait for backend to be ready
sleep 2

# Start frontend
(cd frontend && npm run dev) &
FRONTEND_PID=$!

echo ""
echo "Audit Prototype is running!"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
```

### 5.2 README

Generate `<output-dir>/README.md` with:
- Protocol summary (from contract analysis)
- Quick start instructions (`./start.sh`)
- Architecture overview
- List of admin levers and what they control
- List of simulated behaviors
- Screenshots/descriptions of each UI section
- Notes on what is real data vs simulated

### 5.3 Seed Data

Pre-populate the database with realistic initial state:
- Protocol parameters set to values from contract defaults or constructor args
- A set of simulated accounts with varied balances
- Some initial positions/transactions so the UI isn't empty on first load
- Historical price data for charts (fetched or generated)

### 5.4 Annotation Templates

Pre-populate annotation templates for common audit concerns:
- "Check: access control on this function"
- "Check: reentrancy risk"
- "Check: oracle manipulation"
- "Check: fee calculation accuracy"
- "Note: privileged role can..."
- "Question: what happens when..."

---

## Phase 6: Lead Validation (End-to-End)

After all agents return control, run end-to-end validation yourself:

1. **Can the system start?**
   - Run `./start.sh` or start backend and frontend separately
   - No startup errors in either process

2. **Does the dashboard load?**
   - Navigate to `http://localhost:5173`
   - Dashboard shows protocol overview with data
   - Activity feed is streaming events

3. **Do admin levers work?**
   - Switch to Admin role
   - Change a fee parameter → verify it updates in the database and reflects in the UI
   - Pause/unpause → verify it affects simulated activity

4. **Does simulation work?**
   - Simulated trades/events are appearing in the activity feed
   - Price feeds are updating (real or simulated fallback)
   - Charts are rendering with data points

5. **Do user interactions work?**
   - Switch to User role
   - Execute a simulated action (deposit, swap, etc.)
   - Verify it appears in transaction history and events

6. **Do visualizations render?**
   - Protocol flow diagram is visible
   - Charts have data and are interactive
   - Animations trigger on actions

If validation fails, re-spawn the relevant agent with the specific issue.

---

## Output Summary

When complete, present the user with:

```
Audit Prototype Built Successfully!

Protocol: <name>
Location: <output-dir>/
Contracts Analyzed: <count>

Quick Start:
  cd <output-dir> && ./start.sh

Admin Levers Extracted: <count>
  - <list top 5 most impactful admin functions>

User Functions Mocked: <count>
  - <list top 5 user-facing functions>

Visualizations:
  - <list visualizations included>

Simulations:
  - <list what is being simulated>

Real-Time Data:
  - <list real data sources connected>

Notes:
  - This is a MOCK prototype — no blockchain connections
  - All state is in SQLite at server/data/prototype.db
  - Reset state: delete the .db file and restart
  - Annotations are persisted across sessions
```

---

## Edge Cases

- **No Solidity/Vyper/Rust files found**: Stop and ask the user to specify the contract files
- **Contracts don't compile or have syntax errors**: Analyze them as-is using text parsing, note compilation issues
- **Very large protocol (20+ contracts)**: Group contracts by module/subsystem, build prototype for the core modules first, offer to add more
- **No identifiable admin functions**: Note this in the prototype, provide a read-only explorer view
- **No economic model detected**: Build a simpler state explorer without simulation, note the limitation
- **External dependencies (OpenZeppelin, etc.)**: Resolve imports, use the interface definitions for understanding
- **Proxy contracts**: Identify the implementation contract and analyze that
- **Multiple protocol types (e.g., DEX + Lending)**: Apply customizations for all detected types
- **No internet access for price feeds**: Fall back to generated price data with realistic volatility patterns
- **Port conflicts**: Make ports configurable via environment variables

## Execute

Now analyze the contracts at `$ARGUMENTS[0]` and begin:

1. Read and deeply analyze all smart contracts (Phase 1)
2. Design the prototype architecture based on findings (Phase 2)
3. Determine agent team structure, define contracts and cross-cutting concerns (Phase 3.1-3.3)
4. Enter Delegate Mode (Shift+Tab)
5. Spawn all agents in parallel with full contracts and validation checklists (Phase 3.4)
6. Monitor agents, relay messages, mediate contract deviations (Phase 3)
7. Apply protocol-specific customizations (Phase 4)
8. Assemble final output: startup script, README, seed data (Phase 5)
9. Run end-to-end validation (Phase 6)
10. Present the output summary to the user
