from django.test import TestCase

# Create your tests here.
from core.datamanager import open_file_and_retrieve_data as of

df = of('../static/data/E0.csv')

from core.datamanager import convert_frame_dates
df = convert_frame_dates(df)

