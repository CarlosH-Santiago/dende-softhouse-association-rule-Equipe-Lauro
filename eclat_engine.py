import pandas as pd
from data_preprocessing import generate_tid_sets  

def run_toy_dataset_for_slides():
    print("\n" + "="*50)
    print("DATASET DE BRINQUEDO")
    print("="*50)
    
    # 1. Base fictícia de 5 vendas no formato vertical
    toy_tid_sets = {
        'camisa branca': {1, 2, 4, 5},
        'calça jeans': {1, 2, 4},
        'bone': {2, 3},
        'meia': {1, 4, 5}
    }
    
    print("\n1. Formato Vertical (TID-sets) Inicial:")
    for item, tids in toy_tid_sets.items():
        print(f"   {item}: {tids}")
        
    # Correção: Este bloco saiu de dentro do loop 'for'
    print("\n2. Executando Interseção do ECLAT (min_support = 2):")
    
    # Demonstração visual do cruzamento de conjuntos
    intersecao = toy_tid_sets['camisa branca'].intersection(toy_tid_sets['calça jeans'])
    print(f"   Cruzando: [camisa branca] {toy_tid_sets['camisa branca']} ∩ [calça jeans] {toy_tid_sets['calça jeans']}")
    print(f"   Resultado da Interseção: {intersecao}")
    print(f"   Suporte Final: {len(intersecao)} vendas juntas -> REGRA APROVADA ✅")
    print("="*50 + "\n")

def find_frequent_itemsets(tid_sets, min_support):
    """
    Motor lógico real do ECLAT usando Busca em Profundidade (DFS)
    """
    frequent_itemsets = {}
    
    def eclat_dfs(prefix, items):
        for i in range(len(items)):
            item_a, tid_a = items[i]
            support_a = len(tid_a)
            
            if support_a >= min_support:
                # Salva o itemset frequente atual. 
                # frozenset pq dicionários em Python exigem chaves imutáveis
                new_itemset = frozenset(prefix | {item_a})
                frequent_itemsets[new_itemset] = support_a
                
                # Gera as interseções condicionais para descer na árvore
                conditional_items = []
                for j in range(i + 1, len(items)):
                    item_b, tid_b = items[j]
                    
                    intersection = tid_a.intersection(tid_b)
                    
                    if len(intersection) >= min_support:
                        conditional_items.append((item_b, intersection))
                        
                # Chamada recursiva para achar trios e quartetos
                if conditional_items:
                    eclat_dfs(prefix | {item_a}, conditional_items)
                    
    # Converte o dicionário inicial para uma lista de tuplas para iterar ordenado
    items_list = list(tid_sets.items())
    eclat_dfs(set(), items_list)
    
    # Correção: O retorno obrigatório da função
    return frequent_itemsets
    

if __name__ == '__main__':
    # 1. Primeiro roda o teste pequeno para os slides
    run_toy_dataset_for_slides()
    
    # 2. Roda a Mineração na Base Real
    print("INICIANDO MINERAÇÃO NA BASE REAL...")
    arquivo_csv = './vendas_dataset.csv' 
    
    # Dica de Lucas: Suporte baixo 
    MIN_SUPPORT = 5 
    
    try:
        df_retail = pd.read_csv(arquivo_csv)
        base_vertical = generate_tid_sets(df_retail)
        
        print(f"\nBuscando combos com suporte mínimo de {MIN_SUPPORT} vendas...")
        
        # Chama o motor ECLAT
        itens_frequentes = find_frequent_itemsets(base_vertical, MIN_SUPPORT)
        
        print(f"Sucesso! Encontrados {len(itens_frequentes)} conjuntos de itens frequentes.")
        
        # Mostrando os 5 maiores combos (apenas com 2 peças ou mais)
        print("\n🏆 Top 5 Combos Mais Populares Encontrados:")
        
        # Filtra para mostrar apenas combos (len > 1) e ordena pelo suporte
        combos = {k: v for k, v in itens_frequentes.items() if len(k) > 1}
        top_combos = sorted(combos.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for itemset, support in top_combos:
            produtos = " + ".join(list(itemset))
            print(f"   [{produtos}] -> Vendidos juntos {support} vezes")
            
    except FileNotFoundError:
        print("Erro: O arquivo vendas_dataset.csv não foi encontrado.")