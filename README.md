<h1 align="center">🛰️ TubeGraph: AI-Powered Video Knowledge Mapper</h1>

<h3 align="center"></b>"Turning linear watch-time into non-linear knowledge maps."</b></h3>

---

### 🌊 The Vision (The "Ocean")

Most people treat YouTube as a "passive" learning tool, watching videos from start to finish. **TubeGraph** flips this. It treats a video as a **Knowledge Base**.

By extracting transcripts and processing them through LLMs, TubeGraph identifies **Atomic Concepts** and their **Prerequisite Links**. The result is a interactive graph where a 20-minute video is condensed into a map you can navigate in 20 seconds.

---

### 🛠️ The Architecture (The "Industry Standard" Stack)

| Layer | Responsibility | Technology |
| --- | --- | --- |
| **Orchestration** | Containerization & Portability | **Docker** (`docker-compose`) |
| **Client** | Interactive Graph UI & State | **React.js + React Flow** |
| **API** | Async Processing & Logic | **FastAPI (Python)** |
| **Intelligence** | Semantic Extraction & JSON Structuring | **Gemini 1.5 Flash/Pro** |
| **Ingestion** | Metadata & Transcript Scraping | **YouTube Transcript API** |
| **Styling** | Clean, Dark-themed "Dev" Aesthetic | **Tailwind CSS** |

---

### 🚀 Key Functional Goals

1. **Semantic Graph Construction:** Don't just summarize; identify "Concept A leads to Concept B."
2. **Contextual Nodes:** Clicking a node in the graph should theoretically show you the timestamp of the video it came from.
3. **JSON-Schema Strictness:** Forcing the AI to output valid JSON every time (Crucial for Industry Standard).
4. **Responsive Layouting:** Using algorithms (like Dagre) to make sure the graph doesn't look like a mess of spaghetti.

---

### 🐳 The Dockerized Workflow

* `docker-compose up` launches your **React** frontend, your **FastAPI** backend, and potentially a **Redis** cache (if you want to avoid hitting the Gemini API for the same video twice).
* No more "It worked on my machine but failed in production💀" The environment is locked.

---

### 📈 Why this "Worth It"?

Building this solves three major engineering hurdles:

1. **Data Cleaning:** Handling messy YouTube transcripts.
2. **Prompt Engineering:** Making an AI think in "Nodes and Edges" rather than paragraphs.
3. **State Management:** Handling complex UI interactions where the user zooms and drags data.

<br />

<h2 align="center">Made with ❤️ by <a target="_blank" href="https://twitter.com/Some1NamedMoksh">TheCodedHuman</a></h2>
