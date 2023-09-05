from rest_framework import generics
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemInventory, CategorySerializer, UserGroupSerializer, CartSerializer, OrderItemSerializer
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from .throttle import TenPerMinute
from django.http import HttpResponse

# Create your views here.

# class based views
class MenuItemViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemInventory

class SingleMenuItemViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemInventory

class CategoryViews(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryViews(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# use function
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        category_name = request.GET.get('Category')
        to_price = request.GET.get('to_price')
        search = request.GET.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        # filter by category model in column title
        if category_name:
            items = items.filter(Category__title=category_name)
        # filter by price
        if to_price:
            items = items.filter(price__lte=to_price)
        # filter by title
        if search:
            items = items.filter(title__icontains = search)
            
        if ordering:
            ordering_list=ordering.split(",")
            items = items.order_by(*ordering_list)
        items = items.filter(feature=True)
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except:
            items = []
        
        # serialized_item = MenuItemInventory(item, many=True)
        serialized_item = MenuItemInventory(items, many=True)
        return Response(serialized_item.data)
    
    check = request.user.groups.filter(name='Manager').exists()
    if check < 1:
        return Response({'Message' : 'You are not allowed'}, status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        serialized_item = MenuItemInventory(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def singlemenu_items(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    check = request.user.groups.filter(name='Manager').exists()

    if request.method == 'GET':
        serialized_item = MenuItemInventory(item)
        return Response(serialized_item.data)
    
    if check < 1:
        return Response({'Message' : 'You are not authorized'}, status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serialized_item = MenuItemInventory(instance=item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.update(item, request.data)
        return Response({'Message' : 'Success update data'}, status.HTTP_202_ACCEPTED)
    if request.method == 'DELETE':
        item.delete()
        return Response({'Message' : 'success delete'}, status.HTTP_200_OK)

@api_view()
def category_detail(request, pk):
    item = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(item)
    return Response(serialized_category.data)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    employee = User.objects.filter(name='Manager').all()
    serialized_employee = UserGroupSerializer(employee, many=True)
    if serialized_employee:
        return Response(serialized_employee.data)
    else:
        return Response({"message" : "You are not authorized"}, 403)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu_feature(request):
    check = request.user.groups.filter(name='Manager').exists()
    if check < 1:
        return Response({'Message' : 'You are not allowed'}, status.HTTP_401_UNAUTHORIZED)
    menu = MenuItem.objects.filter(feature=True)
    if menu:
        serialized_menu = MenuItemInventory(menu, many=True)
        return Response(serialized_menu.data)
    else:
        return Response({'message' : 'Not found what you want? lets add it'})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updated_menu_feature(request, pk=None):
    check = request.user.groups.filter(name='Manager').exists()
    if check < 1:
        return Response({'Message' : 'You are not allowed'}, status.HTTP_401_UNAUTHORIZED)
    menu_id = MenuItem.objects.filter(id=pk)
    if menu_id :
        menu_id = menu_id.update(feature=True)
    else:
        return Response('Not found', status.HTTP_404_NOT_FOUND)
    return Response("Success!!!", status.HTTP_200_OK)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenPerMinute])
def throttle_check_auth(request):
    return Response('Success')

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if user:  
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        if request.method == 'POST':
            managers.user_set.add(user)
        if request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({'message' : 'ok'})
    return Response({'message' : 'Error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew(request, pk):
    check = request.user.groups.filter(name='Manager').exists()
    checkadmin = request.user.is_superuser

    # i think 'and' in this context is become 'or'? actually in my pc does
    if check < 1 and checkadmin != True:
        return Response({'Message' : 'You are not authorized to access itdsds'}, status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(User, pk=pk)
    if user:
        managers = Group.objects.get(name="delivery-crew")
        managers.user_set.add(user)
        if request.method == 'POST':
            managers.user_set.add(user)
        if request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({'message' : 'ok'})
    return Response({'message' : 'Error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def listcart(request):
    pick_cart = Cart.objects.filter(user_id=request.user.id)
    
    serialized_cart = CartSerializer(pick_cart)
    if request.method == 'GET':
        return Response(serialized_cart.data)
    if request.method == 'POST':
        unit_price = MenuItem.objects.filter(id=request.POST.get('menuitem')).get()
        quantity = request.POST.get('quantity')
        total = float(unit_price.price) * int(quantity)

        serialized_cart = CartSerializer(data=request.data)
        serialized_cart.is_valid(raise_exception=True)
        serialized_cart.save(
            price=total,
            unit_price=unit_price.price,
            user = request.user
            )
        return Response({'Message' : 'Lets continue our shopp!!'}, status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        pick_cart.delete()
        return Response({'Message' : 'The menu has been deleted'}, status.HTTP_202_ACCEPTED)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'GET':
        order = OrderItem.objects.filter(order=request.user)
        serialized_orders = OrderItemSerializer(order)
        return Response(serialized_orders.data)
    
    if request.method =='POST':
        cart = Cart.objects.filter(user_id=request.user.id).get()
        model_order = {
            'order' : cart.user_id,
            'menuitem' : cart.menuitem_id,
            'quantity' : cart.quantity,
            'unit_price' : cart.unit_price,
            'price' : cart.price
        }
        if cart == None:
            return Response({'Message' : 'may your cart is empty?'})
        serialized_orders = OrderItemSerializer(data=model_order)
        serialized_orders.is_valid(raise_exception=True)
        serialized_orders.save()
        cart.delete()
        return Response({'Message' : 'Thank you customers'}, status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_order(request, pk=None): 
    order = get_object_or_404(OrderItem, pk=pk)
    serialized_order = OrderItemSerializer(order, many=True)
    
    return Response(serialized_order.data)