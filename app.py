import streamlit as st
from docxtpl import DocxTemplate
import os
import tempfile
import subprocess
import re
from datetime import datetime, date
import logging
#from num2words import num2words # Library to convert numbers to words (e.g., salary)

# --- Configuration & Setup ---

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMPLATE = "contract_template.txt"
DATE_FORMAT_STR = "%d/%m/%Y"  # Standard Python format string (e.g., 01/01/2024)

# Define required fields for central validation
# (Only for fields not natively validated by st.date_input/st.number_input)
REQUIRED_FIELDS = [
    "inquilino", "inquilino_id_nr", "morada_inquilino",
    "valor_renda", "endereco_imovel", "senhorio", "senhorio_nif",
    "bank_name", "iban",
    "contract_date_local"
]

# --- Utility Functions ---

def check_template_exists():
    """Check if template file exists"""
    return os.path.exists(TEMPLATE)

def convert_to_pdf(docx_path, output_dir):
    """Convert DOCX to PDF using LibreOffice with error handling"""
    # NOTE: This function still relies on LibreOffice being installed on the server.
    try:
        # Use a longer timeout for robustness
        result = subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", output_dir, docx_path
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            pdf_path = os.path.join(output_dir, os.path.basename(docx_path).replace(".docx", ".pdf"))
            return pdf_path if os.path.exists(pdf_path) else None
        else:
            logger.error(f"Conversão LibreOffice falhou: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        logger.error("PDF conversion timeout")
        return None
    except Exception as e:
        logger.error(f"PDF conversion error: {str(e)}")
        return None


# --- Validation Functions (Simplified) ---

def validate_iban(iban_str):
    """Basic IBAN validation (Angolan IBANs typically 25 characters, starting with AO)"""
    if not iban_str:
        return False
    cleaned_iban = iban_str.replace(" ", "").upper()
    # Check minimum length and starting country code
    return len(cleaned_iban) >= 15 and cleaned_iban.isalnum() and cleaned_iban.startswith('AO')

# --- Streamlit Page Configuration ---

st.set_page_config(
    page_title="Contrato de Arrendamento Urbano", 
    page_icon="📄", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling (retained from original, slightly cleaned up)
st.markdown("""
    <style>
    .main-header {
        font-size: 1.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1.0rem;
    }
    .section-header {
        background-color: #e6f3ff; /* Lighter blue for better contrast */
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 0.5px solid #1f77b4;
    }
    .required-field::after {
        content: " *";
        color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📄 Contrato de Arrendamento Urbano</h1>', unsafe_allow_html=True)
st.markdown("Preencha os detalhes abaixo para o contracto de arrendamento (**DOCX** or **PDF**).")

# Template check and stop
# If the configured template is a .txt but a .docx sibling exists, prefer the .docx
if TEMPLATE.lower().endswith('.txt'):
    alt = TEMPLATE[:-4] + '.docx'
    if os.path.exists(alt):
        TEMPLATE = alt

# Final existence check
if not check_template_exists():
    st.error(f"❌ Template file **'{TEMPLATE}'** not found. Please ensure the template file is in the correct location (expected a .docx for docxtpl).")
    st.stop()
else:
    st.sidebar.success(f"Template '{TEMPLATE}' loaded successfully.")

# --- Input Form ---

with st.form("contract_form", clear_on_submit=False):
    # --- Employer Details ---
    st.markdown('<div class="section-header">', unsafe_allow_html=True)
    st.subheader("🏢 Detalhes do Senhorio")
    st.markdown('</div>', unsafe_allow_html=True)
    
    senhorio = st.text_input("Senhorio *", placeholder="Nome completo")
    colA, colB = st.columns(2)
    with colA:
        senhorio_nif = st.text_input("Senhorio NIF *", placeholder="ex. 1234567LA890", max_chars=20)
    with colB:
        representative_name = st.text_input("Nome do Representante", placeholder="ex. João Silva")
        
    employer_address = st.text_input("Morada *", placeholder="e.g Rei Katyavala, n.15 Andar A Bairro do Maculusso, Município da Ingombota")


    # --- Employee Details ---
    st.markdown('<div class="section-header required-field">', unsafe_allow_html=True)
    st.subheader("👤 Detalhes do Arrendatario")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Required fields with no default value
    inquilino = st.text_input("Inquilino *", placeholder="Nome completo do inquilino")
    #morada_inquilino = st.text_input("Morada do Inquilino *", placeholder="Morada actual do inquilino")

    # ID details using st.date_input for better UX
    col1, col2, col3 = st.columns(3)
    with col1:
        # Tipo de documento dropdown
        inquilino_doc = st.selectbox(
            "Tipo de documento",
            options=["Passaporte", "Bilhete de Identidade"],
            index=1,
            help="Selecione o tipo de documento do inquilino"
        )
    
    with col2:
        inquilino_id_nr = st.text_input("Numero do documento *", placeholder="e.g., 123456789LA123")
        
    with col3:
        # Use st.date_input for Issue Date
        inquilino_id_nr_issue_date_dt = st.date_input(
            "Data de Emissão *",
            value=date(2020, 12, 1), # Default value as a date object
            format="DD/MM/YYYY",
            help="Data em que foi emitido o documento"
        )
        # Use st.date_input for Expiry Date
        inquilino_id_nr_expiry_dt = st.date_input(
            "Data de Validade *",
            value=date(2030, 12, 1), # Default value as a date object
            format="DD/MM/YYYY",
            help=" Data de expiracão do documento"
        )

    # Additional tenant contact fields and property info
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        inquilino_nif = st.text_input("NIF do Inquilino *", placeholder="e.g. 123456789")
        inquilino_contact = st.text_input("Contacto do arrendatario", placeholder="e.g. +244 923 000 000")
    with col_t2:
        inquilino_email = st.text_input("Email do arrendatario", placeholder="e.g. inquilino@example.com")

    endereco_imovel = st.text_input("Endereço do Imóvel *", placeholder="Endereço completo do imóvel a arrendar")

    # --- Contract Details ---
    st.markdown('<div class="section-header required-field">', unsafe_allow_html=True)
    st.subheader("📝 Detalhes do Contracto")
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    # Contract Start Date (using st.date_input)
    col4, col5 = st.columns(2)
    with col4:
        # Input for the date itself
        start_date_dt = st.date_input("Contract Start Date *", value=datetime.now().date(), format="DD/MM/YYYY")
    with col5:
        # Input for the full written-out version (since we don't have a reliable locale-specific converter)
        start_date_written = st.text_input(
            "Data de Inicio (Escrito) *", 
            placeholder="e.g. 25 de Outubro de 2025"
        )
    # Contract End Date (date + written)
    col_end_1, col_end_2 = st.columns(2)
    with col_end_1:
        end_date_dt = st.date_input("Data de Término do Contrato", value=(datetime.now().date()), format="DD/MM/YYYY")
    with col_end_2:
        end_date_written = st.text_input("Data de Término (Escrita)", placeholder="e.g. 25 de Outubro de 2026")
    
    # Rent and payment details
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        valor_renda_float = st.number_input("Valor da Renda (AOA)* ", min_value=0.0, value=150000.00, step=1000.0, format="%.2f")
    with col_r2:
        forma_pagamento = st.text_input("Forma de Pagamento", placeholder="e.g. Transferência Bancária", help="Ex: Transferência Bancária, Cheque")

    col_dep, col_cond = st.columns(2)
    with col_dep:
        valor_caucao_float = st.number_input("Valor da Caução (AOA)", min_value=0.0, value=150000.00, step=1000.0, format="%.2f")
    with col_cond:
        taxa_condominio_float = st.number_input("Taxa de Condomínio (AOA)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")

    # Bank details 
    col8, col9 = st.columns(2)
    with col8:
        bank_name = st.text_input("Nome do Banco *", placeholder="e.g. Banco Angolano de Investimento")
    with col9:
        iban = st.text_input("IBAN *", placeholder="e.g. AO06 0005 0000 1234 5678 9019 4", help="IBAN com o prefixo AO")
        
    # Numeric details using st.number_input
    col10, col11, col12 = st.columns(3)
    with col10:
        # Contract signing date (using st.date_input)
        contract_date_dt = st.date_input("Data da Assinatura do Contracto *", value=datetime.now().date(), format="DD/MM/YYYY")

    # Contract location (Manual input for flexible formatting)
    contract_location = st.text_input("Contract Signing Location *", placeholder="Luanda")
    
    # Combined field for the template (combining date and location for the docxtpl field)
    contract_date_local = f"{contract_location}, aos {contract_date_dt.day} de {contract_date_dt.strftime('%B')} de {contract_date_dt.year}".replace(
        contract_date_dt.strftime('%B'), 
        contract_date_dt.strftime('%B').lower().replace('september', 'Setembro').replace('october', 'Outubro') # Simple Portuguese month mapping (needs extension)
    )
    st.info(f"Generated Signing Line: **{contract_date_local}**")

    submitted = st.form_submit_button(
        "🚀 Gerar Contracto", 
        use_container_width=True, 
        type="primary"
    )

# --- Form Submission and Processing ---

if submitted:
    errors = []
    
    # 1. Required field validation (using the centralized list)
    # The variables are already defined, we check if they are truthy (not None, not empty string)
    
    if not inquilino.strip(): errors.append("Nome do Inquilino é obrigatório")
    if not inquilino_id_nr.strip(): errors.append("Número do documento é obrigatório")
    #if not morada_inquilino.strip(): errors.append("Morada do inquilino é obrigatória")
    if not inquilino_nif.strip(): errors.append("NIF do inquilino é obrigatório")
    if not endereco_imovel.strip(): errors.append("Endereço do imóvel é obrigatório")
    if not start_date_written.strip(): errors.append("Start Date (Written) is required")
    if not bank_name.strip(): errors.append("Bank Name is required")
    if not contract_location.strip(): errors.append("Contract Signing Location is required")
    
    # 2. Format validation (for text fields that need specific format)    
    
    if not validate_iban(iban):
        errors.append("Por favor introduza um IBAN válido (começando com AO, e ate  23 digitos)")

    # Validate required numeric monetary fields
    if valor_renda_float <= 0:
        errors.append("Valor da renda deve ser maior que zero")
    if valor_caucao_float < 0:
        errors.append("Valor da caução inválido")

    # 3. Date Consistency/Logic Validation (e.g., expiry after issue)
    if inquilino_id_nr_issue_date_dt >= inquilino_id_nr_expiry_dt:
        errors.append("ID Expiry Date must be after ID Issue Date.")
        
    # --- Display Errors or Process ---
    if errors:
        st.error("❌ Please correct the following errors:")
        for error in errors:
            st.warning(f"• {error}")
    else:
        # Prepare context data
        # Format currency values for template (AOA format)
        valor_renda_formatted = f"AOA {valor_renda_float:,.2f}".replace(",", "_TMP_").replace(".", ",").replace("_TMP_", ".")
        valor_caucao_formatted = f"AOA {valor_caucao_float:,.2f}".replace(",", "_TMP_").replace(".", ",").replace("_TMP_", ".")
        taxa_condominio_formatted = f"AOA {taxa_condominio_float:,.2f}".replace(",", "_TMP_").replace(".", ",").replace("_TMP_", ".")

        # Use snake_case context keys for template placeholders
        context = {
            "senhorio": senhorio.strip(),
            "senhorio_nif": senhorio_nif.strip(),
            "senhorio_address": employer_address.strip(),
            "representative_name": representative_name.strip(),

            "inquilino": inquilino.strip(),
            "inquilino_nif": inquilino_nif.strip() if inquilino_nif else "",
            "inquilino_contact": inquilino_contact.strip() if inquilino_contact else "",
            "inquilino_email": inquilino_email.strip() if inquilino_email else "",
            #"inquilino_address": morada_inquilino.strip(),
            "endereco_imovel": endereco_imovel.strip(),
            "document_type": inquilino_doc.strip(),
            "document_number": inquilino_id_nr.strip(),
            "document_issue_date": inquilino_id_nr_issue_date_dt.strftime(DATE_FORMAT_STR),
            "document_expiry_date": inquilino_id_nr_expiry_dt.strftime(DATE_FORMAT_STR),
         
            "start_date_written": start_date_written.strip(),
            "end_date_written": end_date_written.strip(),

            "bank_name": bank_name.strip(),
            "iban": iban.strip(),

            "contract_date_local": contract_date_local,

            # Rent/payment details (formatted)
            "valor_renda": valor_renda_formatted,
            "forma_pagamento": forma_pagamento.strip(),
            "valor_caucao": valor_caucao_formatted,
            "taxa_condominio": taxa_condominio_formatted,

            # Static boilerplate context fields
            "governing_law": "Lei Geral do Trabalho, Lei n.º 12/23",
            "signature_employer": "___________________",
            "signature_employee": "___________________"
        }

        # Show loading spinner
        with st.spinner("🔄 A Gerar Contracto..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                try:
                    # Generate safe filename
                    safe_inquilino = "".join(c for c in inquilino if c.isalnum() or c in (' ', '-', '_')).strip()
                    base_filename = f"CAU_{safe_inquilino or 'inquilino'}"
                    docx_path = os.path.join(tmpdir, f"{base_filename}.docx")
                    
                    # Generate DOCX
                    try:
                        tpl = DocxTemplate(TEMPLATE)
                    except Exception as e:
                        logger.error(f"Failed to load template '{TEMPLATE}': {e}")
                        st.error(f"❌ Failed to load template '{TEMPLATE}': {e}")
                        raise
                    try:
                        tpl.render(context)
                    except Exception as e:
                        logger.error(f"Failed to render template: {e}")
                        st.error(f"❌ Failed to render template: {e}")
                        raise
                    tpl.save(docx_path)
                    
                    st.success("✅ Contracto gerado com sucesso!")
                    
                    # Download DOCX
                    colA, colB = st.columns(2)
                    with open(docx_path, "rb") as f:
                        docx_data = f.read()
                    
                    with colA:
                        st.download_button(
                            "📥 Download DOCX",
                            data=docx_data,
                            file_name=f"{base_filename}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            key="docx_download"
                        )
                    
                    # PDF conversion with improved error handling
                    pdf_path = convert_to_pdf(docx_path, tmpdir)
                    
                    with colB:
                        if pdf_path and os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                pdf_data = f.read()
                            
                            st.download_button(
                                "📥 Download PDF", 
                                data=pdf_data,
                                file_name=f"{base_filename}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key="pdf_download"
                            )
                        else:
                            st.warning("⚠️ PDF export falhou (LibreOffice error). Ficheiro DOCX disponivel .")
                            st.info("💡 Conversao PDF requer a instalacao de LibreOffice no servidor.")
                            
                except Exception as e:
                    logger.error(f"Critical error generating contract: {str(e)}")
                    st.error(f"❌ A critical error occurred while generating the contract: {str(e)}")
                    st.info("🔧 Pl" \
                    "ease check the template file placeholders and system logs.")
