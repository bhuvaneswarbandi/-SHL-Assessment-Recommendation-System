import os

os.environ["STREAMLIT_SERVER_PORT"] = os.getenv("PORT", "8501")
os.environ["STREAMLIT_SERVER_ENABLECORS"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

import streamlit as st
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()


#qdrant_api_url = os.getenv("QDRANT_API_URL")
#qdrant_api_key = os.getenv("QDRANT_API_KEY")


model = SentenceTransformer("all-MiniLM-L6-v2")


qdrant_client = QdrantClient(
    url="https://f9bb9b6d-494b-47fd-901a-521fe2270112.us-west-1-0.aws.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.h2gYvCM_spmKzZqLB1pWMNgnFEsc8vMzzaoa3ZECV8I"
)


st.set_page_config(page_title="SHL", layout="centered")
st.title(" SHL Assessment Recommendation System")

query = st.text_input("Enter a topic or keyword:", "")
limit = st.slider("Select number of results", min_value=1, max_value=10, value=3)

if st.button("Search") and query:
    query_vector = model.encode(query).tolist()

    with st.spinner("Searching Qdrant..."):
        raw_results = qdrant_client.search(
            collection_name="course_data",
            query_vector=query_vector,  
            limit=10,             
            with_payload=True
        )

        unique_results = []
        seen_hashes = set()

        for result in raw_results:
            payload = result.payload
            title = payload.get("title", "")
            description = payload.get("description", "")
            hash_key = hashlib.md5((title + description).encode()).hexdigest()

            if hash_key not in seen_hashes:
                seen_hashes.add(hash_key)
                unique_results.append(payload)

            if len(unique_results) == limit:
                break

        if unique_results:
            st.success(f"Found {len(unique_results)} unique results.")
            for idx, payload in enumerate(unique_results, 1):
                with st.expander(f"Result {idx}: {payload.get('title', 'No Title')}"):
                    st.write(f"**Description**: {payload.get('description', 'N/A')}")
                    st.write(f"**Link**: [Visit]({payload.get('link', '#')})")
                    st.write(f"**Job Levels**: {payload.get('Job levels', 'N/A')}")
                    st.write(f"**Languages**: {payload.get('Languages', 'N/A')}")
                    st.write(f"**Assessment Length**: {payload.get('Assessment length', 'N/A')}")
                    st.write(f"**remote_testing**: {payload.get('remote_testing','N/A')}")
                    st.write(f"**adaptive_irt**: {payload.get('adaptive_irt','N/A')}")

        else:
            st.warning("No unique results found.")
