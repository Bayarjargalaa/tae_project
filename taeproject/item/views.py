from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings

def home(request):
    csv_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'other', 'name.xlsx')
    try:
        df = pd.read_excel(csv_path)
        print(df.head())
        # 'name' баганын нэрийг csv-д тааруулна уу
        item_names = df['Зураг'].tolist()
    except Exception as e:
        print(f"Алдаа гарлаа: {e}")
        item_names = []
    context = {
        'item_names': item_names
    }
    return render(request, 'common/home.html', context)