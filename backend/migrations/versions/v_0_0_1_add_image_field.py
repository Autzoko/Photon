from alembic import op
import sqlalchemy as sa

revision = 'add_image_fields'
down_version = 'v_0_0_0'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('images', sa.Column('original_filename', sa.String(), nullable=True))
    
    
def downgrade():
    op.drop_column('images', 'original_filename')
