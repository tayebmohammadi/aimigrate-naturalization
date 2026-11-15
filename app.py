"""Local search and answer app. Run with `python -m streamlit run app.py` from the project root."""
import sys
from pathlib import Path
from threading import Lock

import streamlit as st

# Streamlit may not add the script folder when launched from another directory.
APP_ROOT = str(Path(__file__).resolve().parent)
if APP_ROOT in sys.path:
    sys.path.remove(APP_ROOT)
sys.path.insert(0, APP_ROOT)

from retrieval import INDEX, ROOT, SOURCES, Retriever
from answer import AnswerGenerator

METHODS = {"BM25": "bm25", "MiniLM": "minilm"}
# Actual development/training questions used for Stage 2 checks; no held-out QA.
EXAMPLES = [
    "Choose an example…",
    "What is the overall purpose of the administrative naturalization ceremony according to USCIS?",
    "Can Form N-600 (Application for Certificate of Citizenship) be filed after a child turns 18 years of age?",
    "What immigration status or physical presence requirements must an alien meet at the time of enlistment, reenlistment, extension of service, or induction under INA 329?",
]


def index_signature():
    """Refresh the resource cache if saved inputs change; report missing files early."""
    paths = [SOURCES, ROOT / "retrieval_settings.json", ROOT / "retrieval.py",
             ROOT / "build_index.py", INDEX / "manifest.json", INDEX / "passages.jsonl",
             INDEX / "embeddings.npy", INDEX / "cleaning_audit.jsonl"]
    return tuple((str(p), p.stat().st_size, p.stat().st_mtime_ns) for p in paths)


@st.cache_resource(show_spinner=False)
def get_retriever(signature):
    # Retriever validates fingerprints and reuses saved embeddings. Its model is
    # loaded lazily on the first MiniLM search and retained in this cached object.
    # The lock prevents simultaneous sessions racing to load/use that shared model.
    """Return the cached retriever and its shared-use lock."""
    return Retriever(), Lock()


@st.cache_resource(show_spinner=False)
def get_answer_generator():
    """Return the cached answer model and its shared-use lock."""
    return AnswerGenerator(), Lock()


def clear_search():
    """Clear results when the question or method changes."""
    st.session_state.pop("last_search", None)
    st.session_state.pop("last_answer", None)


def use_example():
    """Copy a selected development example into the question box."""
    selected = st.session_state["example"]
    if selected != EXAMPLES[0]:
        st.session_state["question"] = selected
        clear_search()


def show_error(message, error, command):
    """Show a readable error and the local command that may resolve it."""
    st.error(message)
    st.write("Run this from a local terminal, then try Search again:")
    st.code(f"cd {ROOT}\n{command}", language="bash")
    with st.expander("Technical error details"):
        st.code(f"{type(error).__name__}: {error}", language="text")


def show_answer(result):
    """Display a draft, its mapped citations, supplied evidence, and validation state."""
    st.subheader("Draft answer")
    status = result['status']
    if status == 'answered':
        st.text(result['displayed_answer'])
        for source in result['citations']:
            st.markdown(f"**{source['citation_id']}** — [{source['title']}]({source['url']})")
    elif status == 'abstained':
        st.info(result['displayed_answer'])
        st.caption("The model judged the supplied evidence insufficient. This is not a verified scope detector.")
    elif status == 'input_error':
        st.warning(result['error'])
    elif status in ('loading_error', 'generation_error'):
        st.error("The local answer model could not load or generate a response. Retrieval remains available.")
        st.code(f"cd {ROOT}\n.venv/bin/python answer.py --download", language="bash")
        with st.expander("Answer error details"):
            st.text(result['error'])
    else:
        st.error(f"No accepted answer: {status.replace('_', ' ')}. "
                 "This is an output-validation failure, not an evidence-based abstention.")
        st.caption(result.get('validation_error', ''))
    st.caption("Citation IDs and quote presence are checked, not factual support. Development checks "
               "found incorrect answers even with valid citations. Inspect every claim against the "
               "evidence; this is general information, not a personal eligibility decision.")
    if result.get('evidence'):
        with st.expander("Evidence supplied for this answer"):
            for source in result['evidence']:
                st.write(f"{source['citation_id']} {source['title']}")
                st.markdown(f"[{source['url']}]({source['url']})")
                st.text(source['text'])
                st.caption(f"Document: {source['doc_id']} | Passage: {source['passage_id']}")
        st.caption(f"Local CPU generation: {result['runtime_seconds']:.1f} seconds.")
    if result.get('raw_response') is not None:
        with st.expander("Raw model response"):
            st.text(result['raw_response'])


def main():
    """Render the local Streamlit search and evidence-grounded answer interface."""
    st.set_page_config(page_title="AImigrate — USCIS source search", page_icon="🔎")
    st.title("AImigrate — USCIS source search")
    st.write("Search a selected collection of 57 official USCIS naturalization source "
             "documents. Compare keyword search (BM25) with semantic search (MiniLM) "
             "and inspect the best matching passages.")
    st.info("Course prototype for general information: source passages come from a downloaded "
            "snapshot and have not yet been independently checked against current USCIS pages. "
            "Generated answers are drafts; inspect the evidence and official sources.")
    st.caption("Unrelated questions may still retrieve results. The local answer model is asked "
               "to abstain when evidence is insufficient, but it can make mistakes.")

    st.selectbox("Try a development question", EXAMPLES, key="example", on_change=use_example)
    question = st.text_area("Your question", key="question", height=110,
                            placeholder="Type a naturalization question in English", on_change=clear_search)
    method_label = st.radio("Retrieval method", list(METHODS), index=0,
                            horizontal=True, key="method", on_change=clear_search)
    submitted = st.button("Search", type="primary", key="search")

    if submitted:
        clear_search()
        question = question.strip()
        if not question:
            st.warning("Enter a question or choose a development example, then select Search.")
        else:
            try:
                retriever, lock = get_retriever(index_signature())
            except Exception as error:
                show_error("The saved retrieval index could not be loaded. Check the "
                           "files or rebuild the index; the app does not rebuild it automatically.",
                           error, "HF_HUB_OFFLINE=1 .venv/bin/python build_index.py")
            else:
                try:
                    with st.spinner(f"Searching with {method_label}…"):
                        with lock:
                            results = retriever.search(question, method=METHODS[method_label],
                                                       top_k=3, distinct_documents=True)
                    st.session_state["last_search"] = {
                        "question": question, "method": method_label, "results": results}
                except Exception as error:
                    if isinstance(error, ValueError) and "Input exceeds model limit" in str(error):
                        st.warning("This question is too long for MiniLM. Shorten it and "
                                   "search again, or select BM25. The question was not truncated.")
                    elif method_label == "MiniLM":
                        show_error("MiniLM could not load or run from the local model cache. "
                                   "Check the model below, then retry; BM25 can still be used. "
                                   "The check may need internet access if model files are missing.",
                                   error, ".venv/bin/python -m scripts.smoke_check")
                    else:
                        show_error("BM25 could not complete the search.", error,
                                   "HF_HUB_OFFLINE=1 .venv/bin/python build_index.py")

    last = st.session_state.get("last_search")
    if not last:
        return
    st.caption("Optional: generate a draft using these passages. Local CPU generation "
               "can take a minute or longer; the model stays loaded for later requests.")
    if st.button("Generate answer from this evidence", key="generate_answer"):
        st.session_state.pop('last_answer', None)
        try:
            with st.spinner("Loading the local CPU answer model…"):
                generator, answer_lock = get_answer_generator()
        except Exception as error:
            st.session_state['last_answer'] = {
                'status': 'loading_error', 'error': f'{type(error).__name__}: {error}'}
        else:
            try:
                with st.spinner("Generating a draft from the retrieved evidence…"):
                    with answer_lock:
                        st.session_state['last_answer'] = generator.answer(last['question'], last['results'])
            except ValueError as error:
                st.session_state['last_answer'] = {'status': 'input_error', 'error': str(error)}
            except Exception as error:
                st.session_state['last_answer'] = {
                    'status': 'generation_error', 'error': f'{type(error).__name__}: {error}'}
    if st.session_state.get('last_answer'):
        show_answer(st.session_state['last_answer'])
    st.header("Retrieved sources")
    st.write(f"Results for: {last['question']}")
    st.caption(f"Method: {last['method']}. Each source is ranked by its best passage; "
               "the three results have distinct document IDs. Scores are retrieval "
               "ranking values, not answer-confidence percentages. The two methods "
               "use different score scales.")
    for rank, result in enumerate(last["results"], 1):
        with st.container(border=True):
            st.subheader(f"{rank}. {result['title']}")
            st.markdown(f"[{result['url']}]({result['url']})")
            score_label = "BM25 score" if last["method"] == "BM25" else "MiniLM cosine similarity"
            st.caption(f"{score_label}: {result['score']:.6f}")
            st.write("Best matching passage")
            st.text(result["text"])
            with st.expander("Passage and source details"):
                st.code(f"Document ID: {result['doc_id']}\n"
                        f"Passage ID: {result['passage_id']}\n"
                        f"Content tokens: {result['content_tokens']}\n"
                        f"Cleaned source character range: {result['cleaned_char_start']}"
                        f"–{result['cleaned_char_end']}", language="text")


if __name__ == "__main__":
    main()
