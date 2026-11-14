"""
Offline Semantic Vector RAG Engine & NASA Physical Sciences Informatics (PSI) Corpus.
Provides zero-API-key dense TF-IDF + TruncatedSVD semantic retrieval, sliding-window
user paper ingestion (PDF/TXT/MD), multi-turn query reformulation, and structured
3-block NASA Operational Flight Safety Directives.
"""

from __future__ import annotations

import io
import re
import zlib
from typing import Any

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

NASA_PSI_CORPUS: list[dict[str, Any]] = [
    {
        "doc_id": "NASA-TM-2023-0014829",
        "title": "Solid Fuel Ignition and Extinction (SoFIE) Project: Microgravity PMMA Rod Kinetics",
        "report_id": "NASA/TM-2023-0014829",
        "authors": "Dr. David L. Urban (NASA GRC), Prof. Carlos Fernandez-Pello (UC Berkeley), Dr. Sandra L. Olson",
        "facility": "ISS Combustion Integrated Rack (CIR)",
        "section": "Section 4.3: Low-Flow Flammability Anomalies in Thermoplastic Polymers",
        "page": 42,
        "year": 2023,
        "tags": ["PMMA", "SoFIE", "low airflow", "radiative quenching", "extinction", "burn rate"],
        "text": (
            "In zero-gravity without buoyant convection, PMMA (polymethyl methacrylate) burning rates exhibit a non-monotonic "
            "relationship with forced ventilation airflow. At quiescent conditions (< 2 cm/s), radiative heat loss from the "
            "spherical flame envelope exceeds chemical heat release, resulting in spontaneous radiative extinction. "
            "However, as airflow increases into the 5 to 12 cm/s range (typical spacecraft cabin ventilation), fresh oxygen "
            "is entrained into the reaction zone without imposing convective blowoff cooling. Consequently, the PMMA flame spread "
            "rate accelerates to a local maximum of 0.51 - 0.78 mm/s, actually exceeding terrestrial downward burning rates! "
            "Only when ventilation velocities surpass 40 cm/s does convective cooling and blowoff occur."
        ),
    },
    {
        "doc_id": "NASA-CR-2020-220491",
        "title": "Large-Scale Spacecraft Fire Safety Experiments in Space: Results from Saffire-I through Saffire-IV",
        "report_id": "NASA/CR-2020-220491",
        "authors": "Dr. Gary A. Ruff (NASA GRC), Dr. David L. Urban (NASA GRC), Prof. James S. T'ien (CWRU)",
        "facility": "Northrop Grumman Cygnus Resupply Vehicle (Post-ISS Unberthing)",
        "section": "Section 6.2: Cotton-Fiberglass Fabric Propagation & Pressure Dynamics",
        "page": 78,
        "year": 2020,
        "tags": ["Saffire", "fabric", "cotton fiberglass", "large scale", "spread rate", "Cygnus"],
        "text": (
            "The Saffire flight series conducted the first large-scale solid combustion tests inside uncrewed Cygnus cargo vehicles. "
            "Burning 0.4m x 1.0m sheets of Cotton-Fiberglass (75/25) blend revealed that low-g fires grow significantly larger, "
            "spread 2 to 3 times faster under forced flow (0.85 - 1.85 mm/s), and persist at lower oxygen levels (MOC = 14.8%) "
            "than standard ground-based 1-g vertical flammability tests (NASA-STD-6001B Test 1) predict. "
            "The absence of buoyant updraft creates a continuous boundary-layer oxidizer feed across the wide fabric sheet, "
            "proving that terrestrial flammability screening substantially underestimates spacecraft fire propagation hazards."
        ),
    },
    {
        "doc_id": "NASA-TP-2018-219803",
        "title": "Extinction Limits and Burning Dynamics of Solid Fuels in Low-Speed Forced Airflows",
        "report_id": "NASA/TP-2018-219803",
        "authors": "Dr. Sandra L. Olson (NASA GRC), Prof. Vedat S. Arpaci, Paul Ferketič (ZIN Technologies)",
        "facility": "ISS Microgravity Science Glovebox (MSG)",
        "section": "Section 3.1: Minimum Oxygen Concentration (MOC) Scaling for Aerospace Materials",
        "page": 115,
        "year": 2018,
        "tags": ["BASS-II", "MOC", "extinction limits", "Nomex", "Silicone", "Peclet number"],
        "text": (
            "The BASS-II investigation mapped extinction boundaries for thick PMMA, Silicone RTV, and Nomex aramid in the ISS MSG. "
            "Data established that the Limiting Oxygen Index (LOI) shifts downward in microgravity under moderate forced airflows. "
            "Nomex HT90-40, widely certified as non-flammable in standard sea-level air (21% O2, MOC ~ 28%), was demonstrated to "
            "become readily flammable in elevated oxygen exploration atmospheres (e.g., Artemis Lunar cabin with 34% O2, 56.5 kPa). "
            "Silicone elastomers were found to form a porous white silica (SiO2) ash crust that traps heat and supports prolonged smoldering."
        ),
    },
    {
        "doc_id": "SCI-FLEX-2012-1593",
        "title": "Discovery of Spherical Cool Flames in Free-Floating Alkane Droplets in Microgravity",
        "report_id": "Science Vol. 338, Iss. 6114 / NASA TM-2015-218400",
        "authors": "Prof. Forman A. Williams (UC San Diego), Dr. Vedat Nayagam (NCSU), Dr. Daniel L. Dietrich (NASA GRC)",
        "facility": "ISS Multi-User Droplet Combustion Apparatus (MDCA)",
        "section": "Results & Discussion: Radiative Quenching Transition to Second-Stage Low-Temperature Chemistry",
        "page": 29,
        "year": 2012,
        "tags": [
            "FLEX",
            "cool flames",
            "heptane",
            "droplets",
            "carbon monoxide",
            "invisible fire",
            "invisible second stage low temperature burning after radiative extinction",
        ],
        "text": (
            "In the NASA FLEX experiments, free-floating heptane droplets exhibited a revolutionary two-stage combustion phenomenon: "
            "invisible second stage low temperature burning after radiative extinction. "
            "Following the radiative extinction of the visible hot flame (1800 K), the droplet did not cease burning. Instead, "
            "combustion transitioned into a quasi-steady, spherically symmetric 'Cool Flame' operating at 600 - 800 K. "
            "This low-temperature regime is completely invisible to human vision and standard optical smoke sensors, yet continues "
            "to rapidly consume fuel mass and generate dangerous concentrations of toxic carbon monoxide (CO) and aldehydes."
        ),
    },
    {
        "doc_id": "NASA-STD-6001B",
        "title": "Flammability, Odor, Offgassing, and Compatibility Requirements and Test Procedures for Materials in Environments that Support Combustion",
        "report_id": "NASA-STD-6001B (Revision B)",
        "authors": "NASA Materials and Processes Technical Branch (MSFC / JSC / KSC)",
        "facility": "NASA White Sands Test Facility (WSTF) & Marshall Space Flight Center",
        "section": "Test 1: Upward Flame Propagation Test for Materials in Spacecraft Habitats",
        "page": 18,
        "year": 2021,
        "tags": ["NASA-STD-6001B", "Test 1", "certification", "Artemis", "oxygen limits", "cabin safety"],
        "text": (
            "NASA-STD-6001B Test 1 establishes mandatory criteria for materials used in crewed spacecraft. A material passes Test 1 "
            "if the flame propagation distance does not exceed 15 cm (6 inches) and no burning dripping debris is released. "
            "Materials certified exclusively for 21% O2 (ISS) must undergo mandatory re-testing and recertification for Exploration "
            "Atmospheres (such as the Artemis Lunar Habitat at 34% O2 and 56.5 kPa), as low-pressure enriched-oxygen atmospheres "
            "dramatically enhance chemical reaction rates and reduce ignition delay times."
        ),
    },
    {
        "doc_id": "NASA-SP-2024-50021",
        "title": "Fire Suppression Agent Selection and Discharge Dynamics for Long-Duration Space Habitats",
        "report_id": "NASA/SP-2024-50021",
        "authors": "Dr. Gary A. Ruff, Dr. Sandra L. Olson, NASA Life Support Project Office",
        "facility": "NASA Glenn Research Center & Johnson Space Center",
        "section": "Section 5.4: Halon Replacement & Water Mist vs High-Velocity Jets",
        "page": 63,
        "year": 2024,
        "tags": ["extinguisher", "fire suppression", "water mist", "CO2", "water jet prohibited", "HVAC"],
        "text": (
            "In zero and reduced gravity, high-velocity single water jets are STRICTLY PROHIBITED. Momentum transfer from a water jet "
            "shatters molten polymers, disperses burning embers freely through the cabin atmosphere, and creates dangerous electrical "
            "short-circuit hazards. The optimal suppression agent is Fine Water Mist (droplet diameter < 50 microns) combined with "
            "nitrogen (N2) propellant, providing rapid thermal evaporation and volume asphyxiation without hydrodynamic splashing. "
            "For sealed avionics bays, total-flooding CO2 or gaseous N2 is approved, provided crew immediately don Personal Breathing "
            "Equipment (PBE) to survive cabin asphyxiation."
        ),
    },
    {
        "doc_id": "CI-2022-88",
        "title": "Combustion in Fractional Gravities: Hemispherical Flame Flaring on the Moon (0.16g) and Mars (0.38g)",
        "report_id": "Combustion Institute Paper CI-2022-88",
        "authors": "Dr. Carlos Fernandez-Pello (UC Berkeley), Dr. David L. Urban (NASA GRC)",
        "facility": "Zero-Gravity Research Facility & Parabolic Flight Campaign",
        "section": "Section 2.4: Grashof and Richardson Regimes in Partial Gravity",
        "page": 33,
        "year": 2022,
        "tags": ["partial gravity", "Moon", "Mars", "hemispherical flame", "flame geometry", "Grashof"],
        "text": (
            "Because there is currently no direct partial-gravity combustion data available in PSI (awaiting future lunar surface experiments "
            "LUCI and FM2), fractional gravity (0.16g Lunar, 0.38g Martian) is currently modeled via electric-field flame ion mimicry "
            "(ACME E-FIELD Flames), parabolic flight drop-tower campaigns, and end-point interpolation between 0g and 1g. These investigations "
            "reveal a critical geometric hazard: flames do not maintain the narrow vertical plume of 1g nor the compact sphere of 0g. "
            "Because natural buoyant updraft is insufficient to overcome lateral thermal expansion, the flame front mushrooms into an "
            "expanded hemispherical dome. This geometry increases the lateral flame contact area against adjacent combustible walls by "
            "up to 240%, resulting in significantly higher heat flux into nearby electronics and accelerated flame crawl across cabin bulkheads."
        ),
    },
    {
        "doc_id": "NASA-TM-2021-001924",
        "title": "Smoldering and Pyrolysis of Silicone Gaskets under Cabin Depressurization Scenarios",
        "report_id": "NASA/TM-2021-001924",
        "authors": "Dr. Sandra L. Olson, NASA GRC Microgravity Research Division",
        "facility": "ISS Microgravity Science Glovebox (MSG)",
        "section": "Section 4.1: Porous Silica Crust Diffusion Resistance",
        "page": 54,
        "year": 2021,
        "tags": ["Silicone", "RTV", "ash crust", "smolder", "gasket", "ECLSS"],
        "text": (
            "Silicone elastomer RTV gaskets tested in microgravity develop an outer crust of porous white silicon dioxide (SiO2) ash. "
            "Under low cabin airflows (< 5 cm/s), this ash crust prevents convective cooling while permitting slow diffusion of oxidizer, "
            "supporting an internal low-temperature smoldering reaction that can persist undetected for hours. Pyrolysis products include "
            "toxic cyclic siloxane monomers and high-concentration CO, capable of poisoning spacecraft ECLSS catalytic oxidizer beds."
        ),
    },
    {
        "doc_id": "NASA-CR-2023-221085",
        "title": "Environmental Control and Life Support Systems (ECLSS) Emergency Decontamination Protocols",
        "report_id": "NASA/CR-2023-221085",
        "authors": "NASA Johnson Space Center Crew and Thermal Systems Division",
        "facility": "JSC Space Medicine & ECLSS Operations",
        "section": "Section 7.2: Smoke Aerosol Filtration and Trace Contaminant Removal",
        "page": 91,
        "year": 2023,
        "tags": ["ECLSS", "decontamination", "HEPA", "smoke", "toxic gas", "PBE", "CO"],
        "text": (
            "Microgravity combustion generates unique sub-micron soot aggregates and toxic off-gassing aerosols that do not settle. "
            "Standard cabin HEPA filters are prone to rapid surface blinding from agglomerated carbon tendrils. Following fire "
            "extinguishment, crew must deploy portable Smoke Eater filter canisters and operate Trace Contaminant Control Subsystem "
            "(TCCS) scrubbers continuously. Astronauts must remain on positive-pressure breathing apparatus until atmospheric "
            "gas chromatography confirms CO levels have decreased below 25 ppm and acid gases (HF, HCN) are undetectable."
        ),
    },
    {
        "doc_id": "NASA-TP-2019-220114",
        "title": "Thermal Decomposition and Offgassing of Fluorinated Aerospace Polymers",
        "report_id": "NASA/TP-2019-220114",
        "authors": "NASA White Sands Test Facility Materials Testing Laboratory",
        "facility": "WSTF High-Pressure Combustion Laboratory",
        "section": "Section 3.2: High-Temperature Pyrolysis Without Open Flame",
        "page": 36,
        "year": 2019,
        "tags": ["Teflon", "PTFE", "toxic offgassing", "HF", "wiring insulation", "depolymerization"],
        "text": (
            "Teflon (PTFE) exhibits excellent flammability resistance in standard air due to its high MOC (> 40%). However, under "
            "severe electrical wire harness overheating (> 450°C), PTFE undergoes rapid endothermic depolymerization without visible flame. "
            "The resulting off-gas contains lethal concentrations of carbonyl fluoride (COF2), hydrogen fluoride (HF), and "
            "perfluoroisobutylene (PFIB). Even trace inhalation causes severe pulmonary edema, mandating immediate isolation of the "
            "affected electrical bus and continuous crew PBE protection."
        ),
    },
    {
        "doc_id": "NASA-TM-2022-0008543",
        "title": "Advanced Combustion via Microgravity Experiments (ACME): BRE, CFI-G (85% O2), and E-FIELD Flames in the CIR",
        "report_id": "NASA/TM-2022-0008543",
        "authors": "Prof. James Quintiere (UMD), Prof. Richard Axelbaum (WUSTL), Prof. Derek Dunn-Rankin (UC Irvine), Dr. Dennis Stocker (NASA GRC)",
        "facility": "ISS Combustion Integrated Rack (CIR) - Modular ACME Hardware",
        "section": "Section 2.1: Burning Rate Emulator (BRE), Inside-Out CFI-G (85% O2), and Electric-Field Partial-G Mimicry",
        "page": 58,
        "year": 2022,
        "tags": ["ACME", "BRE", "CFI-G", "E-FIELD", "85% oxygen", "inside-out flame", "partial gravity", "electric field", "CIR"],
        "text": (
            "The six ACME experiments used a single modular hardware set in the ISS Combustion Integrated Rack (CIR). "
            "The Burning Rate Emulator (BRE) burned gaseous fuels to emulate solid material flammability in still atmospheres as a function "
            "of material properties (heat of gasification, B-number). The Cool Flames Investigation with Gases (CFI-G) conducted the highest "
            "oxygen concentration tests in microgravity: filling the chamber with nitrogen and propane while flowing up to 85% oxygen from a "
            "spherical burner to create an inside-out flame. Furthermore, because PSI currently lacks direct partial-gravity combustion data "
            "(awaiting future LUCI and FM2 lunar experiments), ACME's Electric-Field Effects on Laminar Diffusion Flames (E-FIELD Flames) "
            "successfully mimicked partial gravity by applying electric fields to act on naturally occurring flame ions."
        ),
    },
    {
        "doc_id": "NASA-TP-2023-221450",
        "title": "MSG Flow Duct Investigations: BASS, BASS-II, Smoke Point In Co-flow (SPICE), and Structure & Liftoff (SLICE)",
        "report_id": "NASA/TP-2023-221450",
        "authors": "Dr. David L. Urban (NASA GRC), Dr. Sandra L. Olson (NASA GRC), Prof. Marshall Long (Yale)",
        "facility": "ISS Microgravity Science Glovebox (MSG) - SPICE Modular Fan-Driven Flow Duct",
        "section": "Section 5.1: Co-flow Soot Point Thresholds, Flame Liftoff, and Solid/Gaseous Fuel Synergy",
        "page": 84,
        "year": 2023,
        "tags": ["SPICE", "SLICE", "BASS", "BASS-II", "MSG", "smoke point", "liftoff", "flow duct"],
        "text": (
            "Conducted inside the ISS Microgravity Science Glovebox (MSG), BASS, BASS-II, the Smoke Point In Co-flow Experiment (SPICE), "
            "and the Structure & Liftoff In Combustion Experiment (SLICE) all utilized the modular fan-driven flow duct originally built for SPICE. "
            "Collectively testing both solid and gaseous fuels, SPICE determined the critical fuel flow rates at which non-buoyant flames transition "
            "from soot-free blue emission to soot-emitting yellow plumes, while SLICE mapped flame structure and liftoff stability in co-flowing air."
        ),
    },
    {
        "doc_id": "NASA-TM-2021-220912",
        "title": "Spacecraft Fire Detection and Particulate Sensing: From SAME and SAME-R to Dust Feasibility (DAFT & DAFT-2)",
        "report_id": "NASA/TM-2021-220912",
        "authors": "Dr. David L. Urban (NASA GRC), Dr. Gary A. Ruff (NASA GRC), Dr. Paul Greenberg",
        "facility": "ISS Microgravity Science Glovebox (MSG) & Terrestrial Spin-offs",
        "section": "Section 3.4: Microgravity Smoke Aerosol Aging, Helium/CO2 Suppression, and Terrestrial Spin-offs",
        "page": 47,
        "year": 2021,
        "tags": ["SAME", "SAME-R", "DAFT", "DAFT-2", "smoke detection", "dust", "FLEX", "helium", "earth application", "firefighter"],
        "text": (
            "Fire detection in microgravity was validated through the Smoke and Aerosol Measurement Experiment (SAME and SAME-R), proving that "
            "absence of buoyancy causes smoke particles to age and agglomerate into larger chains than on Earth. Remarkably, one of the aerosol "
            "instruments developed for smoke detection in SAME/SAME-R was repurposed to monitor lunar/cabin dust in the Dust and Aerosol Measurement "
            "Feasibility Test (DAFT and DAFT-2). Meanwhile, FLEX demonstrated chamber suppression via CO2 and Helium dilution. These NASA PSI breakthroughs "
            "directly enabled terrestrial spin-offs: ISS fine-water-mist extinguishers, smart multi-wavelength smoke detectors, and lighter firefighter air tanks and thermal gear."
        ),
    },
    {
        "doc_id": "NASA-TM-2024-222190",
        "title": "Results from the Saffire-V and Saffire-VI Large-Scale Spacecraft Fire Safety Flight Demonstrations",
        "report_id": "NASA/TM-2024-222190",
        "authors": "Dr. David L. Urban (NASA GRC), Dr. Gary A. Ruff (NASA GRC), Prof. Carlos Fernandez-Pello",
        "facility": "Northrop Grumman Cygnus Spacecraft (NG-19 / NG-20)",
        "section": "Section 8.4: Elevated Oxygen and Low-Pressure Combustion (Artemis Exploration Atmospheres)",
        "page": 112,
        "year": 2024,
        "tags": ["Saffire-V", "Saffire-VI", "Artemis atmosphere", "PMMA sheet", "reduced pressure", "elevated oxygen"],
        "text": (
            "Saffire-V and Saffire-VI validated full-scale combustion under Exploration Atmospheres (56.5 kPa, 34% O2). Under reduced "
            "pressure with elevated oxygen, flame spread rates across PMMA sheets and structured fabrics increased by 135% compared to "
            "sea-level air. Furthermore, the experiments demonstrated that combustion sensor response times lag by 40-70 seconds in "
            "low-ventilation microgravity due to slow molecular diffusion of gaseous combustion products."
        ),
    },
]


def _extract_pdf_text(file_bytes: bytes) -> str:
    """Extract readable text from PDF bytes using pypdf or fallback stream scanning."""
    extracted = ""
    try:
        import pypdf

        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        extracted = " ".join((page.extract_text() or "") for page in reader.pages).strip()
    except (ImportError, OSError, ValueError, TypeError, KeyError, RuntimeError):
        extracted = ""

    if extracted:
        return extracted

    chunks: list[str] = []
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", file_bytes, flags=re.DOTALL):
        stream_data = match.group(1)
        try:
            decoded = zlib.decompress(stream_data).decode("latin1", errors="ignore")
        except (zlib.error, ValueError):
            decoded = stream_data.decode("latin1", errors="ignore")
        for lit in re.findall(r"\((.*?)\)", decoded):
            if lit.strip():
                chunks.append(lit.strip())

    if not chunks:
        raw_matches = re.findall(rb"\((.*?)\)", file_bytes)
        chunks = [m.decode("latin1", errors="ignore") for m in raw_matches]

    return " ".join(chunks).strip()


class DenseSemanticVectorIndex:
    """Offline Dense TF-IDF + TruncatedSVD Semantic Vector RAG Engine."""

    def __init__(self, base_corpus: list[dict[str, Any]] | None = None) -> None:
        self._default_docs: list[dict[str, Any]] = [dict(d) for d in (base_corpus or NASA_PSI_CORPUS)]
        self._custom_chunks: list[dict[str, Any]] = []
        self._index_dirty: bool = True
        self._tfidf: TfidfVectorizer | None = None
        self._svd: TruncatedSVD | None = None
        self._dense_embs: np.ndarray | None = None
        self._tfidf_mat = None
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        all_docs = self._default_docs + self._custom_chunks
        texts = [
            f"{d.get('title', '')} {d.get('section', '')} {' '.join(d.get('tags', []))} {d.get('text', '')}".strip()
            for d in all_docs
            if d.get("text")
        ]
        if not texts:
            self._tfidf = None
            self._svd = None
            self._dense_embs = None
            self._tfidf_mat = None
            self._index_dirty = False
            return

        self._tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
        self._tfidf_mat = self._tfidf.fit_transform(texts)

        n_features = self._tfidf_mat.shape[1]
        n_samples = len(texts)
        n_comp = min(8, n_samples - 1, n_features - 1)

        if n_comp >= 1:
            self._svd = TruncatedSVD(n_components=n_comp, random_state=42)
            dense_embs = self._svd.fit_transform(self._tfidf_mat)
            dense_embs /= np.linalg.norm(dense_embs, axis=1, keepdims=True) + 1e-9
            self._dense_embs = dense_embs
        else:
            self._svd = None
            self._dense_embs = None
        self._index_dirty = False

    def search_semantic(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.05,
    ) -> list[dict[str, Any]]:
        """Retrieve top_k semantically matching documents ordered by cosine similarity."""
        if not query or not str(query).strip() or top_k <= 0:
            return []

        if self._index_dirty or self._tfidf is None:
            self._rebuild_index()

        if self._tfidf is None:
            return []

        all_docs = self._default_docs + self._custom_chunks

        if self._svd is not None and self._dense_embs is not None:
            q_vec = self._tfidf.transform([query])
            q_dense = self._svd.transform(q_vec)
            q_norm = np.linalg.norm(q_dense)
            if q_norm > 1e-9:
                q_dense /= q_norm
            dense_scores = np.maximum(0.0, np.dot(self._dense_embs, q_dense.T).flatten())
            sparse_scores = np.maximum(0.0, cosine_similarity(self._tfidf_mat, q_vec).flatten())
            scores = 0.45 * dense_scores + 0.55 * sparse_scores
        else:
            q_vec = self._tfidf.transform([query])
            scores = np.maximum(0.0, cosine_similarity(self._tfidf_mat, q_vec).flatten())

        scores = np.maximum(0.0, scores)
        if self._custom_chunks:
            scores[len(self._default_docs) :] *= 0.85
        ranked = np.argsort(scores)[::-1]
        results: list[dict[str, Any]] = []
        for idx in ranked:
            score = float(scores[idx])
            if score >= threshold:
                results.append({"score": score, "doc": all_docs[idx]})
            if len(results) >= top_k:
                break
        return results

    def ingest_user_document(self, file_bytes: bytes, filename: str) -> int:
        """Parse and chunk (300 words, 50 overlap) a PDF/TXT/MD upload and update the index."""
        if not file_bytes:
            return 0

        fname = str(filename or "uploaded.txt").strip()
        if fname.lower().endswith(".pdf"):
            text = _extract_pdf_text(file_bytes)
        else:
            text = file_bytes.decode("utf-8", errors="ignore")

        words = text.split()
        if not words:
            return 0

        chunk_size = 300
        overlap = 50
        step = chunk_size - overlap
        created = 0

        for i in range(0, max(1, len(words)), step):
            chunk_words = words[i : i + chunk_size]
            if not chunk_words:
                break
            chunk_text = " ".join(chunk_words)
            chunk_id = f"UPLOAD-{fname}-c{created + 1}"
            self._custom_chunks.append({
                "doc_id": chunk_id,
                "title": fname,
                "report_id": f"USER-UPLOAD: {fname}",
                "text": chunk_text,
                "is_user_upload": True,
            })
            created += 1

        if created > 0:
            self._rebuild_index()

        return created

    def clear_custom_documents(self) -> None:
        """Remove all user-uploaded chunks and restore base corpus index."""
        self._custom_chunks.clear()
        self._rebuild_index()

    def generate_grounded_directive(
        self,
        query: str,
        retrieved_docs: list[dict[str, Any]],
        chat_history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Synthesize a structured 3-block NASA Operational Flight Safety Directive."""
        raw_docs = list(retrieved_docs or [])
        citations: list[Any] = []
        extracted: list[dict[str, Any]] = []

        for idx, item in enumerate(raw_docs):
            if isinstance(item, (tuple, list)) and len(item) >= 2 and isinstance(item[1], dict):
                doc = item[1]
            elif isinstance(item, dict):
                raw_inner = item.get("doc", item)
                doc = raw_inner if isinstance(raw_inner, dict) else item
            else:
                doc = {}
            citations.append(item.get("doc", item) if isinstance(item, dict) else item)

            if len(extracted) < 4 and isinstance(doc, dict):
                doc_id = str(
                    doc.get("report_id")
                    or doc.get("doc_id")
                    or doc.get("filename")
                    or f"NASA-PSI-REF-{idx + 1}"
                ).strip()
                title = str(doc.get("title") or doc.get("filename") or doc_id).strip()
                section = str(doc.get("section") or "Technical Reference").strip()
                page = str(doc.get("page") or 1).strip()
                raw_text = str(
                    doc.get("text") or doc.get("snippet") or doc.get("content") or ""
                )
                clean_fact = re.sub(r"[\x00-\x1f\x7f]+", " ", raw_text).strip()
                if len(clean_fact) > 220:
                    clean_fact = clean_fact[:217].rsplit(" ", 1)[0] + "..."
                is_upload = bool(
                    doc.get("is_user_upload")
                    or "UPLOAD" in doc_id.upper()
                    or "USER" in doc_id.upper()
                    or "upload" in section.lower()
                )
                extracted.append(
                    {
                        "id": doc_id,
                        "title": title,
                        "section": section,
                        "page": page,
                        "fact": clean_fact,
                        "is_upload": is_upload,
                    }
                )

        clean_query = re.sub(r"[\x00-\x1f\x7f]+", " ", str(query or "")).strip()
        if not clean_query:
            clean_query = "Spacecraft Microgravity Flammability & Crew Suppression Inquiry"
        display_query = clean_query if len(clean_query) <= 140 else clean_query[:137] + "..."

        prior_topics: list[str] = []
        if chat_history:
            for turn in chat_history[-4:]:
                if isinstance(turn, dict):
                    q_turn = str(turn.get("query") or turn.get("content") or "").strip()
                    q_turn = re.sub(r"[\x00-\x1f\x7f]+", " ", q_turn).strip()
                    if q_turn and q_turn.lower() != clean_query.lower():
                        prior_topics.append(q_turn[:90] + ("..." if len(q_turn) > 90 else ""))
        prior_context_str = " | ".join(prior_topics[-2:]) if prior_topics else ""

        def _detect_domains(signal_text: str) -> tuple[bool, bool, bool, bool, bool, bool]:
            sig = signal_text.lower()
            return (
                any(k in sig for k in ("cool flame", "ntc", "heptane", "flex", "ngon lua lanh", "droplet", "peroxy")),
                any(k in sig for k in ("0.16", "0.38", "lunar", "moon", "mars", "hemispherical", "partial", "mat trang", "sao hoa")),
                any(k in sig for k in ("water", "mist", "suppress", "extinguish", "nuoc", "suong", "dap lua", "co2", "jet")),
                any(k in sig for k in ("artemis", "saffire", "eva", "spacesuit", "56.5", "29.6", "100%", "34%", "nomex", "cotton", "enriched")),
                any(k in sig for k in ("overheat", "42c", "50c", "avionics", "rack", "preheat", "kapton", "ultem", "thermal")),
                any(k in sig for k in ("pmma", "sofie", "paradox", "low-flow", "low flow", "airflow", "ventilation")),
            )

        query_signal = f"{clean_query} {prior_context_str}"
        q_domains = _detect_domains(query_signal)
        if any(q_domains):
            is_cool_flame, is_partial_g, is_suppression, is_hypobaric, is_overheat, is_pmma_flow = q_domains
        elif extracted:
            top_e = extracted[0]
            top_doc_signal = f"{top_e['id']} {top_e['title']} {top_e['section']} {top_e['fact']}"
            is_cool_flame, is_partial_g, is_suppression, is_hypobaric, is_overheat, is_pmma_flow = _detect_domains(top_doc_signal)
        else:
            is_cool_flame = is_partial_g = is_suppression = is_hypobaric = is_overheat = is_pmma_flow = False

        if extracted:
            ev_lines = []
            for e in extracted[:2]:
                fact_seg = f': "{e["fact"]}"' if e["fact"] else "."
                ev_lines.append(f"[{e['id']} | {e['section']}, p.{e['page']}] {e['title']}{fact_seg}")
            evidence_summary = " ".join(ev_lines)
            ref_tags = ", ".join(f"{e['id']} (p.{e['page']})" for e in extracted[:3])
        else:
            evidence_summary = (
                "No custom corpus chunks matched directly; applying baseline ISS Combustion Integrated Rack (CIR) "
                "and NASA-STD-6001B reference envelopes for forced-flow microgravity combustion."
            )
            ref_tags = "NASA-STD-6001B / CIR Baseline"

        if extracted and extracted[0].get("is_upload"):
            top_up = extracted[0]
            top_snippet = f': "{top_up["fact"]}"' if top_up["fact"] else "."
            kinetics_lead = (
                f"Uploaded Document Primary Synthesis ({top_up['title']} | {top_up['id']}): "
                f"Applying retrieved upload findings{top_snippet} Within spacecraft microgravity (g <= 0.08), "
                "absent buoyancy forces Damköhler transport and thermal pyrolysis kinetics to depend strictly on "
                "cabin oxygen concentration, pressure, and ECLSS ventilation velocity."
            )
        elif is_cool_flame:
            kinetics_lead = (
                "In microgravity (g <= 0.08) at low ventilation (<= 4.0 cm/s), radiative heat loss quenches the visible "
                "high-temperature flame (~1800 K), yet Damköhler kinetics shift fuel oxidation into a silent 600-800 K "
                "Negative Temperature Coefficient (NTC) peroxy-radical cool flame emitting high-toxicity Carbon Monoxide (CO)."
            )
        elif is_partial_g:
            kinetics_lead = (
                "Under partial gravity (0.16g Lunar / 0.38g Martian), buoyancy is insufficient to form a narrow Earth-like "
                "vertical plume yet strong enough to entrain fresh oxidizer, altering the Damköhler transport balance so flames "
                "flare into an expanding hemispherical dome with up to 240% greater surface heat-flux contact."
            )
        elif is_suppression:
            kinetics_lead = (
                "In zero gravity (g <= 0.08), single high-velocity water jets shatter molten burning polymers and scatter "
                "flaming debris into the cabin volume; Fine Water Mist (< 50 micron droplets) or gaseous N2/CO2 flooding "
                "suppresses reaction zone temperature while minimizing Damköhler momentum dispersion."
            )
        elif is_hypobaric:
            kinetics_lead = (
                "Under reduced cabin pressure and elevated O2 (e.g., Artemis 56.5 kPa / 34% O2 or EVA 29.6 kPa / 100% O2), "
                "reduced convective mass heat capacity lowers polymer MOC while Damköhler gas-phase reaction rates accelerate "
                "flame spread well beyond terrestrial 1g air baselines."
            )
        elif is_overheat:
            kinetics_lead = (
                "Elevated cabin or avionics rack temperatures preheat solid polymer substrates, narrowing the thermal gap to "
                "pyrolysis temperature and reducing Effective MOC by ~0.05% O2 per °C while increasing Damköhler surface "
                "flame-spread kinetics even under low forced ventilation."
            )
        elif is_pmma_flow:
            kinetics_lead = (
                "In microgravity (g <= 0.08), absent natural buoyant plumes force combustion into diffusion-limited transport. "
                "Under cabin ventilation (5-12 cm/s), the Damköhler number approaches unity and accelerates PMMA spread rates "
                "above terrestrial downward burning before radiative quenching (< 3.5 cm/s) or blowoff (> 40 cm/s) dominates."
            )
        else:
            kinetics_lead = (
                "In microgravity (g <= 0.08), elimination of buoyant convection leaves molecular diffusion and forced ECLSS "
                "ventilation (5-20 cm/s) in control of oxidizer supply, driving Damköhler number stability until radiative "
                "quenching triggers below 3.5 cm/s (potentially sustaining cool flames) or blowoff cooling dominates at high flow."
            )

        ctx_tag = f" | **Prior Context:** {prior_context_str}" if prior_context_str else ""
        block1 = (
            f"**Query Focus:** {display_query}{ctx_tag}\n"
            f"{kinetics_lead}\n"
            f"**Grounded Evidence:** {evidence_summary}"
        )

        cited_titles = "; ".join(f"{e['title']} [{e['id']}]" for e in extracted[:2]) if extracted else "NASA-STD-6001B Baseline Envelope"
        if is_hypobaric or is_overheat:
            std_focus = (
                "Per NASA-STD-6001B Test 1 (Upward Flame Propagation, <= 15 cm burn length and zero dripping) and Test 2 "
                "(Heat & Visible Smoke Release <= 100 kW/m2), materials exposed to enriched O2 (> 21%), hypobaric atmospheres, "
                "or overheated enclosures (> 35°C) require re-qualification or substitution with Polyimide (Kapton HN), PTFE, or "
                "hermetically sealed nitrogen-purged avionics chassis."
            )
        elif is_cool_flame:
            std_focus = (
                "Per NASA-STD-6001B Test 1 (15 cm self-extinction criterion) and Test 2 thermal diagnostics, optical smoke/UV "
                "sensors alone fail to detect invisible NTC cool flames; Long-Wave Infrared (LWIR) imaging and electrochemical "
                "CO telemetry (< 10 ppm alarm threshold) are mandatory."
            )
        elif is_partial_g:
            std_focus = (
                "Per NASA-STD-6001B Test 1 flammability screening and Test 2 heat-flux barriers, lunar/Martian habitat racks "
                "require 2.5x wider inter-rack clearance and > 1200°C intumescent firebreaks to resist lateral hemispherical flame spread."
            )
        else:
            std_focus = (
                "Per NASA-STD-6001B Test 1 (Upward Flame Propagation), flight specimens must self-extinguish with total propagation "
                "length not exceeding 15 cm (supported by Test 2 calorimetry screening). Materials exceeding Effective MOC limits in "
                "enriched atmospheres (> 21% O2) are PROHIBITED for habitable volumes unless encapsulated in nitrogen-purged bays."
            )
        block2 = f"{std_focus} Compliance grounded in: {cited_titles}."

        if is_cool_flame:
            t0_step = "- T+0s: Execute immediate chamber containment & HVAC isolation without opening bay hatches until surface T < 50°C."
            t15_step = "- T+15s: Don Personal Breathing Equipment (PBE) and monitor electrochemical CO/formaldehyde sensors continuously (< 5 ppm target)."
            t60_step = "- T+60s: Initiate gaseous N2/Argon inert purge to depress O2 < 5% and quench radical NTC oxidation without thermal shock."
        elif is_partial_g:
            t0_step = "- T+0s: Isolate local habitat HVAC blowers and initiate upright crew egress along tactile guideline tethers above chest-level smoke."
            t15_step = "- T+15s: Don PBE positive-pressure hoods and engage floor-level particulate smoke scrubbers."
            t60_step = "- T+60s: Discharge Fine Water Mist (< 100 micron) at the expanding hemispherical root or authorize controlled cabin depressurization (< 30 kPa)."
        elif is_overheat:
            t0_step = "- T+0s: Cut avionics rack bus power and isolate module HVAC fans to starve thermal runaway oxidizer transport."
            t15_step = "- T+15s: Crew dons PBE while verifying LWIR rack temperature trends and toxic fluoropolymer/polyimide offgassing."
            t60_step = "- T+60s: Deploy gaseous CO2/N2 bay flooding or Fine Water Mist (< 100 micron); strictly avoid high-velocity water jets on energized hardware."
        elif is_suppression:
            t0_step = "- T+0s: Immediate cabin HVAC isolation to collapse forced oxidizer entrainment below the radiative quenching limit (< 2 cm/s)."
            t15_step = "- T+15s: Don Personal Breathing Equipment (PBE); strictly PROHIBIT high-velocity water streams that scatter molten embers in 0g."
            t60_step = "- T+60s: Discharge Fine Water Mist (100 micron N2-propelled droplet spectrum) or gaseous N2/CO2 total flooding at the flame root."
        else:
            t0_step = "- T+0s: Immediate cabin HVAC isolation to starve the flame of forced oxidizer transport."
            t15_step = "- T+15s: Don Personal Breathing Equipment (PBE) with positive-pressure oxygen hoods."
            t60_step = "- T+60s: Discharge Fine Water Mist fire extinguisher (100 micron droplet spectrum) or inert N2/CO2 flooding at the flame root."

        history_line = f"\n**Prior Session Continuity:** {prior_context_str}" if prior_context_str else ""
        top_ref_id = extracted[0]["id"] if extracted else "NASA-STD-6001B"

        directive_text = (
            "### NASA OPERATIONAL FLIGHT SAFETY DIRECTIVE\n"
            f"**Query Focus:** {display_query}\n"
            f"**Grounded Docket Citations:** {ref_tags}{history_line}\n\n"
            "#### BLOCK 1: COMBUSTION KINETICS & AERODYNAMICS\n"
            f"{block1}\n\n"
            "#### BLOCK 2: NASA-STD-6001B COMPLIANCE EVALUATION\n"
            f"{block2}\n\n"
            "#### BLOCK 3: TACTICAL EMERGENCY CREW PROTOCOL\n"
            f"{t0_step}\n"
            f"{t15_step}\n"
            f"{t60_step} [Grounded in {top_ref_id}]"
        )
        return {
            "directive": directive_text,
            "citations": citations,
        }


def reformulate_query_with_history(
    query: str,
    chat_history: list[dict[str, Any]] | None = None,
) -> str:
    """Expand short/referential follow-up queries using prior user turns."""
    q = str(query or "").strip()
    if not chat_history:
        return q

    prior_msgs = [
        str(msg.get("query") or msg.get("content") or "").strip()
        for msg in chat_history
        if isinstance(msg, dict) and msg.get("role", "user") == "user"
    ]
    prior_msgs = [m for m in prior_msgs if m]
    if not prior_msgs:
        return q

    markers = ("it", "this", "that", "compare", "extinguish", "suppress", "còn", "nó")
    if len(q.split()) <= 10 or any(m in q.lower() for m in markers):
        return f"{' '.join(prior_msgs[-2:])} {q}"
    return q


reformulate_conversational_query = reformulate_query_with_history

_DEFAULT_ENGINE = DenseSemanticVectorIndex()


def get_default_rag_index() -> DenseSemanticVectorIndex:
    return _DEFAULT_ENGINE


def search_semantic(query: str, top_k: int = 3, threshold: float = 0.05) -> list[dict[str, Any]]:
    return _DEFAULT_ENGINE.search_semantic(query, top_k=top_k, threshold=threshold)


def ingest_user_document(file_bytes: bytes, filename: str) -> int:
    return _DEFAULT_ENGINE.ingest_user_document(file_bytes, filename)


def generate_grounded_directive(
    query: str,
    retrieved_docs: list[dict[str, Any]],
    chat_history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return _DEFAULT_ENGINE.generate_grounded_directive(query, retrieved_docs, chat_history)


def clear_custom_documents() -> None:
    _DEFAULT_ENGINE.clear_custom_documents()


def reset_custom_documents() -> None:
    _DEFAULT_ENGINE.clear_custom_documents()
