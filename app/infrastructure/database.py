from __future__ import annotations

import os

from psycopg_pool import ConnectionPool

DATABASE_URL = os.environ.get(
    "NEUROMESH_DATABASE_URL",
    "postgresql://neuromesh:neuromesh@localhost:5432/neuromesh",
)

# autocommit=True keeps each repository call a single,
# self-contained statement -- consistent with the in-memory
# repository's behavior, where every method call takes
# effect immediately. Multi-step transactions, if ever
# needed, should be handled explicitly at the call site,
# not hidden inside this shared pool config.
pool = ConnectionPool(
    DATABASE_URL,
    min_size=1,
    max_size=10,
    kwargs={"autocommit": True},
)
