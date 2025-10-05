import streamlit as st
import requests
import json
import csv
import io
from datetime import datetime

# ENHANCED DARK THEME - REDESIGNED V3
st.markdown("""
<style>
    /* === CORE DARK THEME === */
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }
    
    /* === HEADER STYLING === */
    h1 {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 3rem;
        letter-spacing: -1px;
        border-bottom: 3px solid #00bcd4;
        padding-bottom: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .tagline {
        color: #00bcd4;
        font-size: 3.25rem;
        font-weight: 700;
        letter-spacing: 3px;
        margin: 1rem 0;
        text-transform: uppercase;
    }
    
    /* VERSION - 2.5X LARGER */
    .version {
        color: #999999;
        font-size: 20.25rem;
        font-weight: 700;
        margin-bottom: 2rem;
        line-height: 1.2;
    }
    
    /* === SECTION HEADERS === */
    h2, h3 {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 3rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    /* === LABELS === */
    .stTextInput > label,
    .stFileUploader > label {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .stCheckbox > label {
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    .stRadio > label {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* === INPUT FIELDS === */
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        border: 2px solid #00bcd4;
        border-radius: 8px;
        padding: 1.5rem;
        color: #000000;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00bcd4;
        box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.3);
        background-color: #FFFFFF;
    }
    
    /* === BUTTONS - LARGER TEXT === */
    .stButton > button {
        background: linear-gradient(135deg, #00bcd4, #00acc1);
        color: #0A0A0A;
        border: none;
        padding: 2rem 3rem;
        font-weight: 700;
        font-size: 4rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00acc1, #00bcd4);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 188, 212, 0.4);
    }
    
    .stButton > button:disabled {
        background: #333333;
        color: #666666;
        cursor: not-allowed;
        transform: none;
    }
    
    /* === FILE UPLOADER === */
    .stFileUploader {
        background-color: #1A1A1A;
        border: 2px dashed #00bcd4;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    /* === RADIO BUTTONS === */
    .stRadio > div {
        background-color: #1A1A1A;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #333333;
    }
    
    .stRadio > div label {
        font-size: 1.8rem;
        font-weight: 600;
        color: #FFFFFF;
    }
    
    /* === CHECKBOXES - BETTER CONTRAST === */
    .stCheckbox {
        background-color: #1A1A1A;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border: 2px solid #333333;
    }
    
    .stCheckbox:hover {
        border-color: #00bcd4;
        background-color: rgba(0, 188, 212, 0.1);
    }
    
    /* === EXPANDERS - OUTPUT 2.5X LARGER === */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(0, 188, 212, 0.1), rgba(0, 172, 193, 0.1));
        border-left: 3px solid #00bcd4;
        border-radius: 6px;
        font-weight: 700;
        font-size: 10rem;
        color: #FFFFFF;
        padding: 2rem;
    }
    
    .streamlit-expanderContent {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 0 0 6px 6px;
        padding: 2.5rem;
        font-size: 9rem;
        line-height: 1.8;
    }
    
    /* === OUTPUT TEXT - 2.5X LARGER === */
    .streamlit-expanderContent p {
        font-size: 9rem;
        line-height: 1.8;
        margin-bottom: 1.5rem;
    }
    
    .streamlit-expanderContent strong {
        color: #00bcd4;
        font-size: 9.5rem;
    }
    
    /* === MESSAGES - 2.5X LARGER === */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.2), rgba(0, 188, 212, 0.2));
        color: #00FF00;
        border-left: 4px solid #00FF00;
        border-radius: 6px;
        padding: 1.5rem;
        font-weight: 700;
        font-size: 9rem;
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.1);
        color: #ff5252;
        border-left: 4px solid #f44336;
        border-radius: 6px;
        padding: 1.5rem;
        font-weight: 600;
        font-size: 9rem;
    }
    
    .stWarning {
        background-color: rgba(255, 152, 0, 0.1);
        color: #ffab40;
        border-left: 4px solid #ff9800;
        border-radius: 6px;
        padding: 1.5rem;
        font-weight: 600;
        font-size: 9rem;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 188, 212, 0.1), rgba(0, 180, 216, 0.1));
        color: #00bcd4;
        border-left: 4px solid #00bcd4;
        border-radius: 6px;
        padding: 1.5rem;
        font-weight: 600;
        font-size: 9rem;
    }
    
    /* === DIVIDER === */
    hr {
        margin: 3rem 0;
        border: none;
        border-top: 2px solid #333333;
    }
    
    /* === DOWNLOAD BUTTONS === */
    .stDownloadButton > button {
        background-color: #1A1A1A;
        border: 2px solid #00bcd4;
        color: #00bcd4;
        padding: 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background-color: #00bcd4;
        color: #0A0A0A;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        color: #999999;
        font-size: 1.2rem;
        padding: 2rem 0;
        margin-top: 4rem;
        border-top: 2px solid #333333;
    }
    
    /* === CONNECTION STATUS - 1/3 SIZE === */
    .connection-status-green {
        background: linear-gradient(135deg, #00FF00, #00d900);
        color: #0A0A0A;
        font-weight: 900;
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-align: center;
        border: 2px solid #00FF00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.4);
    }

    .connection-status-red {
        background: linear-gradient(135deg, #ff5252, #f44336);
        color: #FFFFFF;
        font-weight: 900;
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-align: center;
        border: 2px solid #ff5252;
        box-shadow: 0 0 15px rgba(255, 82, 82, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="T!M - Transcript Intelligence Machine", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header
st.title("T!M - Transcript Intelligence Machine")
st.markdown('<p class="tagline">REDUCE THE GRIND. REVEAL THE BRILLIANCE.</p>', unsafe_allow_html=True)
st.markdown('<p class="version">MVP Demo Version 1.0</p>', unsafe_allow_html=True)

# Connection section
col1, col2 = st.columns([3, 1])
with col1:
    colab_url = st.text_input(
        "Colab API URL",
        placeholder="https://xxxx.ngrok-free.app",
        help="Enter your Colab ngrok URL to connect to the backend"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if colab_url:
        try:
            test = requests.get(f"{colab_url}/test", timeout=3)
            st.markdown('<div class="connection-status-green">CONNECTED</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="connection-status-red">DISCONNECTED</div>', unsafe_allow_html=True)

if colab_url:
    # Upload and Search Side-by-Side
    st.markdown("---")
    
    upload_col, search_col = st.columns([1, 2])
    
    # UPLOAD SECTION
    with upload_col:
        st.subheader("Upload Transcript")
        uploaded_file = st.file_uploader(
            "Choose a transcript file",
            type=['docx', 'txt', 'pdf'],
            help="Upload a transcript file to process and make searchable"
        )
        
        if st.button("PROCESS TRANSCRIPT", use_container_width=True, disabled=not uploaded_file):
            if uploaded_file:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        
                        response = requests.post(
                            f"{colab_url}/upload-transcript",
                            files=files,
                            headers={"X-API-Key": "tie_smartco1_demo123"}
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"{result['message']}")
                            st.info("Transcript is now searchable!")
                        else:
                            error_data = response.json()
                            st.error(f"Upload failed: {error_data.get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # SEARCH SECTION
    with search_col:
        st.subheader("Search Transcripts")
        
        search_type = st.radio(
            "Search Method",
            ["Keyword Search", "Semantic Search (AI)"],
            help="Keyword: Exact matching | Semantic: AI understands meaning"
        )
        
        # Transcript selector with checkboxes
        try:
            transcripts_response = requests.get(
                f"{colab_url}/list-transcripts",
                headers={"X-API-Key": "tie_smartco1_demo123"}
            )
            
            if transcripts_response.status_code == 200:
                transcripts = transcripts_response.json()
                
                all_transcripts = st.checkbox("All Transcripts", value=True)
                
                selected_transcript_ids = []
                
                if not all_transcripts:
                    st.write("Select specific transcripts:")
                    for transcript in transcripts:
                        if st.checkbox(transcript['filename'], key=f"trans_{transcript['id']}"):
                            selected_transcript_ids.append(transcript['id'])
                
                if all_transcripts:
                    transcript_id = None
                elif len(selected_transcript_ids) == 1:
                    transcript_id = selected_transcript_ids[0]
                else:
                    transcript_id = selected_transcript_ids
            else:
                transcript_id = None
        except:
            transcript_id = None
        
        search_query = st.text_input(
            "Search Query",
            placeholder="Enter your search terms...",
            help="Try: 'drug task force', 'Tammy', 'Oklahoma'"
        )
        
        if st.button("SEARCH", use_container_width=True):
            if search_query:
                with st.spinner("Searching..."):
                    endpoint = "/semantic-search" if search_type == "Semantic Search (AI)" else "/keyword-search"

                    response = requests.post(
                        f"{colab_url}{endpoint}",
                        json={"query": search_query, "transcript_id": transcript_id},
                        headers={"X-API-Key": "tie_smartco1_demo123"}
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        
                        st.markdown(f"### Results: {len(results)} matches found for '{search_query}'")
                        
                        for r in results[:10]:
                            speaker = r.get('speaker', 'Unknown')
                            time_code = r.get('time_code', '00:00:00')
                            source = r.get('source_file', 'Unknown')
                            score = r.get('score', 0)
                            
                            if search_type == "Semantic Search (AI)" and score > 0:
                                header = f"{speaker} [{time_code}] - Relevance: {score:.1f}/10"
                            else:
                                header = f"{speaker} [{time_code}]"
                            
                            with st.expander(header):
                                st.write(f"**Quote:** {r.get('exact_quote', '')}")
                                st.write(f"**Time:** {time_code}")
                                st.write(f"**Speaker:** {speaker}")
                                st.write(f"**Source:** {source}")
                                if score > 0:
                                    st.write(f"**Relevance Score:** {score:.1f}/10")
                        
                        if results:
                            st.markdown("---")
                            st.subheader("Download Results")
                            dcol1, dcol2 = st.columns(2)
                            
                            with dcol1:
                                output = io.StringIO()
                                writer = csv.writer(output)
                                writer.writerow(['T!M Search Results'])
                                writer.writerow(['Query:', search_query])
                                writer.writerow(['Search Type:', search_type])
                                writer.writerow(['Time:', datetime.now().strftime('%Y-%m-%d %H:%M')])
                                writer.writerow([])
                                writer.writerow(['#', 'Speaker', 'Time', 'Quote', 'Source', 'Relevance'])
                                
                                for i, r in enumerate(results, 1):
                                    writer.writerow([
                                        i,
                                        r.get('speaker', ''),
                                        r.get('time_code', ''),
                                        r.get('exact_quote', ''),
                                        r.get('source_file', ''),
                                        f"{r.get('score', 0):.1f}" if r.get('score') else 'N/A'
                                    ])
                                
                                st.download_button(
                                    "Download CSV",
                                    data=output.getvalue(),
                                    file_name=f"T!M_results_{search_query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            with dcol2:
                                report = f"T!M TRANSCRIPT SEARCH REPORT\n"
                                report += f"{'='*50}\n"
                                report += f"REDUCE THE GRIND. REVEAL THE BRILLIANCE.\n"
                                report += f"{'='*50}\n\n"
                                report += f"Search Query: {search_query}\n"
                                report += f"Search Type: {search_type}\n"
                                report += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                                report += f"Total Results: {len(results)}\n\n"
                                report += f"{'='*50}\n"
                                report += f"SEARCH RESULTS\n"
                                report += f"{'='*50}\n"
                                
                                for i, r in enumerate(results, 1):
                                    report += f"\nResult #{i}\n"
                                    report += f"Speaker: {r.get('speaker', 'Unknown')}\n"
                                    report += f"Time: {r.get('time_code', '00:00:00')}\n"
                                    report += f"Source: {r.get('source_file', 'Unknown')}\n"
                                    if r.get('score'):
                                        report += f"Relevance: {r.get('score'):.1f}/10\n"
                                    report += f"\nQuote:\n{r.get('exact_quote', '')}\n"
                                    report += "-"*50 + "\n"
                                
                                st.download_button(
                                    "Download Report",
                                    data=report,
                                    file_name=f"T!M_report_{search_query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                    else:
                        st.error(f"Search failed: {response.status_code}")
            else:
                st.warning("Please enter a search query")
    
    # Quick Actions Section
    st.markdown("---")
    
    # Status indicator
    if transcript_id is None:
        st.info("Selected: All Transcripts (Investigation Insights requires selecting ONE specific transcript)")
    elif isinstance(transcript_id, list):
        st.warning(f"Selected: {len(transcript_id)} transcripts (Investigation Insights requires selecting ONE specific transcript)")
    else:
        try:
            selected_name = next((t['filename'] for t in transcripts if t['id'] == transcript_id), "Unknown")
            st.success(f"Selected: {selected_name} - Ready for Investigation Insights")
        except:
            st.success(f"Selected: 1 transcript - Ready for Investigation Insights")
    
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("EXTRACT ENTITIES", use_container_width=True):
            with st.spinner("Extracting entities..."):
                response = requests.post(
                    f"{colab_url}/entity-extraction",
                    json={},
                    headers={"X-API-Key": "tie_smartco1_demo123"}
                )
                
                if response.status_code == 200:
                    entities = response.json()
                    st.info("Entities extracted successfully")
                    
                    ecol1, ecol2, ecol3, ecol4 = st.columns(4)
                    
                    with ecol1:
                        st.markdown("**People**")
                        all_people = []
                        for person in entities.get('PERSON_OF_INTEREST', []):
                            all_people.append(f"• {person['name']}")
                        for suspect in entities.get('SUSPECTS', []):
                            all_people.append(f"• {suspect['name']} (Suspect)")
                        for victim in entities.get('VICTIMS', []):
                            all_people.append(f"• {victim['name']} (Victim)")
                        for person in all_people[:10]:
                            st.write(person)
                    
                    with ecol2:
                        st.markdown("**Locations**")
                        for location in entities.get('LOCATIONS', [])[:10]:
                            st.write(f"• {location['name']}")
                    
                    with ecol3:
                        st.markdown("**Timeline**")
                        for time in entities.get('TIMELINE', [])[:10]:
                            st.write(f"• {time['name']}")
                    
                    with ecol4:
                        if entities.get('WEAPONS'):
                            st.markdown("**Weapons Mentioned**")
                            for weapon in entities['WEAPONS']:
                                st.write(f"• {weapon['name']}")
                else:
                    st.error("Failed to load entities")
    
    with col2:
        investigation_enabled = isinstance(transcript_id, str) and transcript_id is not None
        
        if st.button("INVESTIGATION INSIGHTS", use_container_width=True, disabled=not investigation_enabled):
            with st.spinner("AI Detective analyzing case..."):
                response = requests.post(
                    f"{colab_url}/api/ai-investigation",
                    json={
                        "transcript_id": transcript_id,
                        "focus_area": None,
                        "analysis_depth": "standard"
                    },
                    headers={"X-API-Key": "tie_smartco1_demo123"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Investigation complete")
                    
                    with st.expander("AI DETECTIVE ANALYSIS", expanded=True):
                        st.markdown(result['analysis'])
                        
                        st.markdown("---")
                        st.markdown("**Analysis Statistics:**")
                        meta = result.get('metadata', {})
                        st.write(f"- Statements analyzed: {meta.get('num_statements_analyzed', 'N/A')}")
                        st.write(f"- High-value statements: {meta.get('num_high_value_statements', 'N/A')}")
                        st.write(f"- Entities found: {meta.get('num_entities', 'N/A')}")
                        st.write(f"- Contradictions detected: {meta.get('num_contradictions', 'N/A')}")
                        
                        report = f"T!M INVESTIGATION INSIGHTS REPORT\n{'='*50}\n\n{result['analysis']}\n\n{'='*50}\nAnalysis Statistics:\n"
                        report += f"- Statements analyzed: {meta.get('num_statements_analyzed', 'N/A')}\n"
                        report += f"- High-value statements: {meta.get('num_high_value_statements', 'N/A')}\n"
                        report += f"- Entities found: {meta.get('num_entities', 'N/A')}\n"
                        report += f"- Contradictions detected: {meta.get('num_contradictions', 'N/A')}\n"
                        
                        st.download_button(
                            "Download Investigation Report",
                            data=report,
                            file_name=f"T!M_investigation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                else:
                    error_msg = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else f"Status code: {response.status_code}"
                    st.error(f"Investigation failed: {error_msg}")
        
        if not investigation_enabled:
            st.caption("Select ONE transcript in the Search section above")

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
    T!M - Transcript Intelligence Machine<br>
    REDUCE THE GRIND. REVEAL THE BRILLIANCE.<br>
    © 2025 Ambitious Riff Raff & InSpireWIRE • MVP Demo Version 1.0<br>
    Built for Producers & Editors & ProdCos
    </div>
    """,
    unsafe_allow_html=True)