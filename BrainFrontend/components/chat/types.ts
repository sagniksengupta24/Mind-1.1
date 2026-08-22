export type Role = 'user' | 'assistant';

export interface Message {
  role: Role;
  content: string;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  updatedAt: number;
  backendSessionId?: string;
}
