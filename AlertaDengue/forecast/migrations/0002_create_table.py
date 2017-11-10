# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 00:41
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    """

    :param apps:
    :param schema_editor:
    :return:
    """

    if not schema_editor.connection.alias == 'forecast':
        return

    return migrations.RunSQL('''
    CREATE TABLE IF NOT EXISTS "forecast".forecast_model (
        id SERIAL PRIMARY KEY,
        name VARCHAR(128) NOT NULL,
        weeks SMALLINT NOT NULL,
        commit_id CHAR(7) NOT NULL,
        active BOOL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "forecast".forecast_cases (
        id SERIAL PRIMARY KEY,
        epiweek INT NOT NULL,
        geocode INT NOT NULL,
        cid10 character varying(5) NOT NULL,
        forecast_model_id INT,
        published_date date NOT NULL,
        init_date_epiweek date NOT NULL,
        cases INT NOT NULL,

        UNIQUE (
          epiweek, geocode, cid10, forecast_model_id, published_date
        ),
        FOREIGN KEY(forecast_model_id)
          REFERENCES "forecast".forecast_model(id),
        FOREIGN KEY(geocode)
          REFERENCES "Dengue_global"."Municipio"(geocodigo),
        FOREIGN KEY(cid10) REFERENCES "Dengue_global"."CID10"(codigo)
    );

    CREATE TABLE IF NOT EXISTS "forecast".forecast_city (
        id SERIAL PRIMARY KEY,
        geocode INT NOT NULL,
        forecast_model_id INT,
        active BOOL NOT NULL,
        UNIQUE (geocode, forecast_model_id),
        FOREIGN KEY(forecast_model_id) REFERENCES "forecast".forecast_model(id),
        FOREIGN KEY(geocode) REFERENCES "Dengue_global"."Municipio"(geocodigo)
    );
    ''')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dados', '__first__'),
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]