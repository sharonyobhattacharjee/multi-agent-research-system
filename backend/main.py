
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

app = FastAPI(
    title="NEXUS Research API",
    description="Multi-Agent AI Research System",
    version="1.0.0",
)

# Allow requests from the local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str = Field(
        min_length=3,
        max_length=500,
        description="The research topic",
    )


@app.get("/")
async def root():
    return {
        "message": "NEXUS Research API is running",
        "status": "operational",
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/research")
async def research(request: ResearchRequest):
    try:
        # Import the existing research pipeline
        from pipeline import run_research_pipeline

        # Run the synchronous pipeline without blocking the API event loop
        result = await run_in_threadpool(
            run_research_pipeline,
            request.topic.strip(),
        )

        return {
            "status": "success",
            "topic": result.get("topic", request.topic),
            "report": str(result.get("report", "")),
            "feedback": str(result.get("feedback", "")),
            "search_results": str(result.get("search_results", "")),
            "scraped_content": str(result.get("scraped_content", "")),
        }

    except Exception as error:
        print(f"Research pipeline error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Research execution failed. Check the backend logs.",
        )
