from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from operations.models import GoodCate, Good, Purchase_records, ReturnSale, Employees


def show(request):
    status = request.session.get('login')
    if status:
        num = request.GET.get('id')
        cate_name = GoodCate.objects.filter(level=1)
        good_name =GoodCate.objects.filter(level=2)
        sell_num = request.GET.get('sell_num')
        times = request.GET.get('times')
        employee=request.GET.get('employee')
        good_name1 = request.GET.get('good_name')
        two_name = request.GET.get('two_name')
        three_name = request.GET.get('three_name')
        print(sell_num,times)
        if not num:
            num = 1
        if sell_num:
            good=Good.objects.all().order_by('-sell_num')
            paginator = Paginator(good, per_page=5)
            pg = paginator.page(num)
            print(pg.object_list)

            return render(request, 'operations/home.html', {'good': pg,
                                                            'cate_name': cate_name,
                                                            'good_name': good_name,
                                                            'three_name': three_name,
                                                            'two_name': two_name,
                                                            'good_name1': 'good_name1',
                                                            'times': 'times',
                                                            'sell_num': 'sell_num'})
        if times:
            good=Good.objects.all().order_by('-date')
            paginator = Paginator(good, per_page=5)
            pg = paginator.page(num)
            print(pg.object_list)
            return render(request, 'operations/home.html', {'good': pg,
                                                            'cate_name': cate_name,
                                                            'good_name': good_name,
                                                            'three_name': three_name,
                                                            'two_name': two_name,
                                                            'good_name1': 'good_name1',
                                                            'times': 'times',
                                                            'sell_num': 'sell_num'})
        if good_name1:
            good1_id=GoodCate.objects.filter(good_cate_name=good_name1)[0].id
            good=Good.objects.filter(good_id_id=good1_id)
        if two_name:
            id1 = GoodCate.objects.filter(good_cate_name=two_name)[0].id
            class_id =GoodCate.objects.filter(parent_id=id1)
            list_id = []
            for i in class_id:
                list_id.append(i.id)
            for j in list_id:
                # j 文章表中的的class+id 来查询所属文章
                good1 = Good.objects.filter(parent_id=j)
            good =good1
        if three_name:
            id2 = GoodCate.objects.filter(good_cate_name=three_name)[0].parent_id
            id3 = GoodCate.objects.filter(good_cate_name=three_name)[0].id
            # 覆盖掉一级标题
            two_name = GoodCate.objects.filter(pk=id2)[0].good_cate_name
            # 通过id3查询二级标题的文章
            good = Good.objects.filter(good_id_id=id3)
        else:
            good=Good.objects.all()
        paginator = Paginator(good, per_page=5)
        pg = paginator.page(num)
        print(pg.object_list)
        return render(request, 'operations/home.html',{'good':pg,
                                                       'cate_name':cate_name,
                                                       'good_name':good_name,
                                                       'three_name': three_name,
                                                       'two_name': two_name,
                                                       'good_name1':'good_name1',
                                                       'times':'times',
                                                       'sell_num':'sell_num'})
    else:
        return redirect('userapp:login')

def addgood(request):
    cate_name=GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    return render(request,'operations/addGood.html',{'cate_name':cate_name,
                                                     'good_name':good_name})
#添加商品逻辑
def addgood_logic(request):
    try:
        name=request.POST.get('goodname')
        cate_name=request.POST.get('cate_sel')
        good_name=request.POST.get('good_sel')
        date = request.POST.get('date')
        text = request.POST.get('text')
        id = GoodCate.objects.filter(good_cate_name=good_name)[0].id
        print(id,name,cate_name,good_name,date,text)
        rst=Good.objects.create(name=name,good_name=good_name,date=date,content=text,good_id_id=id)
        if rst:
            return JsonResponse({'msg': '恭喜添加成功', 'status': 1})
        else:
            return JsonResponse({'msg': '添加失败', 'status': 0})
    except:
        return JsonResponse({'msg':'添加失败','status':0})

def addemployee(request):
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    return render(request, 'operations/add_employee.html', {'cate_name': cate_name,
                                                       'good_name': good_name})
#添加员工逻辑
def addemployee_logic(request):
    try:
        name=request.POST.get('name')
        sex=request.POST.get('gender')
        age=request.POST.get('age')
        tel=request.POST.get('tel')
        position=request.POST.get('position_sel')
        print(name,sex,age,tel,position)
        rst=Employees.objects.create(name=name,sex=sex,age=age,tel=tel,position=position)
        if rst:
            return JsonResponse({'msg': '恭喜添加成功', 'status': 1})
        else:
            return JsonResponse({'msg': '添加失败', 'status': 0})
    except:
        return JsonResponse({'msg': '添加失败', 'status': 0})

#二级联动
def together(request):
    name = request.GET.get('name')
    # 获取 good表的数据,名称和等级
    id =GoodCate.objects.filter(good_cate_name=name)[0].id
    class_name = GoodCate.objects.filter(parent_id=id)
    a = []
    for i in class_name:
        a.append(i.good_cate_name)
    return JsonResponse({'msg': a})

def add_purchase_record(request):
    cate_name=GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    return render(request,'operations/addpurchase_record.html',{'cate_name':cate_name,
                                                                'good_name':good_name})
#添加进货记录
def add_purchase_logic(request):
    try:
        with transaction.atomic():
            name = request.POST.get('purchasename')
            date = request.POST.get('date')
            num = request.POST.get('num')
            address = request.POST.get('address')
            content = request.POST.get('text')
            print(name, date, num, address, content)
            rst=Purchase_records.objects.create(name=name,data=date,num=num,address=address,content=content)
            if rst:
                return JsonResponse({'msg': '添加成功1', 'status': 1})
            else:
                return JsonResponse({'msg': '添加失败', 'status': 0})
    except:
        return JsonResponse({'msg': '添加失败', 'status': 0})

def modify(request):
    id1 = request.GET.get('id1')
    request.session['id']=id1
    good=Good.objects.get(id=id1)
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    return render(request,'operations/modify.html',{'good':good,
                                                    'cate_name':cate_name,
                                                    'good_name':good_name})
#修改商品逻辑
def modify_logic(request):
    id=request.session.get('id')
    name=request.POST.get('goodname')
    good_name=request.POST.get('good_sel')
    num=request.POST.get('num')
    date=request.POST.get('date')
    content=request.POST.get('text')
    good=Good.objects.get(id=id)
    print(id,name,good_name,num,date,content)
    try:
        with transaction.atomic():
            if good:
                good.name=name
                good.good_name=good_name
                good.date=date
                good.sell_num=num
                good.content=content
                good.save()
                return JsonResponse({'msg':'修改商品成功','status':1})
    except:
        return JsonResponse({'msg':'此商品不存在','status':0})

def modify_employee(request):
    id1 = request.GET.get('id7')
    request.session['id7']=id1
    emp=Employees.objects.get(id=id1)
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    return render(request,'operations/modify_employee.html',{'emp':emp,
                                                    'cate_name':cate_name,
                                                    'good_name':good_name})
#修改员工逻辑
def modifyepm_logic(request):
    id=request.session.get('id7')
    name=request.POST.get('name')
    position=request.POST.get('position_sel')
    age=request.POST.get('age')
    sex=request.POST.get('sex')
    tel=request.POST.get('tel')
    emp=Employees.objects.get(id=id)
    print(id,name,position,sex,age,tel)
    try:
        with transaction.atomic():
            if emp:
                emp.name=name
                emp.sex=sex
                emp.age=age
                emp.position=position
                emp.tel=tel
                emp.save()
                return JsonResponse({'msg':'修改员工信息成功','status':1})
    except:
        return JsonResponse({'msg':'此员工不存在','status':0})
#删除商品逻辑
def dele(request):
    try:
        with transaction.atomic():
            id=request.GET.get('id2')
            good=Good.objects.get(id=id)
            good.delete()
            return redirect('operations:show')
    except:
        return  redirect('operations:show')

def purchase(request):
    num = request.GET.get('id')
    purchase=Purchase_records.objects.all()
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    if not num:
        num = 1
    paginator = Paginator(purchase, per_page=5)
    pg = paginator.page(num)
    return render(request,'operations/home_purchase.html',{'purchase':pg,
                                                           'cate_name': cate_name,
                                                           'good_name': good_name,
                                                           })
def return_purchase(request):
    num = request.GET.get('id')
    return_purchase=ReturnSale.objects.all()
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    if not num:
        num = 1
    paginator = Paginator(return_purchase, per_page=5)
    pg = paginator.page(num)
    return render(request,'operations/return_purchase.html',{'return_purchase':pg,
                                                           'cate_name': cate_name,
                                                           'good_name': good_name,
                                                           })

def employees(request):
    num = request.GET.get('id')
    emp=Employees.objects.all()
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    if not num:
        num = 1
    paginator = Paginator(emp, per_page=5)
    pg = paginator.page(num)
    return render(request, 'operations/employees.html', {'employees': pg,
                                                        'cate_name': cate_name,
                                                        'good_name': good_name})
#删除员工逻辑
def dele_employee(request):
    try:
        with transaction.atomic():
            id=request.GET.get('id4')
            emp=Employees.objects.get(id=id)
            emp.delete()
            return redirect('operations:employees')
    except:
        return  redirect('operations:employees')
#删除进货记录逻辑
def dele_purchase(request):
    try:
        with transaction.atomic():
            id=request.GET.get('id5')
            purchase=Purchase_records.objects.get(id=id)
            purchase.delete()
            return redirect('operations:purchase')
    except:
        return  redirect('operations:purchase')
#删除退货记录逻辑
def dele_returnpurchase(request):
    try:
        with transaction.atomic():
            id=request.GET.get('id6')
            return_purchase=ReturnSale.objects.get(id=id)
            return_purchase.delete()
            return redirect('operations:return_purchase')
    except:
        return  redirect('operations:return_purchase')

#模糊查询

def select1(request):
    name=request.POST.get('rst')
    request.session['a']=name
    print(name)
    if name:
        return JsonResponse({'msg':'查询成功','status':1})
    else:
        return JsonResponse({'msg':'输入为空，请重新输入','status':0})

def select(request):
    name=request.session.get('a')
    print(name)
    good=Good.objects.filter(name__icontains=name)[0]
    cate_name = GoodCate.objects.filter(level=1)
    good_name = GoodCate.objects.filter(level=2)
    two_name = request.GET.get('two_name')
    three_name = request.GET.get('three_name')
    return render(request, 'operations/home_select.html', {'good': good,
                                                    'cate_name': cate_name,
                                                    'good_name': good_name,
                                                    'three_name': three_name,
                                                    'two_name': two_name,
                                                    'good_name1': 'good_name1',
                                                    'times': 'times',
                                                    'sell_num': 'sell_num'})


