"""add projects and migrate tasks

Revision ID: b8809079db95
Revises: 80aba73db4cf
Create Date: 2026-08-09 18:54:47.581586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8809079db95'
down_revision: Union[str, Sequence[str], None] = '80aba73db4cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # --------------------------------------------------
    # STEP 1: Create projects table
    # --------------------------------------------------

    # op.create_table(
    #     "projects",

    #     sa.Column(
    #         "id",
    #         sa.Integer(),
    #         primary_key=True
    #     ),

    #     sa.Column(
    #         "name",
    #         sa.String(),
    #         nullable=False
    #     ),

    #     sa.Column(
    #         "description",
    #         sa.String(),
    #         nullable=True
    #     ),

    #     sa.Column(
    #         "user_id",
    #         sa.Integer(),
    #         nullable=False
    #     ),

    #     sa.ForeignKeyConstraint(
    #         ["user_id"],
    #         ["users.id"]
    #     )
    # )

    # --------------------------------------------------
    # STEP 2: Add project_id to tasks
    # temporarily nullable
    # --------------------------------------------------

    op.add_column(
        "tasks",
        sa.Column(
            "project_id",
            sa.Integer(),
            nullable=True
        )
    )

    # --------------------------------------------------
    # STEP 3: Create one default project
    # for every existing user
    # --------------------------------------------------

    connection = op.get_bind()

    users = connection.execute(
        sa.text(
            "SELECT id FROM users"
        )
    ).fetchall()

    for user in users:

        connection.execute(
            sa.text(
                """
                INSERT INTO projects
                (name, description, user_id)
                VALUES
                (:name, :description, :user_id)
                """
            ),
            {
                "name": "My Tasks",
                "description": "Default project",
                "user_id": user.id
            }
        )

    # --------------------------------------------------
    # STEP 4: Assign existing tasks
    # to their user's default project
    # --------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE tasks
            SET project_id = projects.id
            FROM projects
            WHERE tasks.user_id = projects.user_id
            AND projects.name = 'My Tasks'
            """
        )
    )

    # --------------------------------------------------
    # STEP 5: Add foreign key
    # --------------------------------------------------

    op.create_foreign_key(
        "fk_tasks_project_id",
        "tasks",
        "projects",
        ["project_id"],
        ["id"]
    )

    # --------------------------------------------------
    # STEP 6: Make project_id NOT NULL
    # --------------------------------------------------

    op.alter_column(
        "tasks",
        "project_id",
        nullable=False
    )

    # --------------------------------------------------
    # STEP 7: Remove old user_id
    # --------------------------------------------------

    op.drop_constraint(
        "tasks_user_id_fkey",
        "tasks",
        type_="foreignkey"
    )

    op.drop_column(
        "tasks",
        "user_id"
    )


def downgrade():

    # Add user_id back
    op.add_column(
        "tasks",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True
        )
    )

    # Restore user_id through project
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE tasks
            SET user_id = projects.user_id
            FROM projects
            WHERE tasks.project_id = projects.id
            """
        )
    )

    # Make user_id required again
    op.alter_column(
        "tasks",
        "user_id",
        nullable=False
    )

    # Remove project FK
    op.drop_constraint(
        "fk_tasks_project_id",
        "tasks",
        type_="foreignkey"
    )

    # Remove project_id
    op.drop_column(
        "tasks",
        "project_id"
    )

    # Remove projects table
    op.drop_table(
        "projects"
    )
