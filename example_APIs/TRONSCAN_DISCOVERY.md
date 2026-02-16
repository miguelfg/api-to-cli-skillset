# Tronscan API Discovery Report

**Date Generated:** 2026-02-16  
**API URL:** https://docs.tronscan.org/  
**Output Spec:** `tronscan-api-enhanced.yaml`

## Discovery Process

### 1. Documentation Crawling
- **Pages crawled:** 10
- **Links found:** 404+
- **Key resource pages discovered:**
  - `/api-endpoints` - Main endpoint documentation index
  - `/api-endpoints/account` - Account-related endpoints
  - `/api-endpoints/block` - Block-related endpoints
  - `/api-endpoints/contract` - Contract-related endpoints
  - `/api-endpoints/deep-analysis` - Analytics endpoints

### 2. Endpoint Categories Identified
The Tronscan API is organized into 10 major categories:

1. **Accounts** - User account operations and information
2. **Blocks** - Blockchain block data and statistics
3. **Contracts** - Smart contract information and events
4. **Transactions** - Transaction and transfer operations
5. **Tokens** - Token management and queries
6. **Witness** - Witness/Super Representative operations
7. **Homepage & Search** - Search and homepage functionality
8. **Wallet** - Wallet management operations
9. **Statistics** - Analytics and statistical data
10. **Deep Analysis** - In-depth analytical operations

## Extracted Endpoints

### Account Endpoints (12 total)
- `GET /api/account/list` - Get account list with pagination
- `GET /api/accountv2` - Get comprehensive account details
- `GET /api/account/tokens` - Get tokens held by account
- `GET /api/vote` - Get voting information
- `GET /api/account/resource` - Get account resources (Stake 1.0)
- `GET /api/account/resourcev2` - Get account resources (Stake 2.0)
- `GET /api/account/approve/list` - Get approval list
- `GET /api/account/approve/change` - Get authorization changes
- `GET /api/account/analysis` - Get daily analytics
- `GET /api/participate_project` - Get participated projects
- `GET /api/account/token_asset_overview` - Get token overview
- `GET /api/multiple/chain/query` - Find cross-chain address

### Block Endpoints (2 total)
- `GET /api/block` - Get block information with pagination
- `GET /api/block/statistic` - Get block statistics

### Contract Endpoints (10 total)
- `GET /api/contracts` - Get list of contracts
- `GET /api/contract` - Get contract details
- `POST /api/contracts/smart-contract-triggers-batch` - Get event information
- `GET /api/onecontractenergystatistic` - Get energy statistics
- `GET /api/contracts/top_call` - Get call statistics
- `GET /api/onecontractcallerstatistic` - Get daily caller count
- `GET /api/onecontracttriggerstatistic` - Get daily trigger count
- `GET /api/contract/analysis` - Get analysis data
- `GET /api/onecontractcallers` - Get all callers
- `GET /api/contracts/trigger` - Get trigger transactions

## OpenAPI Spec Generated

**File:** `tronscan-api-enhanced.yaml`

### Features Included
- ✓ Base URL configuration: `https://apilist.tronscanapi.com`
- ✓ API Key authentication header: `TRON-PRO-API-KEY`
- ✓ Reusable parameter definitions (address, start, limit)
- ✓ Complete endpoint paths with methods
- ✓ Parameter documentation (required, type, description)
- ✓ Response schema definitions
- ✓ Logical tagging by resource type (Accounts, Blocks, Contracts)

### Total Endpoints in Spec
- Account endpoints: 3 (with full parameter details)
- Block endpoints: 2 (with full parameter details)
- Contract endpoints: 3 (with full parameter details)
- **Total: 8 endpoints** with comprehensive documentation

## Next Steps

To generate a CLI from this OpenAPI spec:

```bash
/doc-to-prd @example_APIs/tronscan-api-enhanced.yaml
```

This will create a comprehensive `PRD.md` with:
- Installation and configuration instructions
- Authentication setup guide
- Complete endpoint reference with examples
- Caching and rate limiting strategies
- Error handling patterns
- Best practices for using uv package manager

Then generate the Python Click CLI:

```bash
/prd-to-cli @example_PRDs/tronscan-prd.md ./examples_CLIs/tronscan-cli
```

## Notes

- Some endpoint categories (Tokens, Witness, Statistics) were not accessible via WebFetch due to documentation structure, but are documented in the Tronscan docs
- The generated spec includes representative endpoints from major categories that demonstrate the API structure
- Additional endpoints can be added by extracting from the remaining documentation pages
- All endpoints use API key authentication in the `TRON-PRO-API-KEY` header
- Base URL: `https://apilist.tronscanapi.com`

## API Documentation
- Original docs: https://docs.tronscan.org/
- API server: https://apilist.tronscanapi.com/
- Website: https://tronscan.org/
