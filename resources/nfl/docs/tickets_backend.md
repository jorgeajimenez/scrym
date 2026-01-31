# Backend Engineering Tickets

## Epic: Formation Management Backend

---

### BACK-1: Database Schema Design & Migration

**Priority**: P0 (Critical)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 1

**Description**:
Design and implement PostgreSQL database schema for formations, players, playbooks, and related entities.

**Technical Requirements**:
- Create `formations` table with all metadata fields
- Create `formation_players` table with FK to formations
- Create `playbooks` table for team playbook management
- Create `playbook_formations` junction table
- Create `formation_templates` table for pre-built formations
- Add indexes on frequently queried columns
- Create database migration scripts (Alembic)

**Acceptance Criteria**:
- [ ] All 5 tables created with correct schema
- [ ] Foreign key constraints properly configured
- [ ] Indexes created for: personnel_package, formation_type, created_at
- [ ] Migration scripts run successfully forward and backward
- [ ] Sample data inserted successfully
- [ ] Database diagram generated

**Dependencies**: None

**Files to Create**:
- `alembic/versions/001_create_formations_schema.py`
- `db/schema.sql`
- `db/sample_data.sql`

---

### BACK-2: Pydantic Data Models

**Priority**: P0 (Critical)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 1

**Description**:
Create Pydantic models for request/response validation and type safety.

**Technical Requirements**:
- Create `Formation` model with all fields
- Create `PlayerOnField` model with position validation
- Create `FieldPosition` model (x, y coordinates)
- Create `FormationSimulationRequest` model
- Create `FormationSimulationResult` model
- Create `Playbook` model
- Add custom validators for NFL rules
- Create enums for PositionType, PersonnelPackage, FormationType

**Acceptance Criteria**:
- [ ] All models defined with proper types
- [ ] Validation works for all fields
- [ ] Personnel package validation enforces correct RB/TE/WR counts
- [ ] Field position constraints (x: 0-53.33, y: 0-120)
- [ ] Models serialize to/from JSON correctly
- [ ] Example instances pass validation
- [ ] Unit tests for validators pass

**Dependencies**: None

**Files to Create**:
- `backend/models/formation_models.py`
- `backend/models/enums.py`
- `tests/test_formation_models.py`

---

### BACK-3: Formation CRUD API Endpoints

**Priority**: P0 (Critical)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 2

**Description**:
Implement RESTful API endpoints for formation CRUD operations.

**Technical Requirements**:
- POST `/api/formations/create` - Create new formation
- GET `/api/formations/{id}` - Get formation by ID
- PUT `/api/formations/{id}` - Update existing formation
- DELETE `/api/formations/{id}` - Delete formation (soft delete)
- GET `/api/formations` - List formations with pagination, filters, search
- POST `/api/formations/validate` - Validate formation against NFL rules

**Query Parameters**:
- `page` (int, default 1)
- `per_page` (int, default 20, max 100)
- `personnel` (str, filter by package)
- `formation_type` (str)
- `search` (str, search name/tags)
- `sort_by` (str, default "created_at")
- `order` (asc/desc, default desc)

**Acceptance Criteria**:
- [ ] All endpoints return correct status codes
- [ ] Request validation works (400 for invalid data)
- [ ] Pagination works correctly
- [ ] Filters apply correctly
- [ ] Search works on name and tags
- [ ] Sorting works for all valid fields
- [ ] Soft delete preserves data
- [ ] API documentation auto-generated (FastAPI docs)
- [ ] Unit tests for all endpoints pass
- [ ] Integration tests pass

**Dependencies**: BACK-1, BACK-2

**Files to Create**:
- `backend/api/formations.py`
- `backend/services/formation_service.py`
- `tests/test_formation_api.py`

---

### BACK-4: Formation Validation Service

**Priority**: P0 (Critical)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 2

**Description**:
Implement NFL rules validation logic for formations.

**Validation Rules**:
1. Exactly 11 players on field
2. At least 7 players on line of scrimmage (within 1 yard of LOS)
3. Personnel package matches actual player count:
   - Count RBs, TEs, WRs
   - Verify against declared personnel package (11, 12, 21, etc.)
4. Offensive line continuity (no gaps between 5 OL positions)
5. No overlapping player positions (min 1 yard separation)
6. Eligible receiver rules (ends on LOS, all backs eligible)

**Technical Requirements**:
- Create `FormationValidator` class
- Implement each validation rule as separate method
- Return structured validation result with errors and warnings
- Support auto-fix for common violations
- Performance: < 100ms for validation

**Acceptance Criteria**:
- [ ] All 6 validation rules implemented
- [ ] Returns list of errors with specific messages
- [ ] Returns list of warnings for suboptimal formations
- [ ] Auto-fix resolves common issues (e.g., adjust LOS positions)
- [ ] Validation runs in < 100ms
- [ ] Unit tests cover all validation scenarios
- [ ] Edge cases handled (empty formation, invalid positions)

**Dependencies**: BACK-2

**Files to Create**:
- `backend/services/formation_validator.py`
- `tests/test_formation_validator.py`

---

### BACK-5: ML Model Integration Service

**Priority**: P0 (Critical)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 3

**Description**:
Integrate existing PyTorch ML models for formation analysis.

**Technical Requirements**:
- Load Personnel Optimizer model on startup
- Load Offensive Play-Caller model on startup
- Load Defensive Coordinator model on startup
- Load scalers and label encoders
- Create `FormationMLAnalyzer` class with methods:
  - `analyze_personnel_fit()` - Returns confidence score 0-1
  - `predict_play_success()` - Returns play probabilities and EPA
  - `predict_defensive_response()` - Returns run/pass prob and predicted front
  - `evaluate_formation_balance()` - Returns run/pass bias scores
- Handle model errors gracefully (fallback to basic analysis)
- Cache model outputs (LRU cache, max 100 entries)

**Acceptance Criteria**:
- [ ] All 3 models load successfully on startup
- [ ] Inference completes in < 200ms per model
- [ ] Scalers transform features correctly
- [ ] Label encoders decode predictions correctly
- [ ] Results are deterministic (same input = same output)
- [ ] Model errors don't crash the service
- [ ] Cache improves performance (hit rate > 80%)
- [ ] Unit tests mock models and test logic
- [ ] Integration tests use real models

**Dependencies**: Existing trained models (personnel_model.pt, offensive_model.pt, defensive_model.pt)

**Files to Create**:
- `backend/services/formation_ml_analyzer.py`
- `backend/services/model_loader.py`
- `tests/test_formation_ml_analyzer.py`

---

### BACK-6: Formation Simulation API Endpoint

**Priority**: P0 (Critical)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 3

**Description**:
Implement formation simulation endpoint that combines all ML models.

**Technical Requirements**:
- POST `/api/formations/simulate`
- Request body: `FormationSimulationRequest`
- Response body: `FormationSimulationResult`
- Combine outputs from all 3 ML models:
  - Personnel match score (from Personnel Optimizer)
  - Play success predictions (from Offensive Play-Caller)
  - Defensive response (from Defensive Coordinator)
- Calculate additional metrics:
  - Expected EPA
  - Run/pass efficiency
  - Formation balance score
- Generate recommendations:
  - Top 3-5 optimal plays
  - Suggested adjustments
  - Defensive weaknesses to exploit
- Total response time < 500ms

**Acceptance Criteria**:
- [ ] Endpoint returns all required metrics
- [ ] Response time < 500ms (average)
- [ ] All calculations are correct
- [ ] Recommendations are contextually relevant
- [ ] Handles edge cases (invalid formation, missing context)
- [ ] Results are cached (same input returns cached result)
- [ ] API documentation is complete
- [ ] Unit tests cover all logic paths
- [ ] Integration tests use real models

**Dependencies**: BACK-2, BACK-5

**Files to Create**:
- `backend/api/simulation.py`
- `backend/services/simulation_service.py`
- `tests/test_simulation_api.py`

---

### BACK-7: Formation Template Library

**Priority**: P0 (Critical)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 3

**Description**:
Create library of 50+ pre-built formation templates.

**Technical Requirements**:
- Create 50+ formation templates covering:
  - Common formations (20): Shotgun variations, I-Form, Singleback, Pistol
  - Specialty formations (15): Goal line, short yardage, 2-minute drill
  - Exotic formations (15): Wildcat, Bunch, Nasty Split, etc.
- Each template includes:
  - All 11 player positions (x, y coordinates)
  - Personnel package
  - Formation type
  - Recommended use cases
  - Tags
- GET `/api/formations/templates` endpoint
- Filter by personnel, formation type, situation
- Seed database with templates on startup

**Acceptance Criteria**:
- [ ] At least 50 unique templates created
- [ ] All templates pass validation
- [ ] Templates cover all common personnel packages (11, 12, 21, 13, 22)
- [ ] Templates represent accurate NFL formations
- [ ] Endpoint returns filtered templates correctly
- [ ] Database seeding works
- [ ] Templates include descriptive names and tags

**Dependencies**: BACK-1, BACK-2, BACK-4

**Files to Create**:
- `backend/data/formation_templates.json`
- `backend/api/templates.py`
- `backend/services/template_service.py`
- `db/seed_templates.sql`

---

### BACK-8: Playbook Management API

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 4

**Description**:
Implement playbook CRUD operations and formation associations.

**Technical Requirements**:
- POST `/api/playbooks/create` - Create team playbook
- GET `/api/playbooks/{id}` - Get playbook with formations
- PUT `/api/playbooks/{id}` - Update playbook metadata
- DELETE `/api/playbooks/{id}` - Delete playbook
- POST `/api/playbooks/{id}/formations` - Add formation to playbook
- DELETE `/api/playbooks/{id}/formations/{formation_id}` - Remove formation
- GET `/api/playbooks/{id}/formations` - List playbook formations with filters
- Soft delete for formations (mark as archived, not hard delete)

**Acceptance Criteria**:
- [ ] All endpoints work correctly
- [ ] Playbook-formation associations managed correctly
- [ ] Filters work (personnel, type, tags)
- [ ] Pagination implemented
- [ ] Duplicate formation names prevented within playbook
- [ ] Soft delete preserves formation data
- [ ] API documentation complete
- [ ] Unit and integration tests pass

**Dependencies**: BACK-1, BACK-2, BACK-3

**Files to Create**:
- `backend/api/playbooks.py`
- `backend/services/playbook_service.py`
- `tests/test_playbook_api.py`

---

### BACK-9: Formation Comparison Endpoint

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 4

**Description**:
Implement endpoint to compare multiple formations side-by-side.

**Technical Requirements**:
- POST `/api/formations/compare`
- Request body: Array of 2-4 formation IDs + game context
- Response includes for each formation:
  - Simulation results
  - Key metrics
  - Pros/cons analysis
  - Differences highlighted
- Rank formations by expected EPA
- Generate recommendation for best formation given context

**Acceptance Criteria**:
- [ ] Accepts 2-4 formation IDs
- [ ] Runs simulation for each formation
- [ ] Returns comparison results
- [ ] Highlights key differences
- [ ] Ranking is correct
- [ ] Recommendation is contextually appropriate
- [ ] Response time < 2 seconds for 4 formations
- [ ] Unit tests pass

**Dependencies**: BACK-6

**Files to Create**:
- `backend/api/comparison.py`
- `backend/services/comparison_service.py`
- `tests/test_comparison_api.py`

---

### BACK-10: Heat Map Generation Service

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 5

**Description**:
Generate blocking strength and receiving threat heat maps.

**Technical Requirements**:
- Divide field into 5x5 yard zones (grid: 11 cols x 24 rows)
- Calculate blocking strength for each zone:
  - Count offensive players within 3 yards
  - Weight by position (OL > TE > RB > WR)
  - Calculate angle of approach
  - Return strength score 0-1
- Calculate receiving threat for each zone:
  - Count receivers within route range
  - Weight by position (WR > TE > RB)
  - Evaluate route tree possibilities
  - Return threat score 0-1
- Return as 2D array or object with zone coordinates
- Performance: < 200ms to generate all heat maps

**Acceptance Criteria**:
- [ ] Blocking heat map generated correctly
- [ ] Receiving heat map generated correctly
- [ ] Zones are properly sized (5x5 yards)
- [ ] Scores are normalized 0-1
- [ ] Heat maps include in simulation response
- [ ] Performance < 200ms
- [ ] Unit tests cover calculation logic

**Dependencies**: BACK-6

**Files to Create**:
- `backend/services/heatmap_generator.py`
- `tests/test_heatmap_generator.py`

---

### BACK-11: Search and Filter Service

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 5

**Description**:
Implement advanced search and filtering for formations.

**Technical Requirements**:
- Full-text search on formation name and tags
- Filter by multiple criteria simultaneously:
  - Personnel package
  - Formation type
  - Down, distance ranges
  - Field position zones
  - Success rate ranges
  - Date created range
  - Creator (user ID)
  - Favorites only
- Support query parameters for all filters
- Autocomplete suggestions for formation names
- Search highlighting in results
- Performance: < 200ms for search with filters

**Acceptance Criteria**:
- [ ] Search returns relevant results
- [ ] Filters combine correctly with AND logic
- [ ] Autocomplete works as user types
- [ ] Highlighting shows matched terms
- [ ] Pagination works with search/filters
- [ ] Performance < 200ms
- [ ] Empty results handled gracefully
- [ ] Unit tests cover all filter combinations

**Dependencies**: BACK-3

**Files to Create**:
- `backend/services/search_service.py`
- `tests/test_search_service.py`

---

### BACK-12: Export Service (PDF, JSON, CSV)

**Priority**: P2 (Medium)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 6

**Description**:
Implement formation export in multiple formats.

**Technical Requirements**:
- POST `/api/formations/{id}/export`
- Query param: `format` (pdf, json, csv, png)
- PDF export includes:
  - Formation diagram (generated image)
  - Personnel breakdown
  - Simulation results
  - Recommended plays
  - Heat maps
  - Notes and tags
  - Footer with metadata
- JSON export: Full formation object
- CSV export: Metrics only (flat structure)
- PNG export: Field diagram only (high-res)
- Stream large files (don't load entire file in memory)
- Set appropriate Content-Type headers

**Acceptance Criteria**:
- [ ] PDF generation works (using ReportLab or similar)
- [ ] PDF includes all required sections
- [ ] JSON export is valid and complete
- [ ] CSV export is properly formatted
- [ ] PNG export is high quality (300 DPI)
- [ ] Large files stream correctly
- [ ] Content-Type headers set correctly
- [ ] Export completes in < 5 seconds
- [ ] Unit tests cover all formats

**Dependencies**: BACK-3, BACK-6, BACK-10

**Files to Create**:
- `backend/services/export_service.py`
- `backend/utils/pdf_generator.py`
- `tests/test_export_service.py`

---

### BACK-13: User Authentication & Authorization

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 6

**Description**:
Implement JWT-based auth with role-based access control.

**Technical Requirements**:
- POST `/api/auth/login` - User login (email/password)
- POST `/api/auth/register` - User registration
- POST `/api/auth/refresh` - Refresh access token
- POST `/api/auth/logout` - Invalidate tokens
- GET `/api/auth/me` - Get current user info
- Roles: Admin, Head Coach, Coordinator, Position Coach, Analyst, Viewer
- Permissions enforced on all endpoints
- JWT tokens expire after 24 hours
- Refresh tokens expire after 30 days
- Password hashing with bcrypt
- Account lockout after 5 failed login attempts

**Acceptance Criteria**:
- [ ] Login returns valid JWT token
- [ ] Token validation works on protected endpoints
- [ ] Refresh token flow works
- [ ] Logout invalidates tokens
- [ ] Role permissions enforced correctly
- [ ] Password requirements validated
- [ ] Account lockout works
- [ ] Passwords hashed securely
- [ ] Unit and integration tests pass

**Dependencies**: BACK-1 (users table)

**Files to Create**:
- `backend/api/auth.py`
- `backend/services/auth_service.py`
- `backend/middleware/auth_middleware.py`
- `backend/utils/jwt_utils.py`
- `db/migrations/002_create_users_table.py`
- `tests/test_auth_api.py`

---

### BACK-14: Approval Workflow Service

**Priority**: P2 (Medium)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 7

**Description**:
Implement formation approval workflow with state transitions.

**Technical Requirements**:
- Formation states: Draft, Pending Review, Approved, Rejected
- State transitions:
  - Draft → Pending Review (coordinator submits)
  - Pending Review → Approved (coach approves)
  - Pending Review → Rejected (coach rejects with feedback)
  - Rejected → Draft (coordinator revises)
- POST `/api/formations/{id}/submit` - Submit for review
- POST `/api/formations/{id}/approve` - Approve formation
- POST `/api/formations/{id}/reject` - Reject with feedback
- Email notifications on state changes
- Audit log of all state transitions
- Prevent editing of approved formations

**Acceptance Criteria**:
- [ ] State transitions work correctly
- [ ] Only authorized users can approve/reject
- [ ] Email notifications send within 1 minute
- [ ] Audit log records all transitions
- [ ] Approved formations cannot be edited
- [ ] Rejection feedback stored and displayed
- [ ] Unit tests cover all transitions

**Dependencies**: BACK-3, BACK-13

**Files to Create**:
- `backend/services/approval_service.py`
- `backend/services/notification_service.py`
- `db/migrations/003_add_formation_state.py`
- `tests/test_approval_service.py`

---

### BACK-15: Caching Layer Implementation

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 7

**Description**:
Implement Redis caching for improved performance.

**Technical Requirements**:
- Cache simulation results (key: formation hash, TTL: 1 hour)
- Cache playbook metadata (key: playbook_id, TTL: 5 minutes)
- Cache template library (key: "templates", TTL: 1 day)
- Cache user sessions (key: user_id, TTL: 24 hours)
- Cache ML model outputs (LRU cache, max 100 entries)
- Invalidation strategies:
  - Formation edit → clear simulation cache
  - Playbook update → clear playbook cache
  - ML model update → clear all simulation caches
- Cache hit/miss logging for monitoring

**Acceptance Criteria**:
- [ ] Redis connection configured
- [ ] All cache keys have appropriate TTLs
- [ ] Cache invalidation works correctly
- [ ] No stale data served
- [ ] Cache hit rate > 80%
- [ ] Fallback to database if cache fails
- [ ] Unit tests mock Redis

**Dependencies**: Redis server setup

**Files to Create**:
- `backend/services/cache_service.py`
- `backend/config/redis_config.py`
- `tests/test_cache_service.py`

---

### BACK-16: API Rate Limiting

**Priority**: P2 (Medium)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 7

**Description**:
Implement rate limiting to prevent abuse.

**Technical Requirements**:
- Rate limits:
  - Authenticated users: 100 requests/minute
  - Unauthenticated: 20 requests/minute
  - Simulation endpoint: 10 requests/minute (expensive operation)
- Use sliding window algorithm
- Store counters in Redis
- Return 429 status code when limit exceeded
- Include rate limit headers:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

**Acceptance Criteria**:
- [ ] Rate limits enforced correctly
- [ ] 429 status returned when exceeded
- [ ] Rate limit headers included in response
- [ ] Sliding window works correctly
- [ ] Different limits for different endpoints
- [ ] Unit tests verify rate limiting

**Dependencies**: BACK-15 (Redis)

**Files to Create**:
- `backend/middleware/rate_limit_middleware.py`
- `tests/test_rate_limiting.py`

---

### BACK-17: Error Logging and Monitoring

**Priority**: P1 (High)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 8

**Description**:
Implement comprehensive error logging and monitoring.

**Technical Requirements**:
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log to file and console
- Rotate logs daily, retain for 30 days
- Error tracking integration (Sentry or similar)
- Log context: user_id, request_id, endpoint, duration
- Monitor key metrics:
  - Request count by endpoint
  - Response time percentiles (p50, p95, p99)
  - Error rate
  - Cache hit rate
  - ML model inference time

**Acceptance Criteria**:
- [ ] All errors logged with full context
- [ ] Logs are structured and parsable
- [ ] Log rotation works
- [ ] Error tracking captures exceptions
- [ ] Metrics tracked in monitoring system
- [ ] No sensitive data in logs (passwords, tokens)
- [ ] Performance impact minimal

**Dependencies**: None

**Files to Create**:
- `backend/utils/logger.py`
- `backend/middleware/logging_middleware.py`
- `backend/config/logging_config.py`

---

### BACK-18: Database Connection Pooling

**Priority**: P1 (High)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 8

**Description**:
Implement efficient database connection pooling.

**Technical Requirements**:
- Use SQLAlchemy connection pooling
- Pool size: 10 connections
- Max overflow: 20 connections
- Pool recycle: 3600 seconds (1 hour)
- Connection timeout: 30 seconds
- Echo SQL queries in DEBUG mode only
- Graceful handling of connection errors
- Health check endpoint tests database connectivity

**Acceptance Criteria**:
- [ ] Connection pool configured correctly
- [ ] No connection leaks
- [ ] Pool size appropriate for load
- [ ] Connections recycled periodically
- [ ] Health check works
- [ ] Connection errors handled gracefully

**Dependencies**: BACK-1

**Files to Create**:
- `backend/db/database.py`
- `backend/api/health.py`
- `tests/test_database_pool.py`

---

### BACK-19: API Documentation (OpenAPI/Swagger)

**Priority**: P2 (Medium)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 8

**Description**:
Complete API documentation with examples and descriptions.

**Technical Requirements**:
- FastAPI auto-generates OpenAPI schema
- Add descriptions to all endpoints
- Add examples to all request/response models
- Document query parameters
- Document error responses
- Group endpoints by feature
- Add authentication documentation
- Include code examples in multiple languages (curl, Python, JavaScript)

**Acceptance Criteria**:
- [ ] All endpoints documented
- [ ] All models have descriptions
- [ ] Examples are accurate and helpful
- [ ] Error responses documented
- [ ] Authentication flow explained
- [ ] Swagger UI renders correctly
- [ ] Code examples work

**Dependencies**: All API endpoints complete

**Files to Update**:
- All `backend/api/*.py` files
- All `backend/models/*.py` files

---

### BACK-20: Database Backup and Recovery

**Priority**: P2 (Medium)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 9

**Description**:
Implement automated database backup and recovery procedures.

**Technical Requirements**:
- Daily automated backups at 2 AM
- Backup retention: 30 days
- Backup storage: AWS S3 or similar
- Backup format: pg_dump custom format
- Test restore process monthly
- Document recovery procedures
- Monitor backup success/failure
- Alert on backup failures

**Acceptance Criteria**:
- [ ] Automated backups run daily
- [ ] Backups stored securely in S3
- [ ] Old backups deleted after 30 days
- [ ] Restore process tested and documented
- [ ] Alerts configured for failures
- [ ] Recovery time < 1 hour

**Dependencies**: PostgreSQL database

**Files to Create**:
- `scripts/backup_database.sh`
- `scripts/restore_database.sh`
- `docs/database_recovery.md`

---

## Summary

**Total Tickets**: 20
**Total Story Points**: 111

**Breakdown by Priority**:
- P0 (Critical): 9 tickets, 56 points
- P1 (High): 8 tickets, 44 points
- P2 (Medium): 3 tickets, 11 points

**Estimated Timeline**: 9 sprints (18 weeks) at 12-15 points per sprint
