AthleteOps
==========

AthleteOps is a personal backend system designed to help student-athletes track tasks, health metrics, and personal finances, with automated weekly summaries computed via background workers.

This project focuses on backend architecture, asynchronous processing, and infrastructure rather than UI polish.

* * * * *

Core Features
-------------

-   **Task, Health, and Finance Tracking**

    -   Relational PostgreSQL data model for tasks, health logs, and transactions

    -   JWT-based authentication for user-scoped data access

-   **Automated Weekly Summaries**

    -   Background jobs compute:

        -   Average sleep (last 7 days)

        -   Total spending (last 7 days)

        -   Count of high-risk ("danger") tasks

    -   Results are persisted for historical analysis

-   **Asynchronous Processing**

    -   Redis-backed job queue using RQ

    -   Decoupled worker service executes batch jobs independently of the web server

-   **Containerized Architecture**

    -   Docker Compose setup with separate services for:

        -   FastAPI web app

        -   PostgreSQL

        -   Redis

        -   Background worker

    -   Designed to mirror real-world backend deployments

* * * * *

Tech Stack
----------

-   **Backend:** FastAPI, Python

-   **Database:** PostgreSQL, SQLAlchemy

-   **Async / Jobs:** Redis, RQ

-   **Auth:** JWT

-   **Infra:** Docker, Docker Compose

* * * * *

Architecture Overview
---------------------

1.  FastAPI handles authenticated API requests.

2.  Redis queues background jobs.

3.  RQ workers consume jobs and run batch computations.

4.  PostgreSQL stores both raw data and derived weekly summaries.

5.  Jobs can be triggered manually or scheduled externally (e.g., cron).

* * * * *

Status
------

This project is intentionally left feature-incomplete.

Its purpose was to explore backend systems design with FastAPI, while implementing background workers and containerized infrastructure.

Further UI work, notifications, or production hardening were intentionally deprioritized.
