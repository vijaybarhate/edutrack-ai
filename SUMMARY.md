# Project Summary: EduTrack AI

## Issues Fixed
| Description | Severity | Fix | Status |
|-------------|----------|-----|--------|
| Figure 2 and 3 not loading in report | High | Increased wait times (15s) and verified loading in Playwright before capture | Fixed |
| Incorrect GitHub Repo Link | Medium | Updated submission document and markdown report with correct link | Fixed |
| Professionalism of PDF Report | Medium | Redesigned `submission.html` with better CSS, Outfit fonts, and feature cards | Fixed |
| UI Responsiveness | Low | Added media queries and clamp() functions to ensure mobile support | Fixed |
| Git Environment | Low | Added `.gitignore` to prevent committing temporary/log files | Fixed |

## Remaining Known Issues
- **Performance**: The Streamlit dashboard can be slow on first load due to cold starts and network latency when fetching data from the FastAPI backend.
- **Data Persistence**: SQLite is used for local storage; however, in a production environment (like Streamlit Cloud), the database file may reset if not mounted on a persistent volume.

## Extra Suggestions
- **Deployment**: Recommend using Streamlit Cloud for the frontend and a hosted Postgres instance for the backend to ensure data persistence.
- **Security**: Add authentication to the dashboard so only authorized teachers can view student data.
- **AI Expansion**: Implement the Google Gemini API integration mentioned in the "Future Scope" to provide real-time tutoring.
