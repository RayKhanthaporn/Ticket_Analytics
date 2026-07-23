# pip install -r requirements.txt
# python -m streamlit run streamlit_ticket_agent.py                                                                                        

# (PowerShell) restart
# .\.venv\Scripts\Activate.ps1
# streamlit run streamlit_ticket_agent.py

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

try:
    import openai
except ImportError:
    openai = None


DEFAULT_CSV_PATH = Path(__file__).resolve().parent / "drive-download-20260721T233205Z-1-001" / "tickets_holidays_categorised_df.csv"


def load_ticket_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    return df


def dataset_overview(df: pd.DataFrame) -> Dict[str, Any]:
    fields = df.columns.tolist()
    sample = df.head(4).to_dict(orient="records")
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "fields": fields,
        "sample_rows": sample,
    }


def top_values(df: pd.DataFrame, column: str, n: int = 8) -> Dict[str, int]:
    if column not in df.columns:
        return {}
    counts = df[column].value_counts(dropna=False).head(n)
    return {str(key): int(value) for key, value in counts.items()}


def holiday_summary(df: pd.DataFrame) -> Dict[str, Any]:
    if "IsPublicHoliday" not in df.columns:
        return {
            "message": "Holiday flag column IsPublicHoliday not found.",
        }

    holiday_df = df[df["IsPublicHoliday"] == 1]
    return {
        "holiday_ticket_count": int(len(holiday_df)),
        "holiday_share": round(100 * len(holiday_df) / max(len(df), 1), 1),
        "holiday_top_categories": top_values(holiday_df, "RK_Category", n=5),
        "holiday_top_teams": top_values(holiday_df, "RK_OperationalOwner", n=5),
    }


def build_prompt(question: str, fields: List[str], sample_rows: List[Dict[str, Any]]) -> str:
    description = (
        "You are a support operations analyst. Answer using only the provided dataframe fields "
        "and sample rows. Focus on ticket trends, team performance, holiday impact, category mapping issues, "
        "and review queue observations. Do not invent values from outside the dataset."
    )

    sample_str = "\n".join(
        [str(row) for row in sample_rows]
    )

    return (
        f"{description}\n\n"
        f"Available fields: {', '.join(fields)}\n\n"
        f"Example rows:\n{sample_str}\n\n"
        f"Question: {question}\n"
        "Answer clearly and cite the dataset context where possible. "
        "If the question cannot be answered from the data, say so explicitly."
    )


def get_openai_api_key() -> str:
    env_key = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
    if env_key:
        return env_key

    # Try Streamlit secrets safely. Accessing `st.secrets.get()` can raise
    # StreamlitSecretNotFoundError when no secrets file is present, so wrap
    # each lookup in a try/except and fall back to other sources.
    try:
        secrets_obj = st.secrets
    except Exception:
        secrets_obj = None

    if secrets_obj is not None:
        for key in ("OPENAI_API_KEY", "openai_api_key"):
            try:
                secret_value = secrets_obj.get(key)
            except Exception:
                secret_value = None
            if secret_value:
                return str(secret_value)

    session_key = st.session_state.get("openai_api_key")
    if session_key:
        return str(session_key)

    return ""


def query_openai(prompt: str, api_key: Optional[str] = None) -> str:
    if openai is None:
        return "OpenAI package is not installed. Install it with `pip install openai`."

    resolved_api_key = api_key or get_openai_api_key()
    if not resolved_api_key:
        return "OPENAI_API_KEY is not set. Enter it in the sidebar or set it in your environment and restart the app."

    try:
        client = openai.OpenAI(api_key=resolved_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=450,
        )
        message_content = ""
        if response and getattr(response, "choices", None):
            first_choice = response.choices[0]
            if getattr(first_choice, "message", None) is not None:
                message_content = getattr(first_choice.message, "content", "") or ""
        return message_content.strip()
    except Exception as exc:
        return f"OpenAI request failed: {exc}"


def make_quick_prompts() -> List[str]:
    return [
        "Summarise the current ticket volume and whether volume is rising or falling.",
        "Which teams have the highest ticket workloads and which categories are most common?",
        "What impact do public holidays have on ticket volumes and category mix?",
        "Report any category classification issues or tickets needing review.",
        "What are the top 5 ticket categories and subcategories by count?",
    ]


def render_summary_cards(df: pd.DataFrame) -> None:
    cols = st.columns(3)
    cols[0].metric("Total tickets", f"{len(df):,}")
    cols[1].metric("Categories", str(df["RK_Category"].nunique() if "RK_Category" in df.columns else "N/A"))
    cols[2].metric("Teams", str(df["RK_OperationalOwner"].nunique() if "RK_OperationalOwner" in df.columns else "N/A"))


def main() -> None:
    st.set_page_config(page_title="Ticket Operations Q&A", layout="wide")
    st.title("Ticket Operations Q&A")
    st.write(
        "A manager-focused ticket analytics assistant for the TechSolve dataset. "
        "Ask questions about ticket trends, holiday impact, team workload, and classification review."
    )

    data_path = os.getenv("TICKET_DATA_PATH")
    if data_path:
        data_path = Path(data_path)
    else:
        data_path = DEFAULT_CSV_PATH

    if not data_path.exists():
        st.error(
            f"Dataset not found at {data_path}.\n"
            "Set TICKET_DATA_PATH or place the CSV next to this app."
        )
        return

    with st.spinner("Loading dataset..."):
        df = load_ticket_data(str(data_path))

    overview = dataset_overview(df)
    st.sidebar.header("Dataset quick facts")
    st.sidebar.write(f"Rows: {overview['rows']:,}")
    st.sidebar.write(f"Columns: {overview['cols']}")
    st.sidebar.write("Holiday tickets:")
    st.sidebar.json(holiday_summary(df))
    st.sidebar.markdown("---")
    st.sidebar.header("Quick prompts")
    for prompt in make_quick_prompts():
        if st.sidebar.button(prompt, key=prompt):
            st.session_state["question"] = prompt

    st.sidebar.markdown("---")
    st.sidebar.subheader("OpenAI access")
    api_key = get_openai_api_key()
    if api_key:
        st.sidebar.success("OpenAI API key detected.")
    else:
        st.sidebar.warning("No API key detected for this session.")
        user_key = st.sidebar.text_input("Enter OpenAI API key", type="password", key="openai_api_key_input")
        if user_key:
            st.session_state["openai_api_key"] = user_key
            api_key = user_key
            st.sidebar.success("API key saved for this session.")
        else:
            st.sidebar.info("You can also set OPENAI_API_KEY in your environment or use a .streamlit/secrets.toml file.")

    render_summary_cards(df)

    st.subheader("Top categories and teams")
    col1, col2 = st.columns(2)
    col1.write(top_values(df, "RK_Category", n=8))
    col2.write(top_values(df, "RK_OperationalOwner", n=8))

    st.markdown("---")
    st.subheader("Ask a question")
    question = st.text_area(
        "Enter your question about ticket trends, team performance, holiday impact, or category issues.",
        value=st.session_state.get("question", ""),
        height=140,
    ) or ""

    if st.button("Submit question") and question.strip():
        prompt = build_prompt(question.strip(), overview["fields"], overview["sample_rows"])
        answer = query_openai(prompt, api_key=api_key)
        st.subheader("Answer")
        st.write(answer)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Notes:**\n"
        "- Set `OPENAI_API_KEY` in your environment.\n"
        "- Set `TICKET_DATA_PATH` to override the default CSV location.\n"
        "- The model only uses the dataset fields shown in the prompt."
    )


if __name__ == "__main__":
    main()
