import streamlit as st
import os
import sys
from core.analytics import AnalyticsService

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import init_db 
from core.services import DocumentService

if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None
if "current_page" not in st.session_state:
    st.session_state.current_page = 0

init_db()
service = DocumentService()
analytics = AnalyticsService()

st.set_page_config(page_title="PDF Manager", layout='wide')
st.title("SMART PDF DOCUMENT MANAGER")
st.divider()
tabs = st.tabs(['Upload', 'Search & View', 'Analytics'])
with tabs[0]:
    st.header("Upload PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    tags = st.text_input("Enter tags for the document (comma-separated)")
    description = st.text_area("Enter a description for the document")
    lecture_date = st.date_input("Select the lecture date", value=None)

    if st.button("Upload"):
        if uploaded_file and tags and description:           
            service.upload_document(
                filename=uploaded_file.name,
                filepath=uploaded_file,                
                tags=tags,
                description=description               
            )
        else:
            st.error("Please upload a PDF file before clicking the Upload button.")

        
    

with tabs[1]:
    # search and view logic
    col1, col2 = st.columns(2)
    with col1:
        search_tags = st.text_input("Search by tags (comma-separated)")
        if search_tags and st.button("Search Tags"):
            st.session_state.search_results = service.search_documents_tags(search_tags)
            
        else:
            st.warning("Please enter tags to search.")
    with col2:
            search_description = st.text_input("Search by description")
            if search_description and st.button("Search Description"):
                pass

    results = st.session_state.search_results
    if results and not st.session_state.reader_mode:
        st.subheader(f" Results: {len(results)} document(s) found.")
        container = st.container(height=500)
        with container:
            for doc in results:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(doc.thumbnail_path, width=100)
                with col2:
                    st.markdown(f"**Filename:** {doc.filename}")
                    st.markdown(f"**Tags:** {doc.tags}")
                    st.markdown(f"**Description:** {doc.description}")
                    st.markdown(f"**Uploaded Date:** {doc.uploaded_date}")                        
                    if st.button("Open", key=f"view_{doc.id}"):
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 0
                        st.session_state.reader_mode = True
                        st.rerun()
                            
    if st.session_state.reader_mode and st.session_state.selected_doc:
        doc = st.session_state.selected_doc
        st.subheader(f"Viewing: {doc.filename}")
        images_dir = os.path.splitext(doc.filepath)[0]
        st.write(f"image directory: {images_dir}")
        st.write(f"Files: {os.listdir(images_dir)}")
        if not os.path.exists(images_dir):
            st.error("Images directory does not exist.")
        else:
            images = sorted([f for f in os.listdir(images_dir) if f.endswith('.png')])
            if images:
                current_page = st.session_state.current_page
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("Previous") and current_page > 0:
                        st.session_state.current_page -= 1
                        st.rerun()
                with col2:
                    st.write(f"Page {current_page + 1} of {len(images)}")
                    st.image(os.path.join(images_dir, images[current_page]), width=600)

                with col3:
                    if st.button("Next") and current_page < len(images) - 1:
                        st.session_state.current_page += 1
                        st.rerun()
            else:
                st.warning("No images found in the directory.")

            analytics_data = analytics.record_page_visit(doc.id, st.session_state.current_page)
            unique_pages = analytics.get_document_analytics(doc.id)
            progress = len(unique_pages) / doc.total_pages if doc.total_pages > 0 else 0
            st.progress(progress, text=f"Progress: {len(unique_pages)}/{doc.total_pages}")


        if st.button("Back to Search"):
            st.session_state.reader_mode = False
            st.session_state.selected_doc = None
            st.session_state.current_page = 0
            st.rerun()  

with tabs[2]:
    # analytics logic
    pass


