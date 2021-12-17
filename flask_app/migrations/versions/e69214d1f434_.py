"""empty message

Revision ID: e69214d1f434
Revises: 7ad72bf00936
Create Date: 2021-12-15 11:02:50.142928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e69214d1f434'
down_revision = '7ad72bf00936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('interview',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate', sa.String(length=120), nullable=True),
    sa.Column('final_grade', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_candidate'), 'interview', ['candidate'], unique=True)
    op.create_table('interviewer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interviewers_interview',
    sa.Column('interviewer_id', sa.Integer(), nullable=False),
    sa.Column('interview_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], ),
    sa.ForeignKeyConstraint(['interviewer_id'], ['interviewer.id'], ),
    sa.PrimaryKeyConstraint('interviewer_id', 'interview_id')
    )
    op.create_table('interviewers_user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('interviewer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['interviewer_id'], ['interviewer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'interviewer_id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('essence', sa.String(length=140), nullable=True),
    sa.Column('supposed_answer', sa.String(length=250), nullable=True),
    sa.Column('max_grade', sa.Integer(), nullable=True),
    sa.Column('interview_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('rater_id', sa.Integer(), nullable=True),
    sa.Column('interview_id', sa.Integer(), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['rater_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('raters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raters',
    sa.Column('rater_id', sa.INTEGER(), nullable=True),
    sa.Column('rated_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['rated_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['rater_id'], ['user.id'], )
    )
    op.drop_table('grade')
    op.drop_table('question')
    op.drop_table('interviewers_user')
    op.drop_table('interviewers_interview')
    op.drop_table('interviewer')
    op.drop_index(op.f('ix_interview_candidate'), table_name='interview')
    op.drop_table('interview')
    # ### end Alembic commands ###