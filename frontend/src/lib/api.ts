import type { AskResponse } from "../types";

const API_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * GET /health — used to drive the online/offline indicator.
 * Returns true only when the backend responds with { status: "ok" }.
 */
export async function checkHealth(signal?: AbortSignal): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/health`, { signal });
    if (!res.ok) return false;
    const data = await res.json();
    return data?.status === "ok";
  } catch {
    return false;
  }
}

/**
 * POST /ask — sends the question to the FastAPI RAG backend and returns
 * the generated answer plus retrieved source passages. No fallback/mock
 * data is ever returned here; failures are surfaced to the caller.
 */
export async function askQuestion(question: string, signal?: AbortSignal): Promise<AskResponse> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      signal,
    });
  } catch (err) {
    if (err instanceof DOMException && err.name === "AbortError") throw err;
    throw new ApiError(
      "Could not reach the backend. Confirm FastAPI is running at " + API_URL + "."
    );
  }

  if (!res.ok) {
    let detail = "";
    try {
      const body = await res.json();
      detail = body?.detail ?? "";
    } catch {
      // response wasn't JSON — ignore
    }
    throw new ApiError(
      detail || `The backend returned an error (status ${res.status}).`
    );
  }

  const data = (await res.json()) as AskResponse;
  if (typeof data.answer !== "string") {
    throw new ApiError("The backend response was missing an answer.");
  }
  return {
    answer: data.answer,
    sources: Array.isArray(data.sources) ? data.sources : [],
  };
}

export { API_URL };
