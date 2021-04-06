'''

Tema 2.

Gramatici independente de context.

Badea Adrian Catalin
Homner Dragos


Sa se scrie un program care primeste la intrare elementele unei gramatici independente de context oarecare,G,
inclusiv cu 𝜆-productii, pentru care:


a) calculeaza multimile First(X), Follow(X), pentru fiecare simbol X terminal sau neterminal

b) elimina recursivitatea la stanga (pentru gramatici fără 𝜆-producții)

c) factorizează stânga gramatica G. 

'''
eps = 'e'


class CFG():
    
    def __init__(self, input_file : str = 'inputs/cfg_follow.in'):
        
        self.productions = {}

        self.nonterminals = []
        self.terminals = []
    
        f = open(input_file, 'r')
    
        for line in f:
            
            nonterminal = line[0]
            self.nonterminals.append(nonterminal)
            
            prod = line[3:].strip('\n').split('|')
            
            self.productions[nonterminal] = prod
        
            for one_prod in prod:
                for car in one_prod:
                    if car not in self.terminals and car != eps and car.islower():
                        self.terminals.append(car)
        
        print("Productions : {}".format(self.productions))
        print("Nonterminals : {}".format(self.nonterminals))
        print("Terminals : {}".format(self.terminals))
        
    def _solve_first(self, node = 'S'):
        
        # https://www.geeksforgeeks.org/first-set-in-syntax-analysis/
        
        if self.first[node] != []:
            return
        
        has_eps = False
        
        if eps in self.productions[node]:
            has_eps = True
            
        if eps in self.productions[node]:
            self.first[node].append(eps)
            
        
        
        for prod in self.productions[node]:
            
            if prod == eps:
                continue
            
            
            
            node_first = []
        
            eps_poss = True
            
            for prod_elem in prod:
                
                self._solve_first(prod_elem)
                
                node_first += self.first[prod_elem] 
                
                
                if eps not in self.first[prod_elem]:
                    eps_poss = False
                    break
                
            if eps_poss == True:
                has_eps = True
                
            self.first[node] += list(set((node_first)))
        
        
        self.first[node] = list(set(self.first[node]))
        
        if eps in self.first[node]:
            self.first[node].remove(eps)
        
        if has_eps == True:
            self.first[node].append(eps)
        
        
    def _solve_follow(self, node = 'S'):
        
        # https://www.geeksforgeeks.org/follow-set-in-syntax-analysis/
        
        if node == 'S':
            self.follow[node].append('#')
            
        
        if eps in self.follow[node]:
            self.follow[node].remove(eps)
                
        self.follow[node] = list(set((self.follow[node])))
            
        #print(node)
        
        if node in self.terminals:
            return
        
        
        if self.visited[node] == True:
            return
        
        self.visited[node] = True
        
        
        for prod in self.productions[node]:
            
            if len(prod) == 1 and prod[0] == eps:
                continue
                
            
            for i in range(0, len(prod)):
                
                j = i + 1
                while j < len(prod):
                    
                    if prod[i] == 'B':
                        print(j)
                    
                    if eps in self.first[prod[j]]:
                        self.follow[prod[i]] += self.first[prod[j]]
                        j += 1
                    else:
                        break
                    
                if j < len(prod):
                    self.follow[prod[i]] += self.first[prod[j]]
                else:
                    self.follow[prod[i]] += self.follow[node]
            
                self._solve_follow(prod[i])
                
            
            
        if eps in self.follow[node]:
            self.follow[node].remove(eps)
                
        self.follow[node] = list(set((self.follow[node])))
        
      
        

    def make_first_and_follow(self):
        
        self.first = {}
        self.follow = {}
        
        for nonterm in self.nonterminals:
            self.first[nonterm] = []
            self.follow[nonterm] = []
            
        for term in self.terminals:
            self.first[term] = [term]
            self.follow[term] = [term]
            
        
        self._solve_first()
        
        for nonterm in self.nonterminals:
            if self.first[nonterm] == []:
                self._solve_first(nonterm)
        
        print("First set: {}".format(self.first))
        
        self.visited = {}
        
        for nonterm in self.nonterminals:
            self.visited[nonterm] = False 
            
        for term in self.terminals:
            self.visited[term] = False
        
        self._solve_follow()
        
        print("Follow set: {}".format(self.follow))
        


if __name__ == '__main__':
    
    cfg = CFG()
    cfg.make_first_and_follow()
    
   
    




