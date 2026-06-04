"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False, server_default=sa.text("'editor'")),
        sa.Column("email", sa.String(length=255)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.CheckConstraint("role IN ('admin', 'reviewer', 'editor', 'viewer')", name="role_check"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "points",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_ja", sa.String(length=255), nullable=False),
        sa.Column("lat", sa.Numeric(precision=10, scale=6), nullable=False),
        sa.Column("lng", sa.Numeric(precision=10, scale=6), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("idx_points_name", "points", ["name"])

    op.create_table(
        "countries",
        sa.Column("iso_id", sa.String(length=16), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_ja", sa.String(length=255), nullable=False),
        sa.Column("capital_point_id", sa.Integer(), sa.ForeignKey("points.id")),
        sa.Column("exist_from", sa.Date()),
        sa.Column("exist_until", sa.Date()),
        sa.Column("summary", sa.Text()),
        sa.Column("summary_jp", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("idx_countries_name", "countries", ["name"])

    op.create_table(
        "international_orgs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_ja", sa.String(length=255), nullable=False),
        sa.Column("headquarters_point_id", sa.Integer(), sa.ForeignKey("points.id"), nullable=False),
        sa.Column("exist_from", sa.Date()),
        sa.Column("exist_until", sa.Date()),
        sa.Column("summary", sa.Text()),
        sa.Column("summary_jp", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("idx_international_orgs_name", "international_orgs", ["name"])

    op.create_table(
        "member_countries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("org_id", sa.Integer(), sa.ForeignKey("international_orgs.id"), nullable=False),
        sa.Column("country_id", sa.String(length=255), sa.ForeignKey("countries.iso_id"), nullable=False),
        sa.Column("joined_at", sa.Date()),
        sa.Column("belonged_to_until", sa.Date()),
        sa.Column("status", sa.String(length=50)),
        sa.Column("status_jp", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.UniqueConstraint("org_id", "country_id", "joined_at", name="member_countries_org_id_country_id_joined_at_key"),
    )
    op.create_index("idx_member_countries_org_id", "member_countries", ["org_id"])
    op.create_index("idx_member_countries_country_id", "member_countries", ["country_id"])

    op.create_table(
        "member_orgs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("greater_org_id", sa.Integer(), sa.ForeignKey("international_orgs.id"), nullable=False),
        sa.Column("member_org_id", sa.Integer(), sa.ForeignKey("international_orgs.id"), nullable=False),
        sa.Column("joined_at", sa.Date()),
        sa.Column("belonged_to_until", sa.Date()),
        sa.Column("status", sa.String(length=50)),
        sa.Column("status_jp", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.CheckConstraint("greater_org_id <> member_org_id", name="no_self_membership"),
    )
    op.create_index("idx_member_orgs_greater_org_id", "member_orgs", ["greater_org_id"])
    op.create_index("idx_member_orgs_member_org_id", "member_orgs", ["member_org_id"])

    op.create_table(
        "local_forces",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_ja", sa.String(length=255), nullable=False),
        sa.Column("headquarters_point_id", sa.Integer(), sa.ForeignKey("points.id")),
        sa.Column("exist_from", sa.Date()),
        sa.Column("exist_until", sa.Date()),
        sa.Column("summary", sa.Text()),
        sa.Column("summary_jp", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("idx_local_forces_name", "local_forces", ["name"])

    op.create_table(
        "maps",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_ja", sa.String(length=255), nullable=False),
        sa.Column("owner", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("read_permission", sa.String(length=20), nullable=False),
        sa.Column("edit_permission", sa.String(length=20), nullable=False),
        sa.Column("exist_from", sa.Date(), nullable=False),
        sa.Column("exist_until", sa.Date(), nullable=False),
        sa.Column("time_scale", sa.String(length=20), nullable=False),
        sa.Column("summary", sa.Text()),
        sa.Column("summary_jp", sa.Text()),
        sa.Column("regulations", sa.Text()),
        sa.Column("source_url", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.CheckConstraint(
            "read_permission IN ('private', 'shared', 'public') AND edit_permission IN ('private', 'shared', 'public')",
            name="permission_check",
        ),
        sa.CheckConstraint(
            "time_scale IN ('hundred_years', 'ten_years', 'five_years', 'one_year', 'one_month', 'one_week', 'one_day')",
            name="time_scale_check",
        ),
    )
    op.create_index("idx_maps_owner", "maps", ["owner"])

    op.create_table(
        "map_points",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("map_id", sa.Integer(), sa.ForeignKey("maps.id"), nullable=False),
        sa.Column("point_id", sa.Integer(), sa.ForeignKey("points.id"), nullable=False),
        sa.Column("color", sa.String(length=16)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.UniqueConstraint("map_id", "point_id", name="map_points_map_id_point_id_key"),
    )

    op.create_table(
        "link_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_ja", sa.String(length=255), nullable=False),
        sa.Column("map_id", sa.Integer(), sa.ForeignKey("maps.id"), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("color", sa.String(length=16)),
        sa.Column("animated", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("idx_link_types_map_id", "link_types", ["map_id"])

    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("map_id", sa.Integer(), sa.ForeignKey("maps.id"), nullable=False),
        sa.Column("link_type", sa.Integer(), sa.ForeignKey("link_types.id"), nullable=False),
        sa.Column("point_from", sa.Integer(), sa.ForeignKey("points.id"), nullable=False),
        sa.Column("point_to", sa.Integer(), sa.ForeignKey("points.id"), nullable=False),
        sa.Column("exist_from", sa.Date(), nullable=False),
        sa.Column("exist_until", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.UniqueConstraint(
            "map_id",
            "link_type",
            "point_from",
            "point_to",
            "exist_from",
            name="links_map_id_link_type_point_from_point_to_exist_from_key",
        ),
    )
    op.create_index("idx_links_map_id", "links", ["map_id"])
    op.create_index("idx_links_point_from", "links", ["point_from"])
    op.create_index("idx_links_point_to", "links", ["point_to"])
    op.create_index("idx_links_link_type", "links", ["link_type"])

    op.create_table(
        "link_details",
        sa.Column("link_id", sa.Integer(), sa.ForeignKey("links.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("summary_ja", sa.Text(), nullable=False),
        sa.Column("source_url", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("link_details")
    op.drop_index("idx_links_link_type", table_name="links")
    op.drop_index("idx_links_point_to", table_name="links")
    op.drop_index("idx_links_point_from", table_name="links")
    op.drop_index("idx_links_map_id", table_name="links")
    op.drop_table("links")
    op.drop_index("idx_link_types_map_id", table_name="link_types")
    op.drop_table("link_types")
    op.drop_table("map_points")
    op.drop_index("idx_maps_owner", table_name="maps")
    op.drop_table("maps")
    op.drop_index("idx_local_forces_name", table_name="local_forces")
    op.drop_table("local_forces")
    op.drop_index("idx_member_orgs_member_org_id", table_name="member_orgs")
    op.drop_index("idx_member_orgs_greater_org_id", table_name="member_orgs")
    op.drop_table("member_orgs")
    op.drop_index("idx_member_countries_country_id", table_name="member_countries")
    op.drop_index("idx_member_countries_org_id", table_name="member_countries")
    op.drop_table("member_countries")
    op.drop_index("idx_international_orgs_name", table_name="international_orgs")
    op.drop_table("international_orgs")
    op.drop_index("idx_countries_name", table_name="countries")
    op.drop_table("countries")
    op.drop_index("idx_points_name", table_name="points")
    op.drop_table("points")
    op.drop_table("users")