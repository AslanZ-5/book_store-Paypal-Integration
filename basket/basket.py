from decimal import Decimal

from django.conf import settings

from store.models import Product
from checkout.models import DeliveryOptions

class Basket():
    """
    A base Basket class, providing some default behaviors that 
    can be inherited or overrided, as necessary.
    """
    def __init__(self,request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in  request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket
    def add(self,product,qty):
        """Adding and updating the users basket session data """
        product_id = str(product.id)
        if product_id  in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.regular_price),'qty':int(qty)}
        self.save() 
    
    def __iter__(self):
        """
            Collect the product_id in the session data to query the database
            and return products
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item 
    
    def __len__(self):
        """ Get the basket data and count the qty of items"""
        
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        subtotal =  sum(item['qty'] * Decimal(item['price']) for item in self.basket.values())
        newprice = 0.00
        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        
        total = subtotal + Decimal(newprice)
        return total
    def delivery_price(self):
        price = 0.00
        if 'purchase' in self.session:
            price = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
            return price
    def get_delivery_id(self):
        if 'purchase' in self.session:
            id = self.session['purchase']['delivery_id']
            return id
    def get_subtotal_price(self):
        return sum(item['qty'] * Decimal(item['price']) for item in self.basket.values())

    def basket_update_delivery(self,del_price=0):
        return sum(item['qty'] * Decimal(item['price']) for item in self.basket.values()) + Decimal(del_price)

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
  
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product, qty):
        """ 
        Update values in session data
        """
        product_id = str(product)

        if product_id  in self.basket:
            self.basket[product_id]['qty'] = qty 
            self.basket[product_id]['total_price'] = qty * float(self.basket[product_id]['price'])
            
        self.save()

    def get_total_item(self,id):
        product_id = str(id)
        return Decimal(self.basket[product_id]['price']) * int(self.basket[product_id]['qty'])
    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        del self.session['address']
        del self.session['purchase']
        self.save()