# MSRTC Risk Register (Pre-Launch)

| ID | Risk Description | Impact | Probability | Mitigation Plan | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | Redis memory fragmentation under extreme load | High | Medium | Implemented FinOps monitoring and anomaly alerting. Vertically scale if > 80% usage. | Platform Team | Accepted |
| R-02 | Third-party Payment Gateway timeouts during Diwali spike | Critical | High | Implemented strict circuit breakers and asynchronous webhook reconciliation. | Payments Team | Mitigated |
