export interface Source {
  section: string;
  text: string;
}

export interface AskResponse {
  answer: string;
  sources: Source[];
}

export type EntryStatus = "loading" | "done" | "error";

export interface ConversationEntry {
  id: string;
  question: string;
  answer?: string;
  sources?: Source[];
  status: EntryStatus;
  error?: string;
  timestamp: number;
}

export type BackendState = "checking" | "online" | "offline";
