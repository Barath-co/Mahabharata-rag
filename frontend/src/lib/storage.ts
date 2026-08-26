import type { ConversationEntry } from "../types";

const STORAGE_KEY = "mahabharata-rag-conversation";

export function loadConversation(): ConversationEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as ConversationEntry[];
    if (!Array.isArray(parsed)) return [];
    // Never resurrect an entry that was mid-flight when the tab closed.
    return parsed.filter((entry) => entry.status !== "loading");
  } catch {
    return [];
  }
}

export function saveConversation(entries: ConversationEntry[]): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  } catch {
    // localStorage unavailable (private mode, quota) — fail silently.
  }
}

export function clearConversation(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }
}
