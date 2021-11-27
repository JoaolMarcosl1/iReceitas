"""adicionei o atributo data_hora na entidade Comntarios

Revision ID: 147787e0b4ce
Revises: 5b949daff4c8
Create Date: 2021-11-26 13:55:08.737726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '147787e0b4ce'
down_revision = '5b949daff4c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_hora', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentarios', schema=None) as batch_op:
        batch_op.drop_column('data_hora')

    # ### end Alembic commands ###