from django.urls import path

from operations import views

app_name='operations'

urlpatterns=[
    path('show/',views.show,name='show'),
    path('addgood/',views.addgood,name='addgood'),
    path('addgoodlogic/',views.addgood_logic,name='addgoodlogic'),
    path('together/',views.together,name='together'),
    path('addpurchase/',views.add_purchase_record,name='addpurchase'),
    path('addpurchaselogic/',views.add_purchase_logic,name='addpurchaselogic'),
    path('modify/',views.modify,name='modify'),
    path('modifylogic/',views.modify_logic,name='modifylogic'),
    path('dele/',views.dele,name='dele'),
    path('purchase/',views.purchase,name='purchase'),
    path('return_purchase/',views.return_purchase,name='return_purchase'),
    path('employees/',views.employees,name='employees'),
    path('addemployee/',views.addemployee,name='addemployee'),
    path('addemployeelogic/',views.addemployee_logic,name='addemployeelogic'),
    path('deleemployee/',views.dele_employee,name='deleemployee'),
    path('delepurchase/',views.dele_purchase,name='delepurchase'),
    path('delereturnpurchase/',views.dele_returnpurchase,name='delereturnpurchase'),
    path('modifyemp/',views.modify_employee,name='modifyemp'),
    path('modifyemplogic/',views.modifyepm_logic,name='modifyemplogic'),
    path('select/',views.select,name='select'),
    path('select1/',views.select1,name='select1'),
]