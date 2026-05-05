import pandas as pd

def perform_eda(df):
    print("--- 🔍 Exploratory Data Analysis ---")
    
    null_transactions = df.isnull().all(axis=1).sum()
    print(f"Total de transações vazias: {null_transactions}")

    all_items = df.stack().reset_index(drop=True)
    top_products = all_items.value_counts().head(10)
    
    print("\nTop 10 Produtos:")
    print(top_products)
    
    return top_products

def generate_tid_sets(df):
    print("\n--- ⚙️ Pré-processamento: TID-sets ---")
    tid_sets = {}

    for tid, row in df.iterrows():
        items = row.dropna().unique()
        for item in items:
            if item not in tid_sets:
                tid_sets[item] = set()
            tid_sets[item].add(tid)
            
    print(f"Itens únicos processados: {len(tid_sets)}")
    return tid_sets

# --- Execução ---

arquivo_csv = './vendas_dataset.csv' 

try:
    df_retail = pd.read_csv(arquivo_csv, header=None)
    
    top_items = perform_eda(df_retail)
    vertical_data = generate_tid_sets(df_retail)

    print("\nExemplo de Saída Vertical:")
    for item in list(vertical_data.keys())[:3]:
        print(f"{item}: {vertical_data[item]}")

except FileNotFoundError:
    print("Erro: Ficheiro não encontrado.")