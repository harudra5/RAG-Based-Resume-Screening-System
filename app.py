
import re
from pathlib import Path

import streamlit as st
import pandas as pd
import altair as alt
from pypdf import PdfReader


# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="HireAI | Recruitment Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------- CUSTOM UI DESIGN --------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FB;
    }

    [data-testid="stSidebar"] {
        background-color: #12243A;
    }

    [data-testid="stSidebar"] * {
        color: #F1F5F9;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #172B4D;
    }

    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B;
    }

    [data-testid="stMetricValue"] {
        color: #153B65;
    }

    div.stButton > button[kind="primary"] {
        background-color: #0D9488;
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #0F766E;
        color: white;
    }

    div[data-testid="stExpander"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("# HireAI")
    st.caption("RECRUITMENT INTELLIGENCE")
    st.divider()

    st.markdown("### Navigation")
    st.markdown("📊  Overview")
    st.markdown("🏆  Candidate Ranking")
    st.markdown("👤  Candidate Profiles")
    st.markdown("📈  Analytics")
    st.markdown("🤖  RAG Assistant")

    st.divider()
    st.caption("AI-powered recruitment")


# -------------------- PAGE HEADER --------------------

st.title("Recruitment Intelligence")
st.caption(
    "Screen resumes, compare candidate skills, "
    "and identify potential matches for your role."
)
st.divider()


# -------------------- RESUME FOLDER --------------------

LOCAL_RESUME_FOLDER = Path(
    r"C:\Users\user\Downloads\20605119-Resumes\Resumes"
)

PROJECT_RESUME_FOLDER = Path(__file__).parent / "Resumes"

if LOCAL_RESUME_FOLDER.exists():
    RESUME_FOLDER = LOCAL_RESUME_FOLDER
else:
    RESUME_FOLDER = PROJECT_RESUME_FOLDER


# -------------------- SKILL DICTIONARY --------------------

SKILL_ALIASES = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Machine Learning": ["machine learning", "machine-learning"],
    "Deep Learning": ["deep learning", "deep-learning"],
    "NLP": ["nlp", "natural language processing"],
    "Generative AI": ["generative ai", "genai", "gen ai"],
    "LLMs": [
        "llm", "llms", "large language model",
        "large language models"
    ],
    "LangChain": ["langchain"],
    "RAG": [
        "rag", "retrieval augmented generation",
        "retrieval-augmented generation"
    ],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Computer Vision": ["computer vision"],
    "Statistics": ["statistics", "statistical analysis"],
    "Data Structures": ["data structures"],
    "Prompt Engineering": ["prompt engineering"],
    "Agentic AI": ["agentic ai", "ai agents", "llm agents"],
    "LangGraph": ["langgraph"],
    "Vector Databases": [
        "vector database", "vector databases",
        "vector db", "vector store"
    ],
    "OpenAI APIs": ["openai api", "openai apis"],
    "Streamlit": ["streamlit"],
    "Git": ["git"],
    "GitHub": ["github"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Docker": ["docker"],
    "MLflow": ["mlflow"],
    "Hugging Face": ["hugging face", "huggingface"],
    "Transformers": ["transformers", "transformer architecture"],
    "Embeddings": ["embeddings", "embedding"],
    "ChromaDB": ["chromadb", "chroma db"],
    "REST APIs": ["rest api", "rest apis"],
    "Keras": ["keras"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Optuna": ["optuna"],
    "Random Forest": ["random forest", "randomforest"],
}


# -------------------- PDF EXTRACTION --------------------

def extract_pdf_text(pdf_path):
    try:
        reader = PdfReader(str(pdf_path))
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )
    except Exception:
        return ""


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[\u2010-\u2015]", "-", text)
    return text


def contains_term(text, term):
    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(term.lower())
        + r"(?![a-z0-9])"
    )
    return re.search(pattern, text) is not None


def find_skills(text, skills):
    normalized = normalize_text(text)
    found = []

    for skill in skills:
        aliases = SKILL_ALIASES.get(skill, [skill.lower()])

        if any(contains_term(normalized, alias) for alias in aliases):
            found.append(skill)

    return found


# -------------------- CONTACT EXTRACTION --------------------

def extract_email(text):
    cleaned = text

    cleaned = re.sub(
        r"\s*(?:\[at\]|\(at\)|\bat\b)\s*",
        "@",
        cleaned,
        flags=re.I
    )
    cleaned = re.sub(
        r"\s*(?:\[dot\]|\(dot\))\s*",
        ".",
        cleaned,
        flags=re.I
    )

    cleaned = re.sub(r"\s*@\s*", "@", cleaned)
    cleaned = re.sub(r"\s*\.\s*", ".", cleaned)

    matches = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        cleaned
    )

    if matches:
        email = matches[0].strip(".,;:")

        if "*" in email:
            return "Masked in PDF"

        return email

    if re.search(
        r"[A-Za-z0-9._%+-]\*{2,}[A-Za-z0-9._%+-]*@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        cleaned
    ):
        return "Masked in PDF"

    return "Not found"


def extract_phone(text):
    label_pattern = re.compile(
        r"(?:mobile|phone|contact|telephone|tel|ph)"
        r"\s*(?:number|no\.?)?\s*[:\-]?\s*"
        r"(\+?[\d][\d\s().\-*]{7,}\d|\+?[\d][\d\s().\-*]{7,}\*+)",
        re.I
    )

    candidates = label_pattern.findall(text)

    if not candidates:
        indian_pattern = re.compile(
            r"(?<!\d)(?:(?:\+?91|0)[\s().\-]*)?"
            r"[6-9](?:[\s().\-]*\d){9}(?!\d)"
        )
        candidates = indian_pattern.findall(text)

    for candidate in candidates:
        if "*" in candidate:
            continue

        digits = re.sub(r"\D", "", candidate)

        if len(digits) == 10 and digits[0] in "6789":
            return candidate.strip()

        if len(digits) == 12 and digits.startswith("91"):
            if digits[2] in "6789":
                return candidate.strip()

        if len(digits) == 11 and digits.startswith("0"):
            if digits[1] in "6789":
                return candidate.strip()

    if re.search(
        r"(?:\+?91[\s\-]*)?[6-9][\d\s().\-]*\*{2,}",
        text
    ):
        return "Masked in PDF"

    return "Not found"


# -------------------- CANDIDATE NAME --------------------

def extract_candidate_name(text, pdf_path):
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:
        if (
            len(line) <= 55
            and not re.search(
                r"@|https?://|www\.|resume|curriculum vitae",
                line,
                re.I
            )
            and not re.search(r"\d{3,}", line)
        ):
            words = line.split()

            if 2 <= len(words) <= 5:
                return line

    return pdf_path.stem


# -------------------- PROJECT EXTRACTION --------------------

def extract_projects(text):
    known_titles = [
        (
            "Vehicle Fuel Economy Prediction, Highway MPG Prediction "
            "using Machine Learning"
        ),
        (
            "Diabetes Prediction Using ANN, Deep Learning-Based "
            "Diabetes Risk Classification"
        ),
        (
            "Financial Services AI Assistant Chatbot, Domain-Specific "
            "Conversational AI using LangChain & OpenAI"
        ),
    ]

    def clean_line(line):
        line = re.sub(r"\s+", " ", line).strip()
        line = re.sub(r"^[•▪●◦*]\s*", "", line)
        line = re.sub(r"^\d+[.)]\s*", "", line)
        return line.strip()

    def title_key(line):
        line = clean_line(line).lower()
        line = re.sub(r"[\u2010-\u2015]", "-", line)
        line = re.sub(r"[^a-z0-9]+", " ", line)
        return " ".join(line.split())

    known_keys = {
        title_key(title): title
        for title in known_titles
    }

    projects_heading = re.compile(
        r"^(?:(?:academic|personal|key|selected)\s+)?"
        r"projects?(?:\s+experience)?\s*[:\-]?$",
        re.I
    )

    section_heading = re.compile(
        r"^(education|experience|work experience|professional "
        r"experience|technical skills|skills|certifications|"
        r"achievements|declaration|interests|languages|publications|"
        r"internships|professional summary|summary|objective|"
        r"personal details|references)\s*[:\-]?$",
        re.I
    )

    description_start = re.compile(
        r"^(built|developed|designed|implemented|created|performed|"
        r"evaluated|applied|used|utilized|leveraged|trained|achieved|"
        r"conducted|deployed|integrated|analyzed|analysed|predicted|"
        r"proposed|worked|responsible|the project|this project|"
        r"tech stack|technologies|tools used|results|outcome|"
        r"accuracy|dataset|key features|features)\b",
        re.I
    )

    title_keywords = re.compile(
        r"\b(prediction|classification|detection|analysis|chatbot|"
        r"assistant|recommendation|forecasting|recognition|"
        r"management|system|application|model|project)\b",
        re.I
    )

    raw_lines = []

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        line = re.sub(r"\s+", " ", raw_line).strip()

        is_bullet = bool(
            re.match(r"^[•▪●◦*]\s*", line)
            or re.match(r"^\d+[.)]\s+", line)
        )

        line = clean_line(line)

        if line:
            raw_lines.append((line, is_bullet))

    project_lines = []
    in_projects = False

    for line, is_bullet in raw_lines:
        if projects_heading.match(line):
            in_projects = True
            continue

        if section_heading.match(line):
            if in_projects:
                break
            continue

        if in_projects:
            project_lines.append((line, is_bullet))

    if not project_lines:
        return []

    def get_known_title(line):
        key = title_key(line)

        if key in known_keys:
            return known_keys[key], ""

        for known_key, display_title in known_keys.items():
            if key.startswith(known_key + " "):
                words = clean_line(line).split()
                title_word_count = len(display_title.split())
                remainder = " ".join(
                    words[title_word_count:]
                ).strip(" :-|")

                return display_title, remainder

        return None, ""

    def is_generic_title(line, is_bullet):
        if is_bullet or len(line) > 150:
            return False

        if line and line[0].islower():
            return False

        if description_start.match(line):
            return False

        if re.match(
            r"^(tech stack|technologies|tools used)\s*:",
            line,
            re.I
        ):
            return False

        if re.match(r"^project\s*\d+\b", line, re.I):
            return True

        return bool(
            title_keywords.search(line)
            and len(line.split()) <= 18
            and not re.search(r"[.!?]\s*$", line)
        )

    grouped = []
    current = None

    for line, is_bullet in project_lines:
        known_title, remainder = get_known_title(line)

        if known_title:
            if current:
                grouped.append(current)

            current = {
                "title": known_title,
                "lines": []
            }

            if remainder:
                current["lines"].append(remainder)

            continue

        if (
            current
            and is_generic_title(line, is_bullet)
            and not any(
                title_key(line).startswith(title_key(t))
                for t in known_titles
            )
        ):
            if current["title"] not in known_titles:
                grouped.append(current)
                current = {
                    "title": line.strip(" :-|"),
                    "lines": []
                }
                continue

            current["lines"].append(line)
            continue

        if current:
            current["lines"].append(line)
        elif is_generic_title(line, is_bullet):
            current = {
                "title": line.strip(" :-|"),
                "lines": []
            }

    if current:
        grouped.append(current)

    metric_patterns = [
        r"~?\d+(?:\.\d+)?\s*%?\s*(?:test\s+)?accuracy\b",
        r"\b\d+(?:\.\d+)?\s*ROC[- ]?AUC\b",
        r"\b\d+(?:\.\d+)?\s*(?:R²|R2|R-squared)\b",
        r"\b\d+(?:\.\d+)?\s*(?:MPG\s*)?RMSE\b",
        r"\b\d+(?:\.\d+)?\s*MAE\b",
        r"\b\d+(?:\.\d+)?\s*precision\b",
        r"\b\d+(?:\.\d+)?\s*recall\b",
        r"\b\d+(?:\.\d+)?\s*F1(?:-score)?\b",
    ]

    project_details = []

    for group in grouped:
        title = group["title"]
        description = " ".join(group["lines"]).strip()
        full_text = " ".join([title, description]).strip()

        tech_match = re.search(
            r"(?:tech(?:nology)?\s*stack|technologies|tools\s*used)"
            r"\s*:\s*(.*?)(?=\s+(?:results?|outcome)\s*:|$)",
            full_text,
            re.I
        )

        explicit_technologies = []

        if tech_match:
            explicit_technologies = [
                item.strip(" .;|")
                for item in re.split(
                    r"[,;|]",
                    tech_match.group(1)
                )
                if item.strip(" .;|")
            ]

        metrics = []

        for pattern in metric_patterns:
            for match in re.finditer(pattern, full_text, re.I):
                value = match.group(0).strip()

                if value not in metrics:
                    metrics.append(value)

        technologies = find_skills(
            full_text,
            list(SKILL_ALIASES.keys())
        )

        project_details.append({
            "Project": title,
            "Description": description or full_text,
            "Technologies": technologies,
            "Tech Stack": explicit_technologies,
            "Results": ", ".join(metrics)
        })

    return project_details[:8]


# -------------------- JD SKILL MATCHING --------------------

def score_candidate(resume_text, jd_text):
    jd_skills = find_skills(
        jd_text,
        list(SKILL_ALIASES.keys())
    )

    resume_skills = find_skills(
        resume_text,
        list(SKILL_ALIASES.keys())
    )

    matched = [
        skill for skill in jd_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in jd_skills
        if skill not in resume_skills
    ]

    score = (
        round(len(matched) / len(jd_skills) * 100, 2)
        if jd_skills else 0.0
    )

    return jd_skills, matched, missing, score, resume_skills


# -------------------- JOB DESCRIPTION --------------------

st.subheader("Job Description")

jd_input = st.text_area(
    "Paste the job description",
    placeholder="Paste the complete AI/ML Engineer job description here...",
    height=180
)

st.caption(
    "Scores use a built-in keyword dictionary. "
    "Skills outside that dictionary may not be counted."
)


# -------------------- RESUME SCANNING --------------------

st.subheader("Resume Screening")

if not RESUME_FOLDER.exists():
    st.error(
        f"Resume folder not found:\n{RESUME_FOLDER}\n\n"
        "Please update RESUME_FOLDER to your actual PDF folder."
    )
    resume_files = []
else:
    resume_files = sorted(RESUME_FOLDER.glob("*.pdf"))
    st.write(f"PDF resumes available: **{len(resume_files)}**")


if st.button("🔍 Scan All Resumes", type="primary"):
    if not jd_input.strip():
        st.warning("Please enter a Job Description first.")

    elif not resume_files:
        st.warning("No PDF resumes found in the configured folder.")

    else:
        results = []
        progress = st.progress(0)
        status = st.empty()

        for index, pdf_path in enumerate(resume_files, start=1):
            status.write(
                f"Scanning resume {index} of {len(resume_files)}: "
                f"{pdf_path.name}"
            )

            resume_text = extract_pdf_text(pdf_path)

            if resume_text.strip():
                jd_skills, matched, missing, score, resume_skills = (
                    score_candidate(resume_text, jd_input)
                )

                projects = extract_projects(resume_text)

                results.append({
                    "Candidate": extract_candidate_name(
                        resume_text, pdf_path
                    ),
                    "Email": extract_email(resume_text),
                    "Phone": extract_phone(resume_text),
                    "Match Score (%)": score,
                    "Matched Skills": ", ".join(matched) or "None found",
                    "Missing Skills": ", ".join(missing) or "None found",
                    "Projects": projects,
                    "Resume File": pdf_path.name,
                    "Resume Skills": ", ".join(resume_skills),
                    "Resume Text": resume_text
                })

            progress.progress(index / len(resume_files))

        status.empty()
        progress.empty()

        if results:
            results.sort(
                key=lambda item: item["Match Score (%)"],
                reverse=True
            )

            st.session_state["screening_results"] = results
            st.session_state["screening_jd"] = jd_input

            st.success(
                f"Scanned {len(resume_files)} PDFs. "
                f"Extracted readable text from {len(results)} resumes."
            )
        else:
            st.warning(
                "Could not extract readable text from these PDFs. "
                "Image-only resumes may require OCR."
            )


# -------------------- DASHBOARD & RANKED RESULTS --------------------

if "screening_results" in st.session_state:
    results = st.session_state["screening_results"]

    st.divider()
    st.header("Hiring Overview")
    st.caption("Candidate screening results for the submitted job description.")

    threshold = st.slider(
        "Minimum match score (%)",
        min_value=0,
        max_value=100,
        value=50
    )

    filtered_results = [
        result for result in results
        if result["Match Score (%)"] >= threshold
    ]

    # KPI cards
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Resumes Screened", len(results))
    k2.metric(
        "Qualified Candidates",
        len(filtered_results),
        help="Candidates meeting the selected minimum keyword-match score."
    )
    k3.metric(
        "Top Match",
        f"{results[0]['Match Score (%)']:.2f}%"
    )
    avg_score = sum(
        r["Match Score (%)"] for r in results
    ) / len(results)
    k4.metric("Average Match Score", f"{avg_score:.1f}%")

    st.divider()

    # Chart and candidate summary
    chart_col, summary_col = st.columns([1.6, 1])

    with chart_col:
        st.subheader("Top Candidate Matches")

        top_candidates = results[:10]
        chart_data = pd.DataFrame([
            {
                "Candidate": r["Candidate"],
                "Match Score (%)": r["Match Score (%)"]
            }
            for r in top_candidates
        ])

        chart = alt.Chart(chart_data).mark_bar(
            cornerRadiusEnd=5,
            color="#0D9488"
        ).encode(
            x=alt.X(
                "Match Score (%):Q",
                title="Keyword Match Score (%)",
                scale=alt.Scale(domain=[0, 100])
            ),
            y=alt.Y(
                "Candidate:N",
                sort="-x",
                title=None
            ),
            tooltip=["Candidate", "Match Score (%)"]
        ).properties(height=320)

        st.altair_chart(chart, use_container_width=True)

    with summary_col:
        st.subheader("Skill Coverage")

        jd_skills = find_skills(
            st.session_state.get("screening_jd", ""),
            list(SKILL_ALIASES.keys())
        )

        matched_counts = {
            skill: sum(
                skill in r["Matched Skills"].split(", ")
                for r in results
            )
            for skill in jd_skills
        }

        if matched_counts:
            skill_data = pd.DataFrame([
                {"Skill": skill, "Candidates": count}
                for skill, count in matched_counts.items()
            ]).sort_values("Candidates", ascending=False).head(10)

            skill_chart = alt.Chart(skill_data).mark_bar(
                cornerRadiusEnd=5,
                color="#3977B8"
            ).encode(
                x=alt.X("Candidates:Q", title="Candidates"),
                y=alt.Y("Skill:N", sort="-x", title=None),
                tooltip=["Skill", "Candidates"]
            ).properties(height=320)

            st.altair_chart(skill_chart, use_container_width=True)
        else:
            st.info("No recognized skills found in the job description.")

    st.divider()

    # Candidate ranking table
    st.header("Candidate Ranking")
    st.caption("Ranked by keyword overlap with the job description.")

    if filtered_results:
        table_data = [
            {
                "Rank": rank,
                "Candidate": candidate["Candidate"],
                "Match Score (%)": candidate["Match Score (%)"],
                "Matched Skills": candidate["Matched Skills"],
                "Missing Skills": candidate["Missing Skills"],
            }
            for rank, candidate in enumerate(filtered_results, start=1)
        ]

        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Match Score (%)": st.column_config.ProgressColumn(
                    "Match Score",
                    min_value=0,
                    max_value=100,
                    format="%.2f%%"
                )
            }
        )

        csv_data = pd.DataFrame([
            {
                key: value
                for key, value in candidate.items()
                if key not in ["Resume Text", "Projects"]
            }
            for candidate in filtered_results
        ]).to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Candidate Results (CSV)",
            data=csv_data,
            file_name="ranked_candidates.csv",
            mime="text/csv"
        )

        st.divider()

        # Candidate profile cards
        st.header("Candidate Profiles")

        for rank, candidate in enumerate(filtered_results, start=1):
            with st.container(border=True):
                header_col, score_col = st.columns([4, 1])

                with header_col:
                    st.subheader(
                        f"{rank}. {candidate['Candidate']}"
                    )
                    st.caption(candidate["Resume File"])

                with score_col:
                    st.metric(
                        "Match Score",
                        f"{candidate['Match Score (%)']:.2f}%"
                    )

                contact1, contact2 = st.columns(2)

                contact1.write("**Email**")
                contact1.write(candidate["Email"])

                contact2.write("**Phone**")
                contact2.write(candidate["Phone"])

                matched_col, missing_col = st.columns(2)

                with matched_col:
                    st.markdown("**Matched JD Skills**")
                    if candidate["Matched Skills"] != "None found":
                        st.success(candidate["Matched Skills"])
                    else:
                        st.write("None found")

                with missing_col:
                    st.markdown("**Missing JD Skills**")
                    if candidate["Missing Skills"] != "None found":
                        st.warning(candidate["Missing Skills"])
                    else:
                        st.write("None found")

                with st.expander("View projects and technologies"):
                    if candidate["Projects"]:
                        for project_index, project in enumerate(
                            candidate["Projects"], start=1
                        ):
                            st.markdown(
                                f"**Project {project_index}: "
                                f"{project['Project']}**"
                            )
                            st.write(project["Description"])

                            if project["Technologies"]:
                                st.markdown("**Detected technologies**")
                                st.write(
                                    ", ".join(project["Technologies"])
                                )

                            if project["Tech Stack"]:
                                st.markdown("**Extracted tech stack**")
                                st.write(
                                    ", ".join(project["Tech Stack"])
                                )

                            if project["Results"]:
                                st.markdown("**Results / metrics**")
                                st.write(project["Results"])

                            st.divider()
                    else:
                        st.info(
                            "A project section could not be identified. "
                            "Check the original resume."
                        )

                with st.expander("View extracted resume text"):
                    st.text(candidate["Resume Text"])

    else:
        st.info("No candidates meet the selected score threshold.")

    st.caption(
        "Scores represent keyword overlap, not verified skill proficiency "
        "or a commercial ATS score. Review original resumes before hiring."
    )
