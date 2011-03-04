from sarpaminfohub.infohub.models import ExchangeRate

class CurrencyExchange:
    def exchange(self, local_price, currency, year):
        if local_price is None: 
            return None
        
        if currency is None:
            return None
        
        try:
            exchange = ExchangeRate.objects.get(symbol=currency, year=year)
        except ExchangeRate.DoesNotExist:
            print "Currency = %s, Year = %d" % (currency, year)
            raise

        return local_price * exchange.rate
