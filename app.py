import streamlit as st
import pymongo
import pandas as pd
from faker import Faker
from bson.objectid import ObjectId
import os


st.set_page_config(page_title="E-Shop Brasil - Admin", layout="wide")
st.title("🛒 E-Shop Brasil - Painel de Gestão de Dados (Big Data PoC)")


@st.cache_resource
def get_mongo_client():
    try:
        mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
        client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        client.server_info() 
        st.sidebar.success("Conectado ao MongoDB!")
        return client
    except pymongo.errors.ServerSelectionTimeoutError as err:
        st.sidebar.error(f"Falha ao conectar ao MongoDB: {err}")
        return None

client = get_mongo_client()

if client:
    db = client.eshop_db
    collection_products = db.products
    collection_users = db.users
    collection_logs = db.logs
else:
    st.error("Não foi possível conectar ao MongoDB. Verifique se o contêiner está em execução.")
    st.stop()



def generate_fake_data():
    fake = Faker('pt_BR')
    
    products = []
    for _ in range(50):
        products.append({
            "nome": fake.ecommerce_name(),
            "categoria": fake.ecommerce_category(),
            "preco": round(fake.random_number(digits=4) / 100, 2),
            "estoque": fake.random_int(min=0, max=200)
        })
    collection_products.insert_many(products)
    
    users = []
    for _ in range(100):
        users.append({
            "nome": fake.name(),
            "email": fake.email(),
            "estado": fake.state_abbr()
        })
    collection_users.insert_many(users)

    logs = []
    for _ in range(1000):
        logs.append({
            "timestamp": fake.date_time_this_year(),
            "user_id": fake.random_element(elements=[u['_id'] for u in collection_users.find({}, {"_id": 1})]),
            "action": fake.random_element(elements=["view_product", "add_to_cart", "checkout", "login"]),
            "product_id": fake.random_element(elements=[p['_id'] for p in collection_products.find({}, {"_id": 1})])
        })
    collection_logs.insert_many(logs)
    
    st.success("Dados falsos gerados e inseridos no MongoDB!")

st.sidebar.title("Menu de Navegação")
menu = st.sidebar.radio(
    "Selecione uma opção:",
    ("Visão Geral", "Gerenciar Dados (CRUD)", "Análise de Big Data (Agregação)")
)

if menu == "Visão Geral":
    st.header("Visão Geral da Prova de Conceito")
    st.markdown("""
    Esta aplicação simula a gestão de dados da E-Shop Brasil[cite: 68], utilizando:
    - **MongoDB:** Para armazenar dados flexíveis de produtos, usuários e logs.
    - **Streamlit:** Para criar esta interface gráfica de manipulação e análise.
    - **Docker:** Para garantir que a aplicação seja escalável e fácil de implantar.

    Use o menu ao lado para explorar as funcionalidades.
    """)
    
    if st.button("Gerar Dados Falsos (se o banco estiver vazio)"):
        generate_fake_data()

elif menu == "Gerenciar Dados (CRUD)":
    st.header("Gerenciamento de Dados (Inserir, Editar, Excluir)")
    
    col_name = st.selectbox("Selecione a Coleção:", ["products", "users", "logs"])
    collection = db[col_name]
    
    try:
        data = list(collection.find().limit(1000)) 
        df = pd.DataFrame(data)
        
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)
        
        st.dataframe(df, height=300)
        
        st.subheader(f"Operações na coleção '{col_name}'")
        
        doc_ids = [str(d["_id"]) for d in data]
        if doc_ids:
            selected_id_str = st.selectbox("Selecione um _id para Editar ou Excluir:", doc_ids)
            selected_doc = collection.find_one({"_id": ObjectId(selected_id_str)})
            
            if selected_doc:
                if st.button(f"Excluir Documento ({selected_id_str})", type="primary"):
                    collection.delete_one({"_id": ObjectId(selected_id_str)})
                    st.success("Documento excluído!")
                    st.experimental_rerun()
                
                st.write("---")
                st.write(f"**Editando:** {selected_id_str}")
                
                updates = {}
                for key, value in selected_doc.items():
                    if key != "_id":
                        if isinstance(value, (str, int, float)): 
                            updates[key] = st.text_input(f"Editar {key}", value=value)
                        else:
                            st.write(f"**{key}**: {value} (Tipo não editável na demo)")

                if st.button(f"Salvar Edições"):
                    update_data = {k: updates[k] for k in updates}
                    collection.update_one({"_id": ObjectId(selected_id_str)}, {"$set": update_data})
                    st.success("Documento atualizado!")
                    st.experimental_rerun()
            else:
                st.warning("ID selecionado não encontrado (pode ter sido excluído).")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

elif menu == "Análise de Big Data (Agregação)":
    st.header("Análise de Dados Logísticos e de Usuário")
    st.markdown("""
    Aqui simulamos análises que a E-Shop Brasil usaria para otimização logística e personalização. 
    Isso demonstra a "manipulação e concatenação" de dados através de agregações.
    """)

    st.subheader("1. Análise de Otimização Logística ")
    st.write("Contagem de produtos e estoque total por categoria (essencial para o controle de estoque).")
    
    if st.button("Executar Análise de Estoque"):
        pipeline_estoque = [
            {
                "$group": {
                    "_id": "$categoria",
                    "total_produtos": {"$sum": 1},
                    "estoque_total": {"$sum": "$estoque"}
                }
            },
            {
                "$sort": {"estoque_total": -1}
            }
        ]
        result_estoque = list(collection_products.aggregate(pipeline_estoque))
        df_estoque = pd.DataFrame(result_estoque).rename(columns={"_id": "Categoria"})
        st.bar_chart(df_estoque.set_index("Categoria"))
        st.dataframe(df_estoque)

    st.subheader("2. Análise de Personalização ")
    st.write("Contagem de ações de usuário (Big Data de logs) para entender o comportamento.")
    
    if st.button("Executar Análise de Logs"):
        pipeline_logs = [
            {
                "$group": {
                    "_id": "$action",
                    "contagem": {"$sum": 1}
                }
            },
            {
                "$sort": {"contagem": -1}
            }
        ]
        result_logs = list(collection_logs.aggregate(pipeline_logs))
        df_logs = pd.DataFrame(result_logs).rename(columns={"_id": "Ação"})
        st.bar_chart(df_logs.set_index("Ação"))
        st.dataframe(df_logs)