# Project Specification – Electrical Load Calculation API

## Objective

Build a backend API that allows users to create electrical projects, define a distribution architecture, and perform power load calculations with result history.

The goal is to simulate a real-world engineering workflow used in electrical design offices, while focusing on backend architecture, scalability, and clean design.

---

## Target Users

- Electrical engineers
- Technicians
- Installers

Users want to quickly estimate the total power of a project without relying on spreadsheets, while ensuring traceability and reusability of calculations.

---

## Core Features (V1)

### Authentication

- User registration
- User login (JWT-based)

---

### Project Management

- Create a project
- Retrieve user projects
- Each project belongs to a single user (V1 scope)

---

### Electrical Architecture

- Define a hierarchical structure representing electrical distribution
- Example: main board → sub-distribution boards

---

### Consumers Management

- Add electrical consumers to a project
- Each consumer includes:
    - quantity
    - unit power
    - simultaneity factor
- Possibility to use predefined templates (optional in V1)

---

### Load Calculation

- Launch a power calculation for a project
- Compute total power based on defined consumers
- Store each calculation result

---

### Calculation History

- Keep track of all calculations per project
- Allow users to retrieve previous results

---

## Key Concepts

- **User**: authenticated account
- **Project**: container for an electrical installation
- **Electrical Structure**: hierarchical representation of the distribution system
- **Consumer**: electrical load element
- **Calculation**: stored result of a computation

---

## Constraints

- A user can only access their own projects
- Calculations must be stored and traceable
- The system must support hierarchical data
- The architecture must allow future async processing

---

## Technical Goals

- Clean architecture (routes / services / models / schemas)
- PostgreSQL database with migrations
- Dockerized environment
- Testable codebase (unit + integration tests)
- Production-ready structure

---

## Future Improvements (V2+)

- Asynchronous calculations (background jobs)
- Multi-user collaboration on projects
- Role-based permissions
- Consumers templates
- Result caching and optimization
- Export features:
    - PDF report
    - External tool format (e.g. Simaris)
- Advanced electrical calculations (voltage drop, cable sizing…)
- Soft Delete (is_deleted status in Project)

---

## Decisions

- Multi-user collaboration is postponed to V2 to reduce complexity
- Calculations are introduced as a dedicated entity to support history and future scalability
- A hierarchical structure is required to represent electrical distribution systems

## Architecture Decisions (V1)

### Data vs Computation

The system enforces a strict separation between stored data and computed values.

- The database stores only raw entities:
    - Project, ElectricBoard, Consumer
- No electrical loads or aggregates are persisted in these tables
- All load calculations are performed dynamically in the backend
- Only validated project states are stored as versioned snapshots

---

### Electrical Hierarchy

The electrical structure is modeled as a tree using a self-referencing relation.

- Each board has a `parent_id` (adjacency list model)
- Each project has exactly one root board (`parent_id = NULL`)
- The root board is created automatically at project creation
- All boards must belong to the same project as their parent
- Cycles are explicitly prevented to guarantee tree integrity

---

### Board Lifecycle

- Creating a board:
    - If no parent is provided, it is automatically attached to the root
- Moving a board:
    - Allowed via `parent_id` update with validation (no cross-project links, no cycles)
- Deleting a board:
    - Children are reattached to the deleted board’s parent
    - All associated consumers are deleted
- The root board cannot be deleted

---

### Consumer Model

Consumers represent electrical loads attached to boards.

- Defined by:
    - quantity
    - unit power
    - simultaneity factor
- Total load is always computed dynamically:
    - `quantity × unit_power × simultaneity`
- No computed values are stored in the database

---

### Versioning System

Validated project states are stored as immutable versions.

- A version represents:
    - a full project calculation result
    - the associated project structure at that time
- Each version stores:
    - total project load
    - per-board load distribution
    - per-consumer contributions (lightweight)
    - a snapshot of boards and consumers

This enables traceability and comparison of different project states over time.

---

### Calculation Workflow

Two distinct workflows are supported:

- Preview calculation:
    - used during editing
    - not persisted
    - can be scoped to a specific board subtree
- Version creation:
    - triggered explicitly by the user
    - computes the entire project from the root board
    - stores the result as an immutable version

This separation avoids unnecessary persistence while preserving meaningful history.

---

### API Design Decisions

- Consumer updates:
    - directly persist changes (auto-save behavior)
    - return computed values:
        - consumer total load
        - local board load (direct consumers only)
- Board retrieval (`GET /boards/{id}`):
    - computes the full subtree dynamically
    - returns a nested structure with aggregated loads
- Version management:
    - users can create and view versions
    - restoring a version is intentionally not supported in V1

---

### Design Principles

- Strict separation of concerns (data vs computation)
- No denormalized or redundant stored values
- Deterministic and reproducible calculations
- Explicit user-triggered persistence for versioning
- Simplicity prioritized over premature optimization

---

## Known Limitations (V1)

- Calculations are synchronous
- Single user per project
- No caching mechanism
- No export functionality yet

---

## Vision

This project is not just a calculation tool, but a backend system designed to handle real-world engineering workflows, with a focus on scalability, maintainability, and professional development practices.