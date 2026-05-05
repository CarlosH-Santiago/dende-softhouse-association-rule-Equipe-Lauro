import pandas as pd

def perform_eda(df):
    print("--- Exploratory Data Analysis (EDA) ---")
    print(f"Total de transações registradas: {len(df)}")
    
    # separa a coluna de produtos pelo ponto e vírgula (;) 
    # e explodir em uma lista para contar corretamente cada item vendido.
    split_items = df['descricao_produtos'].dropna().str.split(';').explode()
    
    # Limpa espaços e deixa minúsculo para a análise visual
    split_items = split_items.str.strip().str.lower()
    
    top_products = split_items.value_counts().head(10)
    
    print("\nTop 10 Produtos Mais Vendidos:")
    print(top_products)
    
    return top_products

def clean_item_name(item):
    """Padroniza o nome removendo espaços extras e maiúsculas."""
    item_clean = str(item).strip().lower()
    return item_clean

def generate_tid_sets(df):
    print("\n--- Pré-processamento: Formato Vertical (TID-sets) ---")
    tid_sets = {}

    for index, row in df.iterrows():
        tid = row['id_transacao'] # Pega o ID real da transação
        produtos_str = row['descricao_produtos']
        
        # Pula se a linha estiver vazia (NaN)
        if pd.isna(produtos_str):
            continue
            
        # Separa as roupas daquela compra usando o ponto e vírgula
        items = str(produtos_str).split(';')
        
        for item in items:
            formatted_item = clean_item_name(item)
            
            if not formatted_item :
                continue
                
            if formatted_item not in tid_sets:
                tid_sets[formatted_item] = set()
            tid_sets[formatted_item].add(tid)
            
    print(f"Total de categorias únicas prontas para o ECLAT: {len(tid_sets)}")
    return tid_sets


if __name__ == '__main__':
    arquivo_csv = './vendas_dataset.csv' 
    
    try:
        df_retail = pd.read_csv(arquivo_csv)
        
        top_items = perform_eda(df_retail)
        vertical_data = generate_tid_sets(df_retail)

        print("\nExemplo de Saída Vertical (Para validar na Apresentação):")
        for item in list(vertical_data.keys())[:3]:
            print(f"Item '{item}' comprado nas transações: {vertical_data[item]}")

    except FileNotFoundError:
        print("Erro: vendas_dataset.csv não encontrado na pasta.")