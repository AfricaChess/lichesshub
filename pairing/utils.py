from collections import defaultdict


class Pairing(object):
    def __init__(self, players, history=None):
        self.players = [
            {
                'id': i['id'],
                'score': i['score'],
                'paired': False
            } for i in players]
        self.output = []
        self.remainder = []

        self.history = defaultdict(list)
        if history:
            for left, right in history:
                self.history[left].append(right)
        #if history:
        #    self.history = history
        #else:
        #    self.history = {}

        score = sum([i['score'] for i in players])
        if score == 0:
            self.slide()
        else:
            self.proximity()

    def proximity(self):
        '''Used when scores > 0'''
        i = 0
        while i < len(self.players):
            if not self.players[i]['paired']:
                k = i + 1
                if k >= len(self.players):
                    self.remainder = {
                        'id': self.players[i]['id'],
                        'score': self.players[i]['score']
                    }
                    i += 1
                    continue
                while self.players[k]['paired']:
                    k += 1
                while self.have_played(
                        self.players[i]['id'], self.players[k]['id']):
                    k += 1
                self.output.append(
                    (self.players[i]['id'], self.players[k]['id']))
                self.players[i]['paired'] = True
                self.players[k]['paired'] = True
                print 'i is ', i, ', k is ', k
            i += 1

    def slide(self):
        '''used to pair when scores == 0'''
        midway = len(self.players)/2
        first = self.players[:midway]
        rest = self.players[midway:]
        out = [(i['id'], k['id']) for i, k in zip(first, rest)]

        if len(rest) > len(first):
            self.remainder = [{'id': rest[-1]['id'], 'score': rest[-1]['score']}]
        else:
            self.remainder = []
        self.output = out

    def have_played(self, left, right):
        if not self.history:
            return False
        if self.history.get(right) and left in self.history.get(right):
            return True
        if self.history.get(left) and right in self.history.get(left):
            return True
        return False


#def pair(players):
#    groups = []
#    remainder = []
#
#    current_score = players[0]['score']
#    current_group = []
#    for player in players:
#        if player['score'] == current_score:
#            current_group.append(player)
#        else:
#            p = Pairing(current_group)
#            groups.extend(p.output)
#            current_group = p.remainder
#
#            current_score = player['score']
#            current_group.append(player)
#
#    if current_group:
#        p = Pairing(current_group)
#        groups.extend(p.output)
#        remainder = p.remainder
#    return groups, remainder
