# Traceability matrix

Each KPA-04 screen ID maps to an SRS requirement, a proposed route, a build week and a status. Routes are proposals: Claude Code may refine them, but must update this file in the same commit.

Status values: Not started, In progress, Built (mock), Built (API), Reviewed by owner, Accepted. "Built (mock)" means the screen still runs on fixture adapters. The evidence column links to tests, spike notes or screenshots.

| Screen | Name | SRS | Proposed route | Week | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| PUB-001 | Brand and shared layout | R-PUB-001 | `(shared public layout)` | 1 | Not started | |
| PUB-002 | Homepage — public | R-PUB-002 | `/` | 1 | Not started | |
| PUB-003 | Social media, header and footer | R-PUB-003 | `(public header, social strip, footer)` | 1 | Not started | |
| PUB-004 | Course catalog / Explore | R-PUB-004 | `/courses` | 1 | Not started | |
| PUB-005 | Course details and free preview | R-PUB-005 | `/courses/:slug` | 1 | Not started | |
| PUB-006 | About Kasina | R-PUB-006 | `/about (#story, #instructors, #training, #contact)` | 1 | Not started | |
| AUTH-001 | Sign in, register and OTP | R-AUTH-001 | `/sign-in, /register, /verify` | 1 | Not started | |
| AUTH-002 | Portal selection and switching | R-AUTH-002 | `/portals (+ switcher in account menu)` | 1 | Not started | |
| STU-001 | Student — My Learning | R-STU-001 | `/learn` | 2 | Not started | |
| STU-002 | Student — Explore | R-STU-002 | `/learn/explore, /learn/explore/:slug` | 2 | Not started | |
| STU-003 | Enrollment and payment | R-STU-003 | `/learn/enroll/:slug` | 2 | Not started | |
| STU-004 | Payment status | R-STU-004 | `/learn/orders/:orderId` | 2 | Not started | |
| STU-005 | Course learning interface | R-STU-005 | `/learn/courses/:courseId/:activityId` | 2 | Not started | |
| STU-006 | Assessments — consolidated view | R-STU-006 | `/learn/courses/:courseId/assessments` | 3 | Not started | |
| STU-007 | Quiz and results | R-STU-007 | `/learn/courses/:courseId/quiz/:activityId` | 3 | Not started | |
| STU-008 | Practical assessment and submission | R-STU-008 | `/learn/courses/:courseId/practical/:activityId` | 3 | Not started | |
| STU-009 | Practical review status | R-STU-009 | `/learn/courses/:courseId/practical/:activityId/attempts/:attemptId` | 3 | Not started | |
| STU-010 | Certificates | R-STU-010 | `/learn/certificates, /learn/certificates/:id` | 3 | Not started | |
| STU-011 | Account, history, notifications and support | R-STU-011 | `/learn/account (/history, /notifications, /contact)` | 4 | Not started | |
| ACD-001 | Shared editor — details | R-ACD-001 | `/{teach|admin}/courses/:id/details` | 2 | Not started | |
| ACD-002 | Curriculum | R-ACD-002 | `/{teach|admin}/courses/:id/curriculum` | 2 | Not started | |
| ACD-003 | Unified lesson editor | R-ACD-003 | `/{teach|admin}/courses/:id/lessons/:activityId` | 2 | Not started | |
| ACD-004 | Lesson video states | R-ACD-004 | `(state of ACD-003 video section)` | 2 | Not started | |
| ACD-005 | Quiz editor | R-ACD-005 | `/{teach|admin}/courses/:id/quizzes/:activityId` | 3 | Not started | |
| ACD-006 | Practical assessment editor | R-ACD-006 | `/{teach|admin}/courses/:id/practicals/:activityId` | 3 | Not started | |
| ACD-007 | Assessments overview | R-ACD-007 | `/{teach|admin}/assessments, /{teach|admin}/courses/:id/assessments` | 3 | Not started | |
| ACD-008 | Practical submission review | R-ACD-008 | `/{teach|admin}/reviews/:attemptId` | 3 | Not started | |
| ACD-009 | Quiz results and course assessments | R-ACD-009 | `/{teach|admin}/courses/:id/quizzes/:activityId/results` | 3 | Not started | |
| ACD-010 | Individual academic record | R-ACD-010 | `/{teach|admin}/students/:studentId` | 3 | Not started | |
| ACD-011 | Course announcements | R-ACD-011 | `/{teach|admin}/courses/:id/announcements` | 3 | Not started | |
| INS-001 | Instructor Dashboard | R-INS-001 | `/teach` | 3 | Not started | |
| INS-002 | My courses | R-INS-002 | `/teach/courses` | 3 | Not started | |
| INS-003 | My students | R-INS-003 | `/teach/students` | 3 | Not started | |
| INS-004 | My profile | R-INS-004 | `/teach/profile` | 3 | Not started | |
| ADM-001 | Admin dashboard | R-ADM-001 | `/admin` | 4 | Not started | |
| ADM-002 | Manage courses | R-ADM-002 | `/admin/courses` | 2 | Not started | |
| ADM-003 | Manage staff | R-ADM-003 | `/admin/staff` | 4 | Not started | |
| ADM-004 | Manage students | R-ADM-004 | `/admin/students` | 4 | Not started | |
| ADM-005 | Enrollment management | R-ADM-005 | `/admin/students/:id/enrollments` | 2 | Not started | |
| ADM-006 | Payments | R-ADM-006 | `/admin/payments, /admin/payments/:orderId` | 2 | Not started | |
| ADM-007 | Certificates | R-ADM-007 | `/admin/certificates` | 3 | Not started | |
| ADM-008 | Financial reports | R-ADM-008 | `/admin/reports/financial` | 4 | Not started | |
| ADM-009 | Academic & enrollment reports | R-ADM-009 | `/admin/reports/academic` | 4 | Not started | |
| ADM-010 | Messages inbox | R-ADM-010 | `/admin/messages` | 4 | Not started | |
| ADM-011 | Message conversation | R-ADM-011 | `/admin/messages/:conversationId` | 4 | Not started | |
| ADM-012 | Contact Kasina | R-ADM-012 | `/about#contact, /learn/account/contact` | 4 | Not started | |
| ADM-013 | Settings home | R-ADM-013 | `/admin/settings` | 4 | Not started | |
| ADM-014 | Academy information | R-ADM-014 | `/admin/settings/academy` | 4 | Not started | |
| ADM-015 | Website content | R-ADM-015 | `/admin/settings/website` | 4 | Not started | |
| ADM-016 | Homepage content editor | R-ADM-016 | `/admin/settings/website/homepage` | 4 | Not started | |
| ADM-017 | Payment settings | R-ADM-017 | `/admin/settings/payments` | 4 | Not started | |
| ADM-018 | Learning settings | R-ADM-018 | `/admin/settings/learning` | 4 | Not started | |
| ADM-019 | Notifications | R-ADM-019 | `/admin/settings/notifications` | 4 | Not started | |
| ADM-020 | Security & activity | R-ADM-020 | `/admin/settings/security` | 4 | Not started | |
| TG-001 | Learn at Kasina — Telegram | R-TG-001 | `Mini App shell → student routes` | 4 (prep), 5–8 | Not started | |

## Phase 2 requirements

| Requirement | Name | Week | Status | Evidence |
| --- | --- | --- | --- | --- |
| R-P2-01 | Telegram Mini App container | 5 | Not started | |
| R-P2-02 | Telegram authentication | 5 | Not started | |
| R-P2-03 | Identity linking | 5 | Not started | |
| R-P2-04 | Bot notifications | 6 | Not started | |
| R-P2-05 | Deep links | 6 | Not started | |
| R-P2-06 | Online payment (Chapa) | 7 | Not started | |
| R-P2-07 | Telegram payment rules gate | 5 | Not started | |
| R-P2-08 | Uploads and media in Telegram | 6 | Not started | |
| R-P2-09 | Phase 2 acceptance | 8 | Not started | |

## Cross-cutting requirements

| Requirement | Topic | Week first needed | Status |
| --- | --- | --- | --- |
| R-CORE-01 | Identity, portals, server-side scope | 1 | Not started |
| R-CORE-02 | Activity types, completion, 90% coverage, no locks | 2 | Not started |
| R-CORE-03 | Content changes vs progress and certificates | 3 | Not started |
| R-CORE-04 | Payment / access / academic states, renewal | 2 | Not started |
| R-CORE-05 | Money, dates, revenue definition, cash, refunds | 2 | Not started |
| R-CORE-06 | Reporting cohorts and CSV | 4 | Not started |
| R-CORE-07 | Sessions, audit, step-up OTP (no MFA, D-04) | 1 | Not started |
| R-CORE-08 | UI states, accessibility, language | 1 | Not started |
