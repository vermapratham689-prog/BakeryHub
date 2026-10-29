from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [('marketplace', '0001_initial')]
    operations = [
        migrations.CreateModel(name='Campaign', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=140)), ('description', models.TextField(blank=True)),
            ('target_audience', models.CharField(blank=True, max_length=120)), ('start_date', models.DateField()),
            ('end_date', models.DateField()), ('budget', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ('status', models.CharField(choices=[('Draft', 'Draft'), ('Scheduled', 'Scheduled'), ('Active', 'Active'), ('Paused', 'Paused'), ('Completed', 'Completed')], default='Draft', max_length=12)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='marketplace.shop')),
        ], options={'ordering': ['-created_at']}),
        migrations.AddConstraint(model_name='campaign', constraint=models.CheckConstraint(condition=models.Q(('end_date__gte', models.F('start_date'))), name='campaign_end_after_start')),
        migrations.CreateModel(name='Coupon', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('code', models.CharField(max_length=32)), ('discount_type', models.CharField(choices=[('percent', 'Percentage'), ('fixed', 'Fixed amount')], default='percent', max_length=10)),
            ('discount_value', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
            ('minimum_order', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
            ('valid_until', models.DateTimeField(blank=True, null=True)), ('usage_limit', models.PositiveIntegerField(default=100)), ('times_used', models.PositiveIntegerField(default=0)), ('active', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='marketplace.shop')),
        ], options={'ordering': ['-created_at']}),
        migrations.AddConstraint(model_name='coupon', constraint=models.UniqueConstraint(fields=('shop', 'code'), name='unique_coupon_code_per_shop')),
        migrations.CreateModel(name='MarketingEvent', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('event_type', models.CharField(choices=[('shop_view', 'Shop view'), ('menu_view', 'Menu view'), ('campaign_click', 'Campaign click'), ('coupon_redeem', 'Coupon redemption')], max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='marketplace.campaign')),
            ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketing_events', to='marketplace.shop')),
        ]),
    ]
