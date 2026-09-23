"""rename_invoked_at_to_revoked_at

Revision ID: 297989a01ddf
Revises: 6d0e4a270d4d
Create Date: 2026-09-23 22:09:57.526199

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "297989a01ddf"
down_revision: str | Sequence[str] | None = "6d0e4a270d4d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("alter table refresh_tokens rename column invoked_at to revoked_at")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("alter table refresh_tokens rename column revoked_at to invoked_at")
