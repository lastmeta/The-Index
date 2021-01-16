class User():
    def __init__(self, credit: float, vote: str, against: int):
        self.credit = credit
        self.vote = vote
        self.against = against
        self.trades = {}

    def __repr__(self):
        return (
            f'\n  credit    {self.credit}'
            f'\n  vote      {self.vote}'
            f'\n  against   {self.against}'
            f'\n  trades    {self.trades}')

    def trade(self, asset, amount):
        self.trades[asset] = amount

    def complete_trades(self, credit):
        self.trades = {}
        self.credit += credit


class Index():
    def __init__(self, users: list, assets: dict, rates: dict):
        self.users = users
        self.assets = assets
        self.rates = rates
        self.mana = {}
        self.weight = {}

    def __repr__(self):
        return (
            f'\nusers   {self.users}'
            f'\nassets  {self.assets}'
            f'\nrates   {self.rates}'
            f'\nmana    {self.mana}'
            f'\nweight  {self.weight}'
            f'\nvalue   {self.value()}')

    def value(self):
        return {k: v * self.rates[k] for k, v in self.assets.items()}

    def clear_mana(self):
        self.mana = {k: 0 for k, v in self.mana.items()}

    def generate_ideal_allocation(self, mana_total):
        values = self.value()
        values_total = sum([v for v in values.values()])
        self.weight = {
            # I thought you had to weight it according to how large the asset is, but I guess not...
            # k: (self.mana[k] / mana_total) * (v / values_total)  
            k: (self.mana[k] / mana_total)
            for k, v in values.items()}
        return {k: v + (v * self.weight[k]) for k, v in values.items()}

    def apply_trades(self):
        ''' assumes only valid trades exist '''
        for user in self.users:
            credit_for_user = 0
            print(self.assets, user.credit)
            for k, amount in user.trades.items():
                self.assets[k] += amount
                credit_for_user += (amount * self.rates[k])
            user.complete_trades(credit_for_user)
            print(self.assets, user.credit)

    def negotiate_allocations(self, ideal, trade, mana_total):
        print('self.weight', self.weight)
        for k, value in trade.items():
            print(
                f'\n{k}: {value} + abs({ideal[k]} - {value}) * {self.weight[k]}',
                f'\n{k}: {value} + {abs(ideal[k] - value)} * {self.weight[k]}',
                f'\n{k}: {value} + {abs(ideal[k] - value) * self.weight[k]}'
                f'\n{k}: {value + abs(ideal[k] - value) * self.weight[k]}')
        return {
            k: value + abs(ideal[k] - value) * self.weight[k]
            for k, value in trade.items()}

    def rate_translation(self, negotiation):
        '''
        if the negotiation was our value and our asset counts is what it is,
        what would the rates have to be?
        '''
        for k, v in negotiation.items():
            print(k, 'rate:', self.rates[k], 'v:', v, 'count:', self.assets[k], '()', v / self.assets[k])
            self.rates[k] = v / self.assets[k]
        return None

    def round(self):
        '''
        1. take allocation of value from last round
        2. generate mana, tally up what it was spent on
           (in demo you can only vote for one asset: all mana is excess mana)
        3. generate ideal allocation
        4. tally up and apply trades
        5. calculate achieved allocation via trading
        6. modify achieved allocation according to mana spent
        7. translate allocation into an effect on rates and apply
        '''
        self.clear_mana()
        mana_total = 0
        for user in self.users:
            self.mana[user.vote] = user.credit * user.against
            mana_total += user.credit
        ideal = self.generate_ideal_allocation(mana_total)
        print('ideal', ideal)
        self.apply_trades()
        trade = self.value()
        print('trade', trade)
        negotiation = self.negotiate_allocations(ideal, trade, mana_total)
        print('negotiation', negotiation)
        self.rate_translation(negotiation)

def run():
    users = [
        User(credit=1, vote='btc', against=1),
        User(credit=2, vote='eth', against=1),
        User(credit=3, vote='xmr', against=-1)]
    assets = {'btc': 1, 'eth': 2, 'xmr': 3}
    rates = {'btc': 1, 'eth': 2, 'xmr': 3}
    index = Index(users, assets, rates)
    index.round()
    users[0].trade('btc', 1)
    index.round()
    users[2].trade('xmr', -3)
    index.round()
    users[1].trade('eth', -1)
