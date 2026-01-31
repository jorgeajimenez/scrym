# Frontend Engineering Tickets

## Epic: Formation Management Frontend

---

### FRONT-1: Project Setup and Configuration

**Priority**: P0 (Critical)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 1

**Description**:
Set up Next.js 14 project with TypeScript, ESLint, and required dependencies.

**Technical Requirements**:
- Initialize Next.js 14 with TypeScript
- Configure ESLint and Prettier
- Set up folder structure:
  - `/app` - Next.js app router
  - `/components` - Reusable components
  - `/lib` - Utilities and helpers
  - `/hooks` - Custom React hooks
  - `/types` - TypeScript type definitions
  - `/services` - API client services
- Install dependencies:
  - React 18+
  - React DnD for drag-and-drop
  - Tailwind CSS for styling
  - Recharts for data visualization
  - Axios for API calls
  - React Hook Form for forms
  - Zod for validation

**Acceptance Criteria**:
- [ ] Project builds successfully
- [ ] ESLint shows no errors
- [ ] All dependencies installed
- [ ] Development server runs
- [ ] Folder structure follows conventions
- [ ] TypeScript strict mode enabled

**Dependencies**: None

**Files to Create**:
- `package.json`
- `tsconfig.json`
- `.eslintrc.json`
- `next.config.js`
- `tailwind.config.js`

---

### FRONT-2: API Client Service

**Priority**: P0 (Critical)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 1

**Description**:
Create API client service for backend communication.

**Technical Requirements**:
- Create Axios instance with base URL configuration
- Implement request/response interceptors
- Add JWT token to all authenticated requests
- Handle common HTTP errors (401, 403, 429, 500)
- Implement retry logic for failed requests
- Create typed API methods for all endpoints:
  - Formations: create, get, update, delete, list
  - Simulation: simulate, compare
  - Templates: list, get
  - Playbooks: CRUD operations
  - Auth: login, register, logout, refresh

**Acceptance Criteria**:
- [ ] API client configured with correct base URL
- [ ] Auth token automatically attached to requests
- [ ] Error handling works for all error codes
- [ ] Retry logic works for network failures
- [ ] All API methods are typed
- [ ] Unit tests mock API responses

**Dependencies**: Backend API endpoints

**Files to Create**:
- `lib/api/client.ts`
- `lib/api/formations.ts`
- `lib/api/simulation.ts`
- `lib/api/playbooks.ts`
- `lib/api/auth.ts`
- `types/api.ts`

---

### FRONT-3: TypeScript Type Definitions

**Priority**: P0 (Critical)
**Story Points**: 3
**Assignee**: TBD
**Sprint**: Sprint 1

**Description**:
Define TypeScript types matching backend Pydantic models.

**Technical Requirements**:
- Create types for all data models:
  - `Formation`
  - `PlayerOnField`
  - `FieldPosition`
  - `FormationSimulationRequest`
  - `FormationSimulationResult`
  - `Playbook`
  - `User`
- Create enums matching backend:
  - `PositionType`
  - `PersonnelPackage`
  - `FormationType`
  - `DefensiveFront`
- Export all types from central index

**Acceptance Criteria**:
- [ ] All types match backend models exactly
- [ ] Enums are properly defined
- [ ] Types are exported correctly
- [ ] No TypeScript compilation errors
- [ ] Types are used throughout application

**Dependencies**: Backend Pydantic models

**Files to Create**:
- `types/formation.ts`
- `types/simulation.ts`
- `types/playbook.ts`
- `types/user.ts`
- `types/index.ts`

---

### FRONT-4: Football Field Canvas Component

**Priority**: P0 (Critical)
**Story Points**: 13
**Assignee**: TBD
**Sprint**: Sprint 2-3

**Description**:
Build interactive football field canvas with accurate NFL dimensions.

**Technical Requirements**:
- Canvas size: 53.33 yards wide, 40 yards visible length
- Scale: 10 pixels per yard (533px x 400px base, responsive)
- Render field elements:
  - Grass/turf texture background
  - Yard lines every 5 yards (bold) and 1 yard (thin)
  - Yard numbers (10, 20, 30, 40, 50)
  - Hash marks (left at 18.5 yards, right at 18.5 yards)
  - Line of scrimmage (bold yellow/gold line)
  - First down marker (adjustable)
  - End zones
- Zoom controls: 50% - 200%
- Pan: Click and drag background
- Reset view button
- Performance: 60fps during interactions
- Responsive: Scale to container while maintaining aspect ratio

**Acceptance Criteria**:
- [ ] Field renders accurately to NFL specs
- [ ] All yard lines and markers visible
- [ ] Zoom works smoothly (50-200%)
- [ ] Pan works by dragging background
- [ ] Reset view centers field
- [ ] Maintains 60fps during zoom/pan
- [ ] Responsive on all screen sizes
- [ ] Passes visual regression tests

**Dependencies**: None

**Files to Create**:
- `components/FormationCanvas/FootballField.tsx`
- `components/FormationCanvas/FieldRenderer.tsx`
- `hooks/useFieldZoom.ts`
- `lib/fieldUtils.ts`

---

### FRONT-5: Player Component with Drag & Drop

**Priority**: P0 (Critical)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 3

**Description**:
Create draggable player component with position-based styling.

**Technical Requirements**:
- Player icon: 30x30px circular marker
- Color by position:
  - QB: Red (#FF0000)
  - RB/FB: Green (#00FF00)
  - WR: Blue (#0000FF)
  - TE: Purple (#FF00FF)
  - OL: Orange (#FFA500)
- Display mode options:
  - Position abbreviation (default)
  - Jersey number
  - Player name
- Hover tooltip: Name, Position, Jersey #, Depth from LOS
- Click to select/deselect
- Multi-select with Shift+Click
- Drag and drop using React DnD:
  - Click and hold to start drag
  - Show ghost outline at original position
  - Player follows cursor smoothly
  - Snap to grid (optional, 1-yard increments)
  - Constrain to field boundaries
  - Validate on drop (no overlaps, within field)
- Visual states:
  - Default
  - Hover
  - Selected
  - Dragging
  - Invalid position (red outline)

**Acceptance Criteria**:
- [ ] Player renders with correct color
- [ ] Tooltip shows on hover within 100ms
- [ ] Drag starts on click and hold
- [ ] Drag is smooth with no lag
- [ ] Drop validates position
- [ ] Snap to grid works when enabled
- [ ] Selection state is visually clear
- [ ] Multi-select works correctly
- [ ] Unit tests cover drag/drop logic

**Dependencies**: FRONT-4, React DnD

**Files to Create**:
- `components/FormationCanvas/Player.tsx`
- `components/FormationCanvas/PlayerTooltip.tsx`
- `hooks/useDragPlayer.ts`
- `lib/playerUtils.ts`

---

### FRONT-6: Formation Editor Toolbar

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 3

**Description**:
Build toolbar with formation editing controls.

**Technical Requirements**:
- Mode toggle: Edit / View / Simulation
- Edit tools:
  - Add Player (click to place)
  - Delete Player (select and delete key)
  - Duplicate Player
  - Align Tool (align selected players horizontally/vertically/to LOS)
  - Distribute Tool (evenly space selected players)
  - Flip Formation (mirror horizontally)
  - Rotate Players (shift positions)
- Undo/Redo buttons (Ctrl+Z, Ctrl+Y)
- Save button
- Simulate button
- Clear All button (with confirmation)
- Keyboard shortcuts displayed in tooltips
- Disabled state for unavailable actions

**Acceptance Criteria**:
- [ ] All tools work correctly
- [ ] Mode switching is instant
- [ ] Undo/redo maintains history (50 actions)
- [ ] Keyboard shortcuts work
- [ ] Tooltips show shortcuts
- [ ] Disabled states are clear
- [ ] Confirmation dialogs for destructive actions
- [ ] Unit tests cover all tool actions

**Dependencies**: FRONT-4, FRONT-5

**Files to Create**:
- `components/FormationEditor/Toolbar.tsx`
- `components/FormationEditor/ToolButton.tsx`
- `hooks/useFormationHistory.ts`
- `lib/formationTools.ts`

---

### FRONT-7: Formation Properties Panel

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 4

**Description**:
Build properties panel for formation metadata editing.

**Technical Requirements**:
- Form fields:
  - Formation Name (text input, required)
  - Personnel Package (dropdown: 11, 12, 21, etc.)
  - Formation Type (dropdown: Shotgun, I-Form, etc. + custom)
  - Down (number input, 1-4)
  - Distance (number input, 1-99)
  - Yard Line (number input, 1-99)
  - Hash Mark (radio: Left, Middle, Right)
  - Tags (multi-input with autocomplete)
  - Notes (textarea, max 500 chars)
- Real-time validation
- Character counter for text fields
- Auto-save draft to localStorage every 30 seconds
- Unsaved changes warning on navigation

**Acceptance Criteria**:
- [ ] All fields render correctly
- [ ] Validation works in real-time
- [ ] Required fields show error states
- [ ] Auto-save works every 30 seconds
- [ ] Unsaved changes warning appears
- [ ] Dropdown options populated from API
- [ ] Tags autocomplete from existing tags
- [ ] Unit tests cover validation logic

**Dependencies**: React Hook Form, Zod

**Files to Create**:
- `components/FormationEditor/PropertiesPanel.tsx`
- `components/FormationEditor/FormField.tsx`
- `hooks/useFormationForm.ts`
- `lib/validation.ts`

---

### FRONT-8: Formation Validation Display

**Priority**: P0 (Critical)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 4

**Description**:
Display real-time formation validation errors and warnings.

**Technical Requirements**:
- Validation indicator badge:
  - Green checkmark: All valid
  - Yellow warning: Has warnings
  - Red X: Has errors
- Validation panel (collapsible):
  - List of errors (must fix)
  - List of warnings (suboptimal but legal)
  - Each item shows:
    - Error/warning message
    - Affected players (highlighted on field)
    - Auto-fix button (if available)
- Highlight problematic players on field (red outline)
- Click error to center field on affected players
- Auto-fix button resolves common issues
- Validation runs on every formation change (debounced 200ms)

**Acceptance Criteria**:
- [ ] Validation indicator updates in real-time
- [ ] Errors and warnings display correctly
- [ ] Players highlighted on field match errors
- [ ] Click error centers field on players
- [ ] Auto-fix resolves at least 80% of common errors
- [ ] Validation debounce prevents excessive API calls
- [ ] Unit tests cover validation display logic

**Dependencies**: FRONT-4, FRONT-5, Backend validation API

**Files to Create**:
- `components/FormationEditor/ValidationPanel.tsx`
- `components/FormationEditor/ValidationBadge.tsx`
- `hooks/useFormationValidation.ts`

---

### FRONT-9: Formation Template Library

**Priority**: P0 (Critical)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 4

**Description**:
Build template library browser and loader.

**Technical Requirements**:
- Modal/sidebar template browser
- Filter templates by:
  - Personnel Package
  - Formation Type
  - Game Situation
- Search by name
- Grid view of template cards:
  - Template name
  - Personnel badge
  - Formation type
  - Thumbnail preview
  - "Load" button
- Load options:
  - Replace current (with warning if unsaved)
  - Merge with current
  - Load as reference overlay
- Template preview modal (before loading)
- Favorites: Star templates for quick access

**Acceptance Criteria**:
- [ ] Template library loads all templates
- [ ] Filters work correctly
- [ ] Search returns relevant results
- [ ] Template cards display correctly
- [ ] Load options work as expected
- [ ] Unsaved changes warning appears
- [ ] Preview modal shows accurate representation
- [ ] Favorites persist in localStorage
- [ ] Unit tests cover template loading

**Dependencies**: Backend template API

**Files to Create**:
- `components/TemplateLibrary/TemplateBrowser.tsx`
- `components/TemplateLibrary/TemplateCard.tsx`
- `components/TemplateLibrary/TemplatePreview.tsx`
- `hooks/useTemplates.ts`

---

### FRONT-10: Simulation Results Dashboard

**Priority**: P0 (Critical)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 5

**Description**:
Display formation simulation results in comprehensive dashboard.

**Technical Requirements**:
- Results panel layout:
  - Header: Formation name, personnel, situation
  - Overall grade: Letter grade (A-F) with color
  - Key metrics (large cards):
    - Personnel Match Score (gauge chart)
    - Expected EPA (+/- indicator, color-coded)
    - Success Probability (progress bar)
  - Efficiency breakdown:
    - Run Efficiency (horizontal bar, percentage)
    - Pass Efficiency (horizontal bar, percentage)
    - Balance Score (calculated indicator)
  - Recommended plays (expandable list):
    - Play name, type, success %, reason
  - Defensive analysis (expandable):
    - Predicted defensive front
    - Formation weaknesses
    - Exploitation strategies
  - Suggested adjustments (numbered list):
    - Specific changes with expected impact
- Tabbed heat map viewer:
  - Blocking Strength
  - Receiving Threat
  - Defensive Pressure
- Export results button (PDF/PNG)
- Compare with other formations button

**Acceptance Criteria**:
- [ ] All metrics display correctly
- [ ] Gauge charts render properly
- [ ] Color coding is consistent
- [ ] Expandable sections work
- [ ] Heat maps overlay on field
- [ ] Export works for all formats
- [ ] Loading state shows during simulation
- [ ] Error handling for failed simulations
- [ ] Unit tests cover data display logic

**Dependencies**: Backend simulation API, Recharts

**Files to Create**:
- `components/Simulation/ResultsDashboard.tsx`
- `components/Simulation/MetricCard.tsx`
- `components/Simulation/PlayRecommendations.tsx`
- `components/Simulation/HeatMapViewer.tsx`
- `hooks/useSimulation.ts`

---

### FRONT-11: Heat Map Overlay Component

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 5

**Description**:
Render heat maps as overlay on football field.

**Technical Requirements**:
- Render heat map as canvas overlay on field
- Divide field into 5x5 yard zones (grid)
- Color coding:
  - Blocking Strength: Green (strong) → Yellow → Red (weak)
  - Receiving Threat: Blue (high) → Cyan → White (low)
  - Defensive Pressure: Red (high) → Orange → Green (safe)
- Smooth color gradients between zones
- Opacity slider (0-100%)
- Toggle heat map on/off
- Legend showing color scale
- Tooltip on hover showing zone strength value
- Performance: Render in < 200ms

**Acceptance Criteria**:
- [ ] Heat map renders correctly over field
- [ ] Colors match strength values accurately
- [ ] Gradients are smooth
- [ ] Opacity slider works
- [ ] Toggle shows/hides heat map
- [ ] Legend is accurate
- [ ] Tooltip shows correct values
- [ ] Renders in < 200ms
- [ ] Unit tests cover rendering logic

**Dependencies**: FRONT-4, FRONT-10

**Files to Create**:
- `components/FormationCanvas/HeatMapOverlay.tsx`
- `components/Simulation/HeatMapLegend.tsx`
- `lib/heatmapRenderer.ts`

---

### FRONT-12: Dashboard Overview Page

**Priority**: P0 (Critical)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 6

**Description**:
Build main dashboard landing page with statistics and quick actions.

**Technical Requirements**:
- Layout sections:
  - Header: Team name, user info, navigation
  - Stats cards (row):
    - Total formations count
    - Formations by personnel (pie chart)
    - Top formations by EPA (top 5 list)
    - Recent formations (last 10)
  - Quick actions (buttons):
    - Create New Formation
    - Browse Playbook
    - Compare Formations
    - View Analytics
  - Recent activity feed:
    - Formation created/edited
    - Simulation run
    - Formation approved
- Filters:
  - Game situation (down, distance)
  - Field position
  - Date range
- Search bar (formations by name/tags)
- Responsive layout (desktop, tablet, mobile)

**Acceptance Criteria**:
- [ ] Dashboard loads in < 2 seconds
- [ ] All stats display correctly
- [ ] Charts render properly
- [ ] Quick actions work
- [ ] Filters apply correctly
- [ ] Search works
- [ ] Responsive on all screen sizes
- [ ] Real-time updates when formations change
- [ ] Unit tests cover data fetching

**Dependencies**: Backend stats API, Recharts

**Files to Create**:
- `app/dashboard/page.tsx`
- `components/Dashboard/StatsCard.tsx`
- `components/Dashboard/QuickActions.tsx`
- `components/Dashboard/RecentActivity.tsx`
- `hooks/useDashboardStats.ts`

---

### FRONT-13: Playbook Browser Page

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 6

**Description**:
Build playbook browser with grid/list view of formations.

**Technical Requirements**:
- View toggle: Grid (default) / List
- Formation cards (grid view):
  - Formation name
  - Personnel badge (11, 12, etc.)
  - Formation type
  - Thumbnail preview
  - Success rate (if available)
  - Last used date
  - Tags
  - Actions: Edit, Duplicate, Delete
- List view: Compact rows with key info
- Filters panel:
  - Personnel Package
  - Formation Type
  - Down/Distance
  - Field Position
  - Success Rate range
  - Tags
  - Favorites only
- Sort options:
  - Name (A-Z, Z-A)
  - Date Created (newest, oldest)
  - Success Rate (high to low)
  - Last Used
- Search bar (name, tags)
- Pagination (20 per page)
- Bulk actions: Select multiple, delete, export
- Empty state with "Create First Formation" CTA

**Acceptance Criteria**:
- [ ] Grid and list views work
- [ ] Formation cards display correctly
- [ ] Filters apply correctly (combine with AND)
- [ ] Sort works for all options
- [ ] Search returns relevant results
- [ ] Pagination works
- [ ] Bulk actions work
- [ ] Empty state displays when no formations
- [ ] Unit tests cover filtering/sorting

**Dependencies**: Backend formations API

**Files to Create**:
- `app/playbook/page.tsx`
- `components/Playbook/FormationCard.tsx`
- `components/Playbook/FormationList.tsx`
- `components/Playbook/FiltersPanel.tsx`
- `hooks/usePlaybook.ts`

---

### FRONT-14: Formation Comparison View

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 7

**Description**:
Build side-by-side formation comparison interface.

**Technical Requirements**:
- Select 2-4 formations to compare
- Split screen layout (2 formations) or grid (3-4)
- Show for each formation:
  - Field diagram
  - Key metrics
  - Simulation results
  - Pros/cons
- Highlight differences:
  - Personnel package differences (color-coded)
  - Player position changes (arrows showing movement)
  - Performance metric deltas (+/- from average)
- Comparison table:
  - Metric rows, formation columns
  - Color-code best/worst values
- Export comparison as PDF/PNG
- Share comparison link

**Acceptance Criteria**:
- [ ] Can select 2-4 formations
- [ ] Split screen/grid renders correctly
- [ ] Differences are clearly highlighted
- [ ] Comparison table is accurate
- [ ] Export works for PDF and PNG
- [ ] Share link generates and works
- [ ] Responsive on tablet and desktop
- [ ] Unit tests cover comparison logic

**Dependencies**: Backend comparison API

**Files to Create**:
- `app/compare/page.tsx`
- `components/Comparison/ComparisonView.tsx`
- `components/Comparison/ComparisonTable.tsx`
- `components/Comparison/DifferenceHighlighter.tsx`
- `hooks/useComparison.ts`

---

### FRONT-15: Analytics Dashboard Page

**Priority**: P2 (Medium)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 7

**Description**:
Build analytics dashboard with charts and insights.

**Technical Requirements**:
- Charts:
  - Formation success rate by personnel package (bar chart)
  - EPA distribution by formation type (histogram)
  - Run vs Pass efficiency (scatter plot)
  - Success rate by field position (heat map)
  - Formation usage frequency (pie chart)
  - Success rate trend over time (line chart)
- Time range selector: 7 days, 30 days, Season, All Time
- Export all charts to PDF/CSV
- Interactive tooltips on hover
- Drill-down: Click chart to see formation details
- Filters: Personnel, Formation Type, Down/Distance
- Key insights section:
  - Highest performing formations
  - Underutilized formations
  - Recommended personnel changes

**Acceptance Criteria**:
- [ ] All charts render correctly
- [ ] Charts update on time range change
- [ ] Tooltips show on hover
- [ ] Drill-down works
- [ ] Export includes all visible data
- [ ] Filters apply to all charts
- [ ] Insights are accurate and helpful
- [ ] Responsive on all screen sizes
- [ ] Unit tests cover chart data processing

**Dependencies**: Backend analytics API, Recharts

**Files to Create**:
- `app/analytics/page.tsx`
- `components/Analytics/ChartContainer.tsx`
- `components/Analytics/InsightsPanel.tsx`
- `hooks/useAnalytics.ts`

---

### FRONT-16: User Authentication Pages

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 8

**Description**:
Build login, registration, and password reset pages.

**Technical Requirements**:
- Login page:
  - Email and password fields
  - "Remember me" checkbox
  - "Forgot password" link
  - Form validation
  - Error messages for invalid credentials
  - Redirect to dashboard on success
- Registration page:
  - Name, email, password, confirm password
  - Password requirements displayed
  - Form validation
  - Email verification flow
- Password reset:
  - Enter email to receive reset link
  - Reset link opens form with new password
  - Confirmation on success
- JWT token stored in httpOnly cookie or localStorage
- Auto-logout on token expiration
- Protected routes redirect to login

**Acceptance Criteria**:
- [ ] Login works with valid credentials
- [ ] Error messages display for invalid input
- [ ] Registration creates new account
- [ ] Password reset flow works end-to-end
- [ ] Token stored securely
- [ ] Auto-logout works on token expiration
- [ ] Protected routes redirect correctly
- [ ] Unit tests cover form validation

**Dependencies**: Backend auth API

**Files to Create**:
- `app/login/page.tsx`
- `app/register/page.tsx`
- `app/reset-password/page.tsx`
- `components/Auth/LoginForm.tsx`
- `hooks/useAuth.ts`
- `lib/auth.ts`

---

### FRONT-17: Navigation and Layout

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 8

**Description**:
Build app navigation and consistent layout.

**Technical Requirements**:
- Top navigation bar:
  - Logo/app name
  - Main navigation links (Dashboard, Playbook, Analytics, Editor)
  - User menu (dropdown): Profile, Settings, Logout
  - Notification badge (unread count)
- Sidebar (optional, collapsible):
  - Quick links to favorite formations
  - Recent formations
  - Playbook sections
- Breadcrumbs for deep navigation
- Footer: Links, version, support
- Responsive: Mobile menu (hamburger)
- Active route highlighting
- Loading bar for page transitions

**Acceptance Criteria**:
- [ ] Navigation renders on all pages
- [ ] Links navigate correctly
- [ ] User menu works
- [ ] Active route highlighted
- [ ] Mobile menu works on small screens
- [ ] Breadcrumbs show correct path
- [ ] Loading bar displays on navigation
- [ ] Collapsible sidebar persists state

**Dependencies**: None

**Files to Create**:
- `components/Layout/Navigation.tsx`
- `components/Layout/Sidebar.tsx`
- `components/Layout/UserMenu.tsx`
- `components/Layout/Breadcrumbs.tsx`

---

### FRONT-18: Notifications System

**Priority**: P2 (Medium)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 9

**Description**:
Build in-app notification system for alerts and updates.

**Technical Requirements**:
- Notification types:
  - Success (green)
  - Error (red)
  - Warning (yellow)
  - Info (blue)
- Display methods:
  - Toast (auto-dismiss after 5 seconds)
  - Banner (persist until dismissed)
  - Badge (notification count in nav)
- Notification center (dropdown):
  - List of recent notifications
  - Mark as read
  - Clear all
- Real-time notifications via WebSocket (optional)
- Notification preferences (settings page)
- Notification history page

**Acceptance Criteria**:
- [ ] Toasts appear and auto-dismiss
- [ ] Banners persist until dismissed
- [ ] Badge shows correct count
- [ ] Notification center works
- [ ] Mark as read updates count
- [ ] Clear all removes all notifications
- [ ] Preferences save correctly
- [ ] Unit tests cover notification logic

**Dependencies**: None

**Files to Create**:
- `components/Notifications/Toast.tsx`
- `components/Notifications/NotificationCenter.tsx`
- `hooks/useNotifications.ts`
- `lib/notifications.ts`

---

### FRONT-19: Responsive Design & Mobile Support

**Priority**: P1 (High)
**Story Points**: 8
**Assignee**: TBD
**Sprint**: Sprint 9

**Description**:
Ensure all components are fully responsive and work on mobile.

**Technical Requirements**:
- Breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px
- Mobile-specific adjustments:
  - Navigation: Hamburger menu
  - Formation editor: Touch-friendly controls
  - Field canvas: Pinch to zoom, two-finger pan
  - Tables: Horizontal scroll or stacked layout
  - Forms: Full-width inputs
- Touch gestures:
  - Tap to select
  - Long press for context menu
  - Swipe to delete
  - Pinch to zoom (field canvas)
- Test on real devices (iOS, Android)
- Progressive Web App (PWA) support (optional)

**Acceptance Criteria**:
- [ ] All pages responsive on mobile/tablet
- [ ] Navigation works on mobile
- [ ] Formation editor usable on tablet
- [ ] Touch gestures work correctly
- [ ] No horizontal scroll on mobile
- [ ] Passes mobile usability tests
- [ ] Works on iOS 14+ and Android 10+

**Dependencies**: All frontend components

**Files to Update**:
- All component files for responsive styles

---

### FRONT-20: Performance Optimization

**Priority**: P1 (High)
**Story Points**: 5
**Assignee**: TBD
**Sprint**: Sprint 10

**Description**:
Optimize frontend performance for fast load times and smooth interactions.

**Technical Requirements**:
- Code splitting: Lazy load routes and heavy components
- Image optimization: Next.js Image component, WebP format
- Bundle size reduction:
  - Tree shaking
  - Remove unused dependencies
  - Minimize bundle size < 500KB (gzipped)
- Caching strategies:
  - Cache API responses (SWR or React Query)
  - Cache formation thumbnails
  - LocalStorage for user preferences
- Performance monitoring:
  - Lighthouse score > 90
  - First Contentful Paint < 1.5s
  - Time to Interactive < 3s
- Optimize canvas rendering:
  - Use requestAnimationFrame
  - Debounce expensive operations
  - Virtualize long lists

**Acceptance Criteria**:
- [ ] Bundle size < 500KB gzipped
- [ ] Lighthouse score > 90
- [ ] FCP < 1.5s
- [ ] TTI < 3s
- [ ] Canvas maintains 60fps
- [ ] Long lists virtualized
- [ ] No unnecessary re-renders
- [ ] Performance budget met

**Dependencies**: All frontend components

**Files to Update**:
- `next.config.js` for bundle analysis
- All components for optimization

---

## Summary

**Total Tickets**: 20
**Total Story Points**: 127

**Breakdown by Priority**:
- P0 (Critical): 8 tickets, 67 points
- P1 (High): 10 tickets, 52 points
- P2 (Medium): 2 tickets, 13 points

**Estimated Timeline**: 10 sprints (20 weeks) at 12-13 points per sprint
