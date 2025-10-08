import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render

def home(request):
    excel_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'other', 'name.xlsx')

    try:
        df = pd.read_excel(excel_path)

        # Тухайн багануудыг ашиглах
        items = df.to_dict(orient='records')  # [{ 'Зураг': 'apple.jpg', 'Нэр': '...', ... }, ...]
        
        

    except Exception as e:
        print(f"Алдаа гарлаа: {e}")
        items = []
    context={
        'items': items,        
             }
    return render(request, 'common/home.html', context)
