import json
import pandas as pd
from itertools import combinations
from data_preprocessing import generate_tid_sets
from eclat_engine import find_frequent_itemsets

def calculate_rules_and_metrics(frequent_itemsets, total_transactions):
    print("\n--- Calculando Regras: Confiança e Lift ---")
    rules = []
    
    # Filtra apenas os conjuntos que têm 2 ou mais itens (para formar uma regra A -> B)
    combo_itemsets = {k: v for k, v in frequent_itemsets.items() if len(k) >= 2}
    
    for itemset, count_AB in combo_itemsets.items():
        # Desmembra o combo para testar as direções da regra
        for consequent_item in combinations(itemset, 1):
            consequent = frozenset(consequent_item)
            antecedent = itemset - consequent
            
            # Busca quantas vezes o Antecedente e o Consequente foram vendidos isoladamente
            count_A = frequent_itemsets.get(antecedent, 0)
            count_B = frequent_itemsets.get(consequent, 0)
            
            # Prevenção de divisão por zero 
            if count_A == 0 or count_B == 0:
                continue
                
            # CONFIDENCE: Qual a probabilidade de B ser comprado dado que A foi comprado?
            confidence = count_AB / count_A
            
            # LIFT: O quanto a compra de A alavanca a venda de B em relação ao normal?
            # Lift = Confiança / Suporte Relativo de B
            support_B_relative = count_B / total_transactions
            lift = confidence / support_B_relative
            
            if lift > 1.0:
                rules.append({
                    "antecedente": list(antecedent),
                    "consequente": list(consequent),
                    "suporte_vendas_juntas": count_AB,
                    "confianca": round(confidence, 4),
                    "lift": round(lift, 4)
                })
                
    print(f"Total de regras comerciais válidas geradas (Lift > 1): {len(rules)}")
    return rules

def export_to_json(rules, filename="combos.json"):
    # Pega as 5 melhores regras e exporta para JSON. 
    
    # Ordena as regras pelo maior Lift
    top_5_rules = sorted(rules, key=lambda x: x['lift'], reverse=True)[:5]
    
    # Salva o arquivo JSON garantindo a acentuação correta
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(top_5_rules, f, ensure_ascii=False, indent=4)
        
    print(f"\nSUCESSO! Ponte criada. Top 5 combos exportados para '{filename}'")
    for i, rule in enumerate(top_5_rules, 1):
        ant = " + ".join(rule['antecedente']).title()
        cons = rule['consequente'][0].title()
        print(f"  {i}. Dendê Softhouse Recomenda: Se comprar [{ant}] -> Mostre [{cons}] (Lift: {rule['lift']})")

if __name__ == '__main__':
    arquivo_csv = './vendas_dataset.csv'
    MIN_SUPPORT = 5
    
    try:
        df_retail = pd.read_csv(arquivo_csv)
        total_transacoes = len(df_retail)
        
        base_vertical = generate_tid_sets(df_retail)
        itens_frequentes = find_frequent_itemsets(base_vertical, MIN_SUPPORT)
        
        regras_geradas = calculate_rules_and_metrics(itens_frequentes, total_transacoes)
        export_to_json(regras_geradas)
        
    except Exception as e:
        print(f"Erro Crítico de Execução: {e}")
