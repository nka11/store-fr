from decimal import Decimal as D

from oscar.apps.shipping.methods import Free, FixedPrice
from oscar.apps.shipping.repository import Repository as CoreRepository
from oscar.core.loading import get_model

WeightBased = get_model('shipping','WeightBased')

class Repository(CoreRepository):
    """
    This class is included so that there is a choice of shipping methods.
    Oscar's default behaviour is to only have one which means you can't test
    the shipping features of PayPal.
    """

    def get_methods(self):
        return WeightBased.objects.all()

    def get_shipping_methods(self, user, basket, shipping_addr=None,
                             request=None, **kwargs):
        methods = self.get_methods()
        result = []
        for method in methods:
            if method is not None:
                method.set_basket(basket)
                result.append(method)
        return result

    def find_by_code(self, code, basket):
        for method in self.get_methods():
            if code == method.code:
                return self.prime_method(basket, method)

    def prime_method(self, basket, method):
        method.set_basket(basket)
        try:
            method.charge_incl_tax
        except:
            return None

        return method
