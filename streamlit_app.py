import streamlit as st
import requests
import base64
import img2pdf
from io import BytesIO
from bs4 import BeautifulSoup

# Updated dictionary with question paper numbers and subject names
question_papers = {
    "2100": "ENVIRONMENTAL STUDIES",
    "2104": "HIGHWAY ENGINEERING",
    "2080": "BASICS ELECTRICAL ENGINEERING",
    "0830": "ELECTRONICS-II",
    "2088": "BASIC OF ELECTRICAL AND ELECTRONICS ENGINEERING",
    "2044": "ENGINEERING DRAWING-I",
    "2228": "CLOUD COMPUTING",
    "2106": "REINFORCED CEMENT CONCRETE (RCC) DRAWING",
    "2112": "INDUSTRIAL ELECTRONICS AND CONTROL",
    "2132": "E-COMMERCE AND DIGITAL MARKETING",
    "2077": "APPLIED MECHANICS",
    "2242": "DEVELOPMENT OF ANDROID APPLICATIONS",
    "2107": "REINFORCED CEMENT CONCRETE STRUCTURES (RCC STRUCTURES)",
    "2344": "UTILIZATION OF ELECTRICAL ENERGY",
    "2208": "OBJECT ORIENTED PROGRAMMING USING JAVA",
    "2241": "DESIGN OF STEEL STRUCTURE",
    "2192": "ELECTRICAL DESIGN, DRAWING AND ESTIMATING-I",
    "2108": "SURVEYING-I",
    "2193": "TRANSMISSION AND DISTRIBUTION OF ELECTRICAL POWER",
    "2214": "ADVANCED JAVA (ELECTIVE)",
    "2238": "DATA SCIENCE AND MACHINE LEARNING (ELECTIVE)",
    "2244": "DOT NET TECHNOLOGIES (ELECTIVE)",
    "2041": "APPLIED MATHEMATICS-I",
    "2301": "RAILWAYS BRIDGES AND TUNNELS",
    "2332": "ELECTRIC TRACTION (ELECTIVE)",
    "2333": "RENEWABLE SOURCES OF ENERGY (ELECTIVE)",
    "2207": "OPERATING SYSTEM",
    "2076": "APPLIED MATHEMATICS-II",
    "2105": "IRRIGATION ENGINEERING",
    "2079": "APPLIED PHYSICS-II",
    "2042": "APPLIED PHYSICS-I",
    "2309": "SOIL MECHANICS AND FOUNDATION ENGINEERING",
    "2050": "FUNDAMENTALS OF COMPUTER AND INFORMATION TECHNOLOGY",
    "2043": "APPLIED CHEMISTRY",
    "2317": "WASTE WATER AND IRRIGATION ENGINEERING DRAWING",
    "2268": "INTERNET OF THINGS",
    "2040": "COMMUNICATION SKILLS-I",
    "2318": "WATER AND WASTE WATER ENGINEERING",
    "2308": "SOFTWARE ENGINEERING",
    "2103": "COMMUNICATION SKILLS-II",
    "2326": "SURVEYING-II",
    "2338": "SWITCH GEAR AND PROTECTION",
    "2231": "COMPUTER PROGRAMMING USING PYTHON",
    "2700": "ENVIRONMENTAL STUDIES AND DISASTER MANAGEMENT",
    "2319": "WEB DEVELOPMENT USING PHP",
    "2101": "HYDRAULICS AND HYDRAULIC MACHINES",
    "2058": "TECHNICAL DRAWING",
    "2045": "CONSTRUCTION MATERIALS",
    "2086": "BASICS OF MECHANICAL AND CIVIL ENGINEERING",
    "2247": "ELECTRICAL DESIGN, DRAWING AND ESTIMATING II",
    "2097": "ENERGY CONSERVATION",
    "2134": "COMPUTER ARCHITECTURE AND HARDWARE MAINTENANCE",
    "2102": "STRUCTURAL MECHANICS",
    "2337": "INDUSTRIAL MANAGEMENT & ENTREPRENEURSHIP DEVELOPMENT",
    "2098": "BUILDING CONSTRUCTION",
    "2176": "ELECTRICAL INSTRUMENTS AND MEASUREMENT",
    "2189": "DIGITAL ELECTRONICS",
    "2327": "EARTHQUAKE ENGINEERING",
    "2292": "PLC, MICROCONTROLLER AND SCADA",
    "2087": "CONCEPT OF PROGRAMMING USING C",
    "2310": "STEEL STRUCTURE DRAWING",
    "2181": "ELECTRICAL MACHINES-I",
    "2188": "DATA STRUCTURE USING C",
    "2177": "CONCRETE TECHNOLOGY",
    "2343": "INSTALLATION MAINTENANCE & REPAIR OF ELECTRICAL EQUIPMENT",
    "2089": "MULTIMEDIA & ANIMATION",
    "2341": "CONSTRUCTION MANAGEMENT ACCOUNTS & ENTREPRENEURSHIP DEVELOPMENT",
    "2131": "DATABASE MANAGEMENT SYSTEM",
    "2219": "ANALYSIS OF STRUCTURES (ELECTIVE)",
    "2293": "PLUMBING SERVICES (ELECTIVE)",
    "2342": "REPAIR AND MAINTENANCE OF BUILDINGS (ELECTIVE)",
    "2203": "POWER PLANT ENGINEERING",
    "2109": "APPLIED MATHEMATICS-III",
    "2111": "ELECTRICAL AND ELECTRONICS ENGINEERING MATERIALS",
    "2130": "INTERNET AND WEB TECHNOLOGY",
    "2078": "BASICS OF MECHANICAL AND ELECTRICAL ENGG.",
    "2330": "ELECTRICAL MACHINES-II",
    "2300": "QUANTITY SURVEYING AND VALUATION",
    "2110": "DIGITAL ELECTRONICS",
    "2099": "BUILDING DRAWINGS",
    "2081": "ANALOG ELECTRONICS",
}

def get_question_paper_images(copy_no):
    """Fetches and returns all image URLs from the given question paper page."""
    encoded_qp = base64.b64encode(copy_no.encode()).decode()
    url = f"https://bteexam.com/Examiner/Print_Question_Paper?QPNO={encoded_qp}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")

        img_urls = []
        for img_tag in img_tags:
            img_url = img_tag["src"]
            if not img_url.startswith("http"):
                img_url = f"https://bteexam.com{img_url}"
            img_urls.append(img_url)

        return img_urls

    except Exception:
        return None

def create_pdf_from_images(img_urls):
    """Download images and generate a PDF."""
    pdf_bytes = BytesIO()
    img_data_list = []

    for img_url in img_urls:
        response = requests.get(img_url)
        if response.status_code == 200:
            img_data_list.append(response.content)

    pdf_bytes.write(img2pdf.convert(img_data_list))
    pdf_bytes.seek(0)

    return pdf_bytes

# Streamlit UI
st.title("BTEUP Question Paper Viewer")
url1 = "https://bteup.ac.in/PDFFILES/NEWS_638701455709583359.pdf"
url2 = "https://bteup.ac.in/PDFFILES/NEWS_638701455343935289.pdf"
st.write("To know the QP Code of Back/Special Back Subject [Click Here ](%s)" % url1)
st.write("To know the QP Code of Regular Subject [Click Here ](%s) "% url2)
copy_no = st.text_input("Enter Question Paper Number")

if st.button("View Question Paper"):
    if copy_no.strip():
        img_urls = get_question_paper_images(copy_no)
        if img_urls:
            for img_url in img_urls:
                st.image(img_url, use_container_width=True)

            pdf_file = create_pdf_from_images(img_urls)
            st.download_button(
                label="📄 Save as PDF",
                data=pdf_file,
                file_name=f"{copy_no}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No images found. The Question Paper number might be incorrect.")
    else:
        st.warning("Please enter a valid Question Paper Number.")
