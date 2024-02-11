# Generated by Django 5.0.1 on 2024-01-23 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0012_alter_annualroster_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='trans_event',
            field=models.CharField(choices=[('Verbal Commitment from High School', 'Verbal Commitment from High School'), ('Verbal Commitment from College', 'Verbal Commitment from College'), ('National Letter of Intent Signed', 'National Letter of Intent Signed'), ('Decommit', 'Decommit'), ('Entered Transfer Portal', 'Entered Transfer Portal'), ('Verbal Commitment to Transfer College', 'Verbal Commitment to Transfer College'), ('Signed Professional Contract', 'Signed Professional Contract'), ('No Longer With Program - Other Reason', 'No Longer With Program - Other Reason')], max_length=64),
        ),
    ]