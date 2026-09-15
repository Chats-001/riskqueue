# Architecture

```mermaid
flowchart LR
    A[PaySim CSV] --> B[Contract validation]
    B --> C[History-only features]
    C --> D[Chronological split]
    D --> E[Logistic + boosted models]
    E --> F[Calibration and metrics]
    F --> G[Cost + capacity policy]
    G --> H[FastAPI]
    H --> I[(PostgreSQL audit log)]
    I --> J[Streamlit operations view]
    C --> K[Offline drift checks]
```

The batch feature builder is intentionally explicit rather than streaming. A real deployment would maintain aggregates in online feature infrastructure; this project precomputes them to keep the methodology reproducible and inspectable.

